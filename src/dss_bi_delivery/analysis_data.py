"""Build validated order-level views for historical logistics analysis.

Source outcomes are never rewritten. Unrecoverable local place names become an
explicit unknown category; a separate timestamp-consistent view is sensitivity only.
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

UNKNOWN = "__UNKNOWN__"
DAMAGED_TEXT = r"[?\ufffd\x00-\x1f\x7f-\x9f]"
LABELS = {"Advance shipping": 0, "Shipping on time": 0, "Late delivery": 1}
MODES = {"First Class", "Second Class", "Standard Class", "Same Day"}
TEXT_FIELDS = ["payment_type", "customer_segment", "shipping_mode", "market",
               "order_region", "order_country", "order_state", "order_city"]
CORE_NUMERIC = ["shipping_days_actual", "shipping_days_scheduled", "line_count", "total_quantity"]
ANALYSIS_COLUMNS = [
    "order_id", "order_datetime", "order_year", "order_month", "order_weekday",
    "order_is_weekend", *TEXT_FIELDS, "line_count", "total_quantity",
    "shipping_days_scheduled", "shipping_days_actual", "delay_days", "late_days",
    "is_late_from_days", "late_delivery_risk", "delivery_status",
    "order_state_unknown_flag", "order_city_unknown_flag", "duration_mismatch_flag",
]
# Explicit allowlist. IDs/timestamps are join keys, not estimators' features.
FEATURES = ["order_year", "order_month", "order_weekday", "order_is_weekend",
            "shipping_days_scheduled", "shipping_mode", "market", "order_region",
            "order_country", "customer_segment", "payment_type", "line_count", "total_quantity"]


def normalize_labels(values: pd.Series) -> pd.Series:
    return values.astype("string").map(
        lambda x: unicodedata.normalize("NFC", x) if pd.notna(x) else pd.NA
    ).astype("string").str.replace(r"\s+", " ", regex=True).str.strip().replace("", pd.NA)


def build_analysis(orders: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Validate every order; quarantine failures instead of guessing missing outcomes."""
    d = orders.copy()
    adjustments = []
    for c in TEXT_FIELDS:
        old = d[c].astype("string")
        d[c] = normalize_labels(old)
        count = int(old.fillna("").ne(d[c].fillna("")).sum())
        adjustments.append({"column": c, "action": "normalize_NFC_and_whitespace", "affected_orders": count})
    for c in ["order_datetime", "shipping_datetime"]:
        d[c] = pd.to_datetime(d[c], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    for c in CORE_NUMERIC + ["late_delivery_risk", "invalid_logistics_flag", "order_header_conflict"]:
        d[c] = pd.to_numeric(d[c], errors="coerce")

    # Bad city/state labels cannot be recovered safely from a question mark.
    geographic_issues = []
    for c in ["order_state", "order_city"]:
        bad = d[c].isna() | d[c].str.contains(DAMAGED_TEXT, regex=True, na=False)
        geographic_issues.append(pd.DataFrame({"column": c, "original_value": d.loc[bad, c].fillna("<MISSING>"),
                                              "order_id": d.loc[bad, "order_id"]}))
        d[f"{c}_unknown_flag"] = bad.astype("Int64")
        d.loc[bad, c] = UNKNOWN
        adjustments.append({"column": c, "action": "unknown_category_with_flag", "affected_orders": int(bad.sum())})

    reason = pd.DataFrame(index=d.index)
    reason["shipping_canceled"] = d["delivery_status"].eq("Shipping canceled").fillna(False)
    reason["missing_or_duplicate_order_id"] = (
        d["order_id"].isna() | d["order_id"].astype("string").str.strip().eq("")
        | d["order_id"].duplicated(keep=False)
    )
    required_text = [c for c in TEXT_FIELDS if c not in ["order_state", "order_city"]]
    reason["missing_or_damaged_required_category"] = d[required_text].isna().any(axis=1)
    for c in required_text:
        reason["missing_or_damaged_required_category"] |= d[c].str.contains(DAMAGED_TEXT, regex=True, na=False)
    reason["invalid_shipping_mode"] = ~d["shipping_mode"].isin(MODES)
    reason["invalid_payment_type"] = ~d["payment_type"].isin(["DEBIT", "TRANSFER", "CASH", "PAYMENT"])
    reason["invalid_customer_segment"] = ~d["customer_segment"].isin(["Consumer", "Corporate", "Home Office"])
    reason["invalid_market"] = ~d["market"].isin(["Africa", "Europe", "LATAM", "Pacific Asia", "USCA"])
    reason["missing_or_invalid_datetime"] = (
        d[["order_datetime", "shipping_datetime"]].isna().any(axis=1)
        | d["shipping_datetime"].lt(d["order_datetime"])
    )
    reason["invalid_numeric_domain"] = False
    for c in CORE_NUMERIC:
        good = d[c].notna() & np.isfinite(d[c].astype(float)) & d[c].mod(1).eq(0)
        good &= d[c].ge(0) if c.startswith("shipping_days") else d[c].gt(0)
        reason["invalid_numeric_domain"] |= ~good.fillna(False)
    days = d["shipping_days_actual"] - d["shipping_days_scheduled"]
    expected = d["delivery_status"].map(LABELS)
    reason["invalid_or_inconsistent_label"] = (
        ~d["late_delivery_risk"].isin([0, 1]) | ~d["delivery_status"].isin(LABELS)
        | d["late_delivery_risk"].ne(expected).fillna(True)
        | days.gt(0).astype("Int64").ne(d["late_delivery_risk"]).fillna(True)
        | (d["delivery_status"].eq("Advance shipping") & ~days.lt(0))
        | (d["delivery_status"].eq("Shipping on time") & ~days.eq(0))
    )
    # Cancellations have their own reason; their 0 labels are not corruption.
    reason.loc[reason["shipping_canceled"], "invalid_or_inconsistent_label"] = False
    reason["source_validation_failure"] = d["invalid_logistics_flag"].ne(0).fillna(True)
    reason["order_header_conflict"] = d["order_header_conflict"].ne(0).fillna(True)
    reason = reason.fillna(True).astype(bool)
    rejected_mask = reason.any(axis=1)
    rejected = d.loc[rejected_mask, ["order_id", "delivery_status", "shipping_mode"]].copy()
    rejected["exclusion_reasons"] = pd.Series(
        [";".join(reason.columns[row]) for row in reason.loc[rejected_mask].to_numpy()],
        index=rejected.index, dtype="string",
    )
    reason_counts = pd.DataFrame({"reason": reason.columns, "excluded_orders": reason.sum().values})

    # Derive from validated values instead of trusting stale derived columns.
    d["order_year"] = d["order_datetime"].dt.year.astype("Int64")
    d["order_month"] = d["order_datetime"].dt.month.astype("Int64")
    d["order_weekday"] = d["order_datetime"].dt.dayofweek.astype("Int64")
    d["order_is_weekend"] = d["order_weekday"].ge(5).astype("Int64")
    d["delay_days"] = days
    d["late_days"] = days.clip(lower=0)
    d["is_late_from_days"] = days.gt(0).astype("Int64")
    span = (d["shipping_datetime"] - d["order_datetime"]).dt.total_seconds() / 86400
    d["duration_mismatch_flag"] = span.sub(d["shipping_days_actual"]).abs().gt(1e-8).fillna(True).astype("Int64")
    analysis = d.loc[~rejected_mask, ANALYSIS_COLUMNS].sort_values(["order_datetime", "order_id"]).reset_index(drop=True)
    for c in CORE_NUMERIC + ["late_delivery_risk", "delay_days", "late_days", "is_late_from_days"]:
        analysis[c] = analysis[c].astype("Int64")
    strict = analysis.loc[analysis["duration_mismatch_flag"].eq(0)].copy()
    x = analysis[["order_id", "order_datetime", *FEATURES]].copy()
    y = analysis[["order_id", "late_delivery_risk"]].copy()

    # Fixed historical partitions, with a conservative seven-day purge before cuts.
    # The shipment timestamp is only a proxy for observed outcome availability.
    split = analysis[["order_id", "order_datetime"]].copy()
    split["partition"] = "test"
    validation_start = pd.Timestamp("2017-01-01")
    test_start = pd.Timestamp("2017-07-01")
    split.loc[split.order_datetime.lt(test_start), "partition"] = "validation"
    split.loc[split.order_datetime.lt(validation_start), "partition"] = "train"
    available = d.set_index("order_id")["shipping_datetime"] if d["order_id"].is_unique else None
    if available is None:
        # Duplicate IDs are already quarantined; map only unambiguous source IDs.
        available = d.loc[~d["order_id"].duplicated(keep=False)].set_index("order_id")["shipping_datetime"]
    outcome_proxy = split.order_id.map(available)
    for name, cutoff in [("train", validation_start), ("validation", test_start)]:
        purge = split.partition.eq(name) & (
            split.order_datetime.ge(cutoff - pd.Timedelta(days=7)) | outcome_proxy.ge(cutoff) | outcome_proxy.isna()
        )
        split.loc[purge, "partition"] = "purged_boundary"

    geography = pd.concat(geographic_issues, ignore_index=True)
    geography = geography.groupby(["column", "original_value"], dropna=False).size().reset_index(name="affected_orders")
    changes = pd.DataFrame(adjustments)
    return {"analysis": analysis, "timestamp_consistent": strict, "features": x, "labels": y,
            "splits": split, "excluded": rejected, "exclusion_summary": reason_counts,
            "geography_changes": geography, "cleaning_changes": changes}


def validate_views(views: dict[str, pd.DataFrame], source_orders: pd.DataFrame) -> dict:
    a, strict = views["analysis"], views["timestamp_consistent"]
    x, y, splits = views["features"], views["labels"], views["splits"]
    checks = {}
    checks["primary_nonempty"] = len(a) > 0
    checks["primary_no_missing_cells"] = not a.isna().any().any()
    checks["primary_no_duplicate_order_ids"] = a.order_id.is_unique
    checks["primary_no_duplicate_rows"] = not a.duplicated().any()
    numbers = a.select_dtypes("number")
    checks["primary_all_numeric_values_finite"] = np.isfinite(numbers.to_numpy(dtype=float)).all()
    checks["primary_no_cancellations"] = a.delivery_status.isin(LABELS).all()
    checks["primary_target_agrees_with_days"] = a.late_delivery_risk.eq(a.shipping_days_actual.gt(a.shipping_days_scheduled).astype(int)).all()
    checks["primary_no_damaged_geographic_labels"] = not any(
        a[c].str.contains(DAMAGED_TEXT, regex=True, na=False).any() for c in TEXT_FIELDS
    )
    checks["unknown_categories_have_explicit_flags"] = all(
        a[c].eq(UNKNOWN).eq(a[f"{c}_unknown_flag"].eq(1)).all() for c in ["order_city", "order_state"]
    )
    checks["all_source_rows_accounted_for"] = len(a) + len(views["excluded"]) == len(source_orders)
    checks["features_exact_allowlist"] = list(x.columns) == ["order_id", "order_datetime", *FEATURES]
    checks["features_no_outcomes_or_post_event_flags"] = not set(x.columns).intersection({
        "late_delivery_risk", "delivery_status", "shipping_days_actual", "delay_days", "late_days",
        "is_late_from_days", "shipping_datetime", "order_status", "duration_mismatch_flag", "delivery_kpi_eligible",
    })
    checks["feature_label_split_alignment"] = x.order_id.equals(y.order_id) and x.order_id.equals(splits.order_id)
    checks["feature_values_match_analysis_table"] = all(x[c].equals(a[c]) for c in ["order_datetime", *FEATURES])
    checks["label_values_match_analysis_table"] = y.late_delivery_risk.equals(a.late_delivery_risk)
    checks["split_timestamps_match_analysis_table"] = splits.order_datetime.equals(a.order_datetime)
    checks["features_no_missing_cells"] = not x.isna().any().any()
    checks["target_labels_preserved_from_source"] = a.late_delivery_risk.astype(int).tolist() == pd.to_numeric(
        a.order_id.map(source_orders.drop_duplicates("order_id").set_index("order_id").late_delivery_risk)
    ).astype(int).tolist()
    checks["timestamp_consistent_subset_no_mismatch"] = strict.duration_mismatch_flag.eq(0).all()
    checks["strict_partition_accounts_for_mismatch"] = len(strict) + int(a.duration_mismatch_flag.sum()) == len(a)
    period_ranges = []
    for name in ["train", "validation", "test"]:
        sub = splits.loc[splits.partition.eq(name), "order_datetime"]
        checks[f"{name}_nonempty"] = not sub.empty
        period_ranges.append((sub.min(), sub.max()))
    checks["partitions_chronological"] = period_ranges[0][1] < period_ranges[1][0] and period_ranges[1][1] < period_ranges[2][0]
    result = {"checks": {k: bool(v) for k, v in checks.items()}}
    result.update(passed=sum(result["checks"].values()), total=len(checks), all_passed=all(result["checks"].values()))
    return result


def export_analysis(orders: pd.DataFrame, root: Path) -> dict:
    from .prepare_data import csv, markdown

    views = build_analysis(orders)
    validation = validate_views(views, orders)
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "analysis_validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
    if not validation["all_passed"]:
        raise ValueError("Analysis data failed validation. See reports/analysis_validation.json")
    names = {"analysis": "orders_analysis.csv", "timestamp_consistent": "orders_timestamp_consistent.csv",
             "features": "orders_model_features.csv", "labels": "orders_model_labels.csv",
             "splits": "orders_model_splits.csv", "excluded": "orders_excluded.csv"}
    for key, name in names.items():
        csv(views[key], root / "data/processed" / name)
    for key in ["exclusion_summary", "geography_changes", "cleaning_changes"]:
        csv(views[key], reports / f"analysis_{key}.csv")
    a = views["analysis"]
    monthly_mode = a.groupby([a.order_datetime.dt.to_period("M").astype(str).rename("month"), "shipping_mode"]).agg(
        order_count=("order_id", "size"), late_count=("late_delivery_risk", "sum"),
        late_rate=("late_delivery_risk", "mean"), actual_days_min=("shipping_days_actual", "min"),
        actual_days_max=("shipping_days_actual", "max"), actual_days_unique=("shipping_days_actual", "nunique"),
        timestamp_discrepancies=("duration_mismatch_flag", "sum"),
    ).reset_index()
    csv(monthly_mode, reports / "anomalies_by_month_and_mode.csv")
    sensitivity = []
    for name, data in [("primary_source_duration", a), ("timestamp_consistent_only", views["timestamp_consistent"]),
                       ("without_first_class_sensitivity", a.loc[a.shipping_mode.ne("First Class")])]:
        sensitivity.append({"cohort": name, "orders": len(data), "late_count": int(data.late_delivery_risk.sum()),
                            "late_rate": float(data.late_delivery_risk.mean()),
                            "same_day_orders": int(data.shipping_mode.eq("Same Day").sum())})
    csv(pd.DataFrame(sensitivity), reports / "analysis_sensitivity.csv")
    durations = []
    for (mode, region), data in a.groupby(["shipping_mode", "order_region"]):
        durations.append({"shipping_mode": mode, "order_region": region, "order_count": len(data),
                          "late_rate": float(data.late_delivery_risk.mean()),
                          "mean_actual_days": float(data.shipping_days_actual.mean()),
                          **{f"p{int(q*100)}_actual_days": float(data.shipping_days_actual.quantile(q, interpolation="higher")) for q in [.5, .9, .95]}})
    csv(pd.DataFrame(durations), reports / "duration_distribution_by_mode_region.csv")
    split_summary = views["splits"].groupby("partition").agg(orders=("order_id", "size"),
                        start=("order_datetime", "min"), end=("order_datetime", "max")).reset_index()
    csv(split_summary, reports / "model_split_summary.csv")

    # A sidecar documents CSV dtypes and which fields are suitable for estimators.
    from .schema import DERIVED, ORDER_AGGREGATES, SCHEMA
    metadata = {s["column"]: {"dtype": s["dtype"], "role": s["role"], "definition": s["description_vi"]} for s in SCHEMA}
    metadata.update({v[0]: {"dtype": v[1], "role": v[4], "definition": v[5]} for v in DERIVED + ORDER_AGGREGATES})
    for c in ["order_city", "order_state"]:
        metadata[c]["definition"] += " Trong orders_analysis: tên không khôi phục được đổi thành __UNKNOWN__, kèm cờ."
        metadata[f"{c}_unknown_flag"] = {"dtype": "Int64", "role": "quality", "definition": f"1 nếu {c} thiếu hoặc chứa ký tự hỏng; __UNKNOWN__ không phải địa danh thật."}
    for c in a.columns:
        metadata[c]["used_as_model_feature"] = c in FEATURES
    schema = {"grain": "one row per non-canceled validated order", "columns": {c: metadata[c] for c in a.columns},
              "model_feature_columns": FEATURES, "join_keys_not_model_features": ["order_id", "order_datetime"],
              "unknown_category": UNKNOWN, "source_duration_semantics_unverified": True,
              "forecast_scope": "late delivery conditional on non-cancellation in this historical snapshot",
              "model_split_policy": {"validation_start": "2017-01-01", "test_start": "2017-07-01", "purge_days": 7,
                 "availability_proxy": "shipping_datetime; actual time of outcome recording is not supplied"}}
    (root / "docs/analysis_schema.json").write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {"input_orders": len(orders), "analysis_orders": len(a), "analysis_columns": len(a.columns),
               "excluded_orders": len(views["excluded"]), "timestamp_consistent_orders": len(views["timestamp_consistent"]),
               "unknown_city_orders": int(a.order_city_unknown_flag.sum()), "unknown_state_orders": int(a.order_state_unknown_flag.sum()),
               "missing_cells_in_analysis": int(a.isna().sum().sum()),
               "duration_discrepancy_orders_in_analysis": int(a.duration_mismatch_flag.sum()),
               "late_count": int(a.late_delivery_risk.sum()), "late_rate": float(a.late_delivery_risk.mean()),
               "numeric_values_imputed": 0, "target_values_rewritten": 0,
               "validation_passed": validation["passed"], "validation_total": validation["total"]}
    (reports / "analysis_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = "# Dữ liệu bàn giao cho bốn cấp độ phân tích\n\n"
    report += f"Bảng chính: `data/processed/orders_analysis.csv`, **{len(a):,} đơn × {len(a.columns)} cột**; thiếu ô: **{summary['missing_cells_in_analysis']}**. Không có giá trị số được gán hay nhãn bị sửa.\n\n"
    report += "Các kết quả đạt quy tắc kỹ thuật đã công bố, không xác minh được tính đúng ngoài đời của các chỉ báo nguồn. `orders_clean.csv` là bảng trung gian giữ đầy đủ đơn; dùng bảng analysis cho mẫu logistics chính.\n\n"
    report += "## Trước → sau\n\n" + markdown(pd.DataFrame([
        {"Vấn đề": "Đơn trong bảng trung gian", "Trước": len(orders), "Sau": len(a), "Xử lý": "Loại khỏi mẫu chính các đơn không đạt điều kiện; lưu mã và lý do ở orders_excluded.csv"},
        {"Vấn đề": "City/state hỏng hoặc thiếu", "Trước": int(views['geography_changes'].affected_orders.sum()), "Sau": "0 chuỗi hỏng trong bảng chính", "Xử lý": "Đổi thành __UNKNOWN__ và cờ; số trước là số ô trên mọi đơn, không phải số đơn duy nhất"},
        {"Vấn đề": "ZIP thiếu", "Trước": "Customer ZIP 3; Order ZIP 155679 dòng nguồn", "Sau": "Không có cột ZIP trong bảng chính", "Xử lý": "Loại trường không cần cho câu hỏi logistics; không xóa đơn vì ZIP"},
        {"Vấn đề": "Duration lệch timestamp", "Trước": int(pd.to_numeric(orders.duration_mismatch_flag).sum()), "Sau": int(a.duration_mismatch_flag.sum()), "Xử lý": "Mẫu chính dùng duration nguồn; bỏ timestamp shipment/span để tránh hai định nghĩa; mẫu đối chiếu thời gian riêng"},
    ])) + "\n\n"
    report += "## Đầu ra theo nhiệm vụ\n\n"
    report += "- Mô tả/chẩn đoán: orders_analysis.csv; không suy diễn quan hệ nhân quả từ liên hệ quan sát. Các tên địa lý chưa khôi phục nằm trong nhóm __UNKNOWN__ có cờ.\n"
    report += "- Dự báo: orders_model_features.csv, orders_model_labels.csv và orders_model_splits.csv. Chỉ FEATURES là đầu vào estimator; order_id và order_datetime chỉ để join/chia tập. Chưa huấn luyện/đánh giá mô hình. Tập này có điều kiện không hủy; không đại diện mọi đơn mới.\n"
    report += "- Đề xuất cam kết: duration_distribution_by_mode_region.csv có phân vị và số đơn. Đây là phân phối lịch sử toàn mẫu để khám phá, không phải khuyến nghị hay feature huấn luyện; nếu đánh giá trên test phải tính lại phân vị chỉ từ train.\n"
    report += "- Tối ưu tuyến: chưa đủ đầu vào. Phải bổ sung Solomon hoặc điểm dừng/xe/khung giờ phù hợp.\n\n"
    report += "## Bất thường đã điều tra\n\n"
    first = monthly_mode.loc[monthly_mode.shipping_mode.eq("First Class")]
    report += f"First Class trễ 100% ở **{int(first.late_rate.eq(1).sum())}/{len(first)} tháng** có quan sát trong mẫu chính. Không tự sửa nhãn hay xóa nhóm. Xem anomalies_by_month_and_mode.csv và so sánh mô hình có/không Shipping Mode sau này.\n\n"
    report += "Same Day có chênh lệch ±0,5 ngày giữa duration và khoảng timestamp. Dữ liệu không chứng minh cơ chế; không ép hai trường bằng nhau. Nếu chỉ giữ timestamp nhất quán thì mất toàn bộ Same Day, vì vậy bảng đó chỉ dùng độ nhạy, không thay mẫu chính.\n\n"
    report += markdown(pd.DataFrame(sensitivity).round(6)) + "\n\n## Chia tập lịch sử\n\n" + markdown(split_summary) + "\n\n"
    report += "Các cut 01/01/2017 và 01/07/2017 được chốt trước huấn luyện. Chừa 7 ngày trước mỗi cut (lớn hơn duration tối đa 6 ngày của bản nguồn); dùng shipping timestamp làm proxy bổ sung. Thời điểm ghi nhận nhãn thật chưa được nguồn cung cấp nên đây chưa là chứng minh hết leakage. Mọi encoding/gán giá trị/scaling và tổng hợp lịch sử phải fit trên train. Không dùng dòng purged_boundary để fit hoặc chấm điểm.\n\n"
    report += f"Kiểm tra bàn giao: **{validation['passed']}/{validation['total']}**. Xem analysis_validation.json; dictionary và allowlist tại docs/analysis_schema.json.\n"
    (reports / "analysis_readiness_report.md").write_text(report, encoding="utf-8")
    return summary
