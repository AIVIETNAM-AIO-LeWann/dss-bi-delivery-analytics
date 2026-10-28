"""Independently reconcile exported tables to the pinned raw CSV, without rewriting them."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .schema import DERIVED, EXPECTED_SHA256, ORDER_AGGREGATES, SCHEMA

ROOT = Path(__file__).resolve().parents[2]


def verify() -> dict:
    raw_path = ROOT / "data/raw/DataCoSupplyChainDataset.csv"
    raw = pd.read_csv(raw_path, encoding="cp1252", dtype="string", keep_default_na=False, na_values=[""])
    items = pd.read_csv(ROOT / "data/processed/order_items_clean.csv", encoding="utf-8-sig", dtype="string")
    orders = pd.read_csv(ROOT / "data/processed/orders_clean.csv", encoding="utf-8-sig", dtype="string")
    checks: dict[str, bool] = {}

    def check(name: str, ok: object) -> None:
        checks[name] = bool(ok)

    check("raw_checksum_unchanged", hashlib.sha256(raw_path.read_bytes()).hexdigest() == EXPECTED_SHA256)
    check("all_source_lines_preserved", len(items) == len(raw) == 180519)
    check("order_item_identity_preserved_in_source_order", items["order_item_id"].equals(raw["Order Item Id"]))
    check("source_row_trace_complete", pd.to_numeric(items["source_row_number"]).tolist() == list(range(2, len(raw) + 2)))
    check("orders_are_unique_and_complete", orders["order_id"].is_unique
          and set(orders["order_id"]) == set(raw["Order Id"]) and len(orders) == 65752)
    line_counts = raw.groupby("Order Id").size().sort_index()
    exported_counts = pd.to_numeric(orders.set_index("order_id")["line_count"]).sort_index()
    check("per_order_line_count_reconciles", np.array_equal(line_counts.to_numpy(), exported_counts.to_numpy()))
    for original, exported in [("Order Item Quantity", "total_quantity"), ("Sales", "sales_gross_total"), ("Order Item Total", "item_total_net_sum")]:
        source_totals = pd.to_numeric(raw[original]).groupby(raw["Order Id"]).sum().sort_index()
        clean_totals = pd.to_numeric(orders.set_index("order_id")[exported]).sort_index()
        check(f"per_order_{exported}_reconciles", np.allclose(source_totals, clean_totals, rtol=0, atol=1e-8))
    check("target_labels_unchanged", items["late_delivery_risk"].equals(raw["Late_delivery_risk"]))
    # Boundary example: scheduled=0 is valid; canceled outcomes are not silently recoded.
    same_day = raw["Shipping Mode"].eq("Same Day")
    check("zero_day_same_day_preserved", (pd.to_numeric(items.loc[same_day, "shipping_days_scheduled"]) == 0).all())
    canceled = raw["Delivery Status"].eq("Shipping canceled")
    check("canceled_rows_retained_but_excluded_from_primary_kpi", canceled.sum() == 7754
          and items.loc[canceled, "delivery_kpi_eligible"].eq("0").all())
    positive_delay_canceled = canceled & (
        pd.to_numeric(raw["Days for shipping (real)"]) > pd.to_numeric(raw["Days for shipment (scheduled)"])
    )
    check("canceled_positive_delay_does_not_overwrite_target", positive_delay_canceled.sum() == 4423
          and items.loc[positive_delay_canceled, "is_late_from_days"].eq("1").all()
          and items.loc[positive_delay_canceled, "late_delivery_risk"].eq("0").all())
    negative_profit = pd.to_numeric(raw["Order Profit Per Order"]).lt(0)
    check("negative_profit_preserved", negative_profit.any()
          and items.loc[negative_profit, "order_profit_per_order"].notna().all()
          and pd.to_numeric(items.loc[negative_profit, "order_profit_per_order"]).lt(0).all())
    check("dates_preserve_original_order_timestamp", pd.to_datetime(items["order_datetime"], format="%Y-%m-%d %H:%M:%S").equals(
        pd.to_datetime(raw["order date (DateOrders)"], format="%m/%d/%Y %H:%M")))
    retained = {s["column"] for s in SCHEMA if not s["treatment"].startswith("drop_")}
    check("item_dictionary_covers_all_exported_columns", set(items.columns) == retained | {row[0] for row in DERIVED})
    check("order_dictionary_covers_all_exported_columns", set(orders.columns).issubset(retained | {row[0] for row in DERIVED + ORDER_AGGREGATES}))
    primary = orders["delivery_kpi_eligible"].eq("1")
    check("primary_order_kpi_reconciles", primary.sum() == 62897
          and pd.to_numeric(orders.loc[primary, "late_delivery_risk"]).sum() == 36048)
    check("no_personal_names_email_password_street_in_exports", not {
        "customer_email", "customer_first_name", "customer_last_name", "customer_password", "customer_street"
    }.intersection(set(items.columns) | set(orders.columns)))
    # Inspect saved analysis exports, rather than relying on in-memory validation.
    from .analysis_data import validate_views

    schema = json.loads((ROOT / "docs/analysis_schema.json").read_text(encoding="utf-8"))

    def read_analysis(name: str) -> pd.DataFrame:
        path = ROOT / "data/processed" / name
        header = pd.read_csv(path, encoding="utf-8-sig", nrows=0).columns
        dtypes = {c: meta["dtype"] for c, meta in schema["columns"].items()
                  if c in header and meta["dtype"] != "datetime"}
        dtypes["order_id"] = "string"
        frame = pd.read_csv(path, encoding="utf-8-sig", dtype=dtypes)
        if "order_datetime" in frame:
            frame["order_datetime"] = pd.to_datetime(frame["order_datetime"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
        return frame

    views = {key: read_analysis(name) for key, name in {
        "analysis": "orders_analysis.csv", "timestamp_consistent": "orders_timestamp_consistent.csv",
        "features": "orders_model_features.csv", "labels": "orders_model_labels.csv",
        "splits": "orders_model_splits.csv", "excluded": "orders_excluded.csv",
    }.items()}
    validated = validate_views(views, orders)
    for name, ok in validated["checks"].items():
        check(f"analysis_{name}", ok)
    expected_ids = set(raw.loc[raw["Delivery Status"].ne("Shipping canceled"), "Order Id"])
    check("analysis_order_ids_match_source_non_canceled_orders", set(views["analysis"].order_id) == expected_ids)
    raw_headers = raw.drop_duplicates("Order Id").set_index("Order Id")
    a = views["analysis"]
    for original, clean in [("Order City", "order_city"), ("Order State", "order_state")]:
        source_values = a.order_id.map(raw_headers[original])
        bad = source_values.isna() | source_values.str.contains(r"[?\ufffd\x00-\x1f\x7f-\x9f]", regex=True, na=False)
        check(f"analysis_{clean}_unknown_flags_match_raw_damage", bad.to_numpy().tolist() == a[f"{clean}_unknown_flag"].eq(1).tolist())
    source_order_time = pd.to_datetime(a.order_id.map(raw_headers["order date (DateOrders)"]), format="%m/%d/%Y %H:%M")
    source_ship_time = pd.to_datetime(a.order_id.map(raw_headers["shipping date (DateOrders)"]), format="%m/%d/%Y %H:%M")
    source_days = pd.to_numeric(a.order_id.map(raw_headers["Days for shipping (real)"]))
    independent_mismatch = ((source_ship_time - source_order_time).dt.total_seconds() / 86400 - source_days).abs().gt(1e-8)
    check("timestamp_consistent_ids_reconciled_to_raw", set(views["timestamp_consistent"].order_id) == set(a.loc[~independent_mismatch, "order_id"]))
    split = views["splits"]
    source_shipping = pd.to_datetime(split.order_id.map(raw_headers["shipping date (DateOrders)"]), format="%m/%d/%Y %H:%M")
    for name, cutoff_text in [("train", "2017-01-01"), ("validation", "2017-07-01")]:
        selected = split.partition.eq(name)
        cutoff = pd.Timestamp(cutoff_text)
        check(f"{name}_respects_seven_day_gap", split.loc[selected, "order_datetime"].lt(cutoff - pd.Timedelta(days=7)).all())
        check(f"{name}_source_shipping_before_cutoff", source_shipping.loc[selected].lt(cutoff).all())
    result = {"checks": checks, "passed": sum(checks.values()), "total": len(checks), "all_passed": all(checks.values())}
    (ROOT / "reports/validation_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["all_passed"]:
        raise AssertionError("Export reconciliation failed; see reports/validation_results.json")
    return result


if __name__ == "__main__":
    verify()
