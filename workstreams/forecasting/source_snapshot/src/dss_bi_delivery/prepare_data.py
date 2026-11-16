"""Reproducible DataCo profiling, conservative cleaning, and order-level exports."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .schema import DERIVED, EXPECTED_SHA256, ORDER_AGGREGATES, ORDER_FIELDS, SCHEMA

ROOT = Path(__file__).resolve().parents[2]
DELIVERY_STATUSES = {"Advance shipping", "Late delivery", "Shipping canceled", "Shipping on time"}
SHIPPING_MODES = {"Standard Class", "First Class", "Second Class", "Same Day"}
ORDER_STATUSES = {"COMPLETE", "PENDING", "CLOSED", "PENDING_PAYMENT", "CANCELED",
                  "PROCESSING", "SUSPECTED_FRAUD", "ON_HOLD", "PAYMENT_REVIEW"}


def csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d %H:%M:%S")


def markdown(df: pd.DataFrame) -> str:
    def escape(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")
    return "\n".join([
        "| " + " | ".join(map(escape, df.columns)) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
        *["| " + " | ".join(map(escape, row)) + " |" for row in df.itertuples(index=False, name=None)],
    ])


def make_kpis(frame: pd.DataFrame, grain: str) -> list[dict]:
    rows = []
    cohorts = {
        "all_source_labels": pd.Series(True, index=frame.index),
        "non_canceled_valid": frame["delivery_kpi_eligible"].eq(1),
        "complete_closed_sensitivity": frame["delivery_kpi_eligible"].eq(1)
        & frame["order_status"].isin(["COMPLETE", "CLOSED"]),
    }
    for name, mask in cohorts.items():
        sub = frame.loc[mask]
        valid = sub["late_delivery_risk"].isin([0, 1])
        numerator = int(sub.loc[valid, "late_delivery_risk"].sum())
        denominator = int(valid.sum())
        rows.append({"grain": grain, "cohort": name, "records_in_cohort": len(sub),
                     "late_count": numerator, "labeled_count": denominator,
                     "late_rate": numerator / denominator if denominator else None,
                     "mean_actual_days": float(sub["shipping_days_actual"].mean()) if len(sub) else None})
    return rows


def run(source: Path, allow_source_change: bool = False) -> dict:
    checksum = hashlib.sha256(source.read_bytes()).hexdigest()
    if checksum != EXPECTED_SHA256 and not allow_source_change:
        raise ValueError("Source checksum changed. Review version/encoding/schema before using --allow-source-change.")
    # Windows-1252 decodes the entire reference file strictly; latin-1 creates 20 C1 controls.
    raw = pd.read_csv(source, encoding="cp1252", dtype="string", keep_default_na=False, na_values=[""])
    expected = [s["source_column"] for s in SCHEMA]
    if list(raw.columns) != expected:
        raise ValueError("CSV columns/order differ from the documented 53-column schema.")
    reports = ROOT / "reports"
    processed = ROOT / "data/processed"
    for path in (reports, processed, ROOT / "docs"):
        path.mkdir(parents=True, exist_ok=True)
    log: list[dict] = []

    def record(stage: str, rule: str, field: str, count: int, action: str, reason: str) -> None:
        log.append({"stage": stage, "rule": rule, "field": field, "affected_rows": int(count),
                    "action": action, "reason_vi": reason})

    d = raw.rename(columns={s["source_column"]: s["column"] for s in SCHEMA}).copy()
    for s in SCHEMA:
        c = s["column"]
        old = d[c]
        trimmed = old.str.strip().replace("", pd.NA)
        changed = old.fillna("<NA>").ne(trimmed.fillna("<NA>"))
        d[c] = trimmed
        record("1_quality", "trim", c, changed.sum(), "strip đầu/cuối; rỗng thành NA", "Không đổi nội dung bên trong hay tự sửa tên địa lý.")
        if s["dtype"] in ("Int64", "Float64"):
            numeric = pd.to_numeric(trimmed, errors="coerce")
            bad = trimmed.notna() & numeric.isna()
            nonfinite = numeric.notna() & ~np.isfinite(numeric.astype(float))
            bad |= nonfinite
            numeric = numeric.mask(nonfinite)
            if s["dtype"] == "Int64":
                fraction = numeric.notna() & numeric.mod(1).ne(0)
                bad |= fraction
                numeric = numeric.mask(fraction)
            d[c] = numeric.astype(s["dtype"])
            record("1_quality", "numeric_parse", c, bad.sum(), "NA nếu không parse; giữ raw", "Không gán trung bình/trung vị.")
        elif s["dtype"] == "datetime":
            parsed = pd.to_datetime(trimmed, format="%m/%d/%Y %H:%M", errors="coerce")
            flag = "order_date_parse_failed" if c == "order_datetime" else "shipping_date_parse_failed"
            d[flag] = (trimmed.notna() & parsed.isna()).astype("Int64")
            d[c] = parsed
            record("1_quality", "datetime_parse", c, d[flag].sum(), "parse định dạng tường minh; lỗi thành NaT", "Không tự suy diễn DD/MM hoặc múi giờ.")
        elif c.endswith("zipcode"):
            # CSV stores ZIPs such as 603.0. Remove numeric serialization suffix only.
            d[c] = trimmed.str.replace(r"\.0$", "", regex=True)
            record("1_quality", "zipcode_string", c, trimmed.ne(d[c]).fillna(False).sum(), "chuỗi; bỏ hậu tố .0", "Không đoán hay khôi phục số 0 đầu bị mất từ nguồn.")

    # Validate all duplicate-column claims before dropping any data.
    duplicate_pairs = [
        ("benefit_per_order", "order_profit_per_order"), ("sales_per_customer", "item_total_net"),
        ("product_price", "item_unit_price"), ("order_customer_id", "customer_id"),
        ("product_category_id", "category_id"), ("order_item_product_id", "product_id"),
    ]
    relationships = []
    for left, right in duplicate_pairs:
        equal = (d[left].eq(d[right]) | (d[left].isna() & d[right].isna())).fillna(False)
        relationships.append({"left": left, "right": right, "mismatch_rows": int((~equal).sum())})
        if not equal.all():
            raise ValueError(f"Duplicate-column assumption no longer holds: {left}, {right}")
        record("2_validate", "duplicate_column_verified", left, len(d), f"giữ {right}", "Đã đối chiếu toàn bộ giá trị, không dựa vào tên cột.")

    d["source_row_number"] = pd.Series(range(2, len(d) + 2), dtype="Int64")
    d["order_year"] = d["order_datetime"].dt.year.astype("Int64")
    d["order_month"] = d["order_datetime"].dt.month.astype("Int64")
    d["order_weekday"] = d["order_datetime"].dt.dayofweek.astype("Int64")
    d["order_is_weekend"] = d["order_weekday"].ge(5).astype("Int64")
    d["delay_days"] = d["shipping_days_actual"] - d["shipping_days_scheduled"]
    d["late_days"] = d["delay_days"].clip(lower=0)
    d["is_late_from_days"] = d["delay_days"].gt(0).astype("Int64")
    d["is_shipping_canceled"] = d["delivery_status"].eq("Shipping canceled").astype("Int64")
    d["timestamp_span_days"] = (d["shipping_datetime"] - d["order_datetime"]).dt.total_seconds().div(86400).astype("Float64")
    d["duration_mismatch_flag"] = (d["timestamp_span_days"] - d["shipping_days_actual"]).abs().gt(1e-8).fillna(True).astype("Int64")

    invalid = pd.Series(False, index=d.index)
    core = ["order_id", "order_item_id", "order_datetime", "shipping_datetime", "shipping_days_actual",
            "shipping_days_scheduled", "late_delivery_risk", "shipping_mode", "delivery_status", "order_status"]
    missing_core = d[core].isna().any(axis=1)
    invalid |= missing_core
    record("2_validate", "missing_core", ", ".join(core), missing_core.sum(), "gắn cờ; loại khỏi KPI chuẩn", "Không xóa nguồn hay tự điền nhãn.")
    duplicate_items = d["order_item_id"].duplicated(keep=False) & d["order_item_id"].notna()
    invalid |= duplicate_items
    record("2_validate", "duplicate_item_id", "order_item_id", duplicate_items.sum(), "gắn cờ tất cả bản ghi trùng khóa", "Order Id lặp không phải lỗi; Order Item Id mới là khóa dòng.")
    for c, allowed in [("delivery_status", DELIVERY_STATUSES), ("shipping_mode", SHIPPING_MODES),
                       ("order_status", ORDER_STATUSES), ("late_delivery_risk", {0, 1})]:
        bad = ~d[c].isin(allowed)
        invalid |= bad
        record("2_validate", "category_domain", c, bad.sum(), "gắn cờ giá trị ngoài miền", "Miền của phiên bản được ghi nhận; không tự thay nhãn mới.")
    negative_days = d[["shipping_days_actual", "shipping_days_scheduled"]].lt(0).any(axis=1)
    negative_span = d["timestamp_span_days"].lt(0).fillna(False)
    invalid |= negative_days | negative_span
    record("2_validate", "negative_duration", "shipping_days_actual; scheduled; timestamps", (negative_days | negative_span).sum(), "gắn cờ", "Khoảng thời gian thực tế âm cần xem lại nguồn.")
    expected_label = d["delivery_status"].map({"Late delivery": 1, "Advance shipping": 0, "Shipping on time": 0, "Shipping canceled": 0})
    label_mismatch = d["late_delivery_risk"].ne(expected_label).fillna(True)
    non_cancel = d["delivery_status"].isin(DELIVERY_STATUSES - {"Shipping canceled"})
    days_mismatch = non_cancel & d["is_late_from_days"].ne(d["late_delivery_risk"]).fillna(True)
    status_days_mismatch = (
        (d["delivery_status"].eq("Advance shipping") & ~d["delay_days"].lt(0))
        | (d["delivery_status"].eq("Shipping on time") & ~d["delay_days"].eq(0))
        | (d["delivery_status"].eq("Late delivery") & ~d["delay_days"].gt(0))
    ).fillna(True)
    invalid |= label_mismatch | days_mismatch | status_days_mismatch
    record("2_validate", "label_consistency", "delivery_status; late_delivery_risk; delay_days", (label_mismatch | days_mismatch | status_days_mismatch).sum(), "gắn cờ lỗi nhất quán", "Không bắt nhãn trễ của đơn hủy phải bằng chênh lệch ngày.")
    d["invalid_logistics_flag"] = invalid.astype("Int64")
    d["delivery_kpi_eligible"] = (non_cancel & ~invalid).astype("Int64")
    record("2_validate", "duration_comparison", "timestamps vs shipping_days_actual", d["duration_mismatch_flag"].sum(), "chỉ gắn cờ; không tự sửa duration", "Nguồn có chênh 0.5 ngày; chưa rõ cơ chế làm tròn hay ngữ nghĩa.")
    for c, low, high in [("store_latitude", -90, 90), ("store_longitude", -180, 180)]:
        record("2_validate", "coordinate_range", c, (~d[c].between(low, high)).sum(), "chỉ báo chất lượng", "Tọa độ cửa hàng; không coi là điểm dừng giao hàng.")
    for c in ["item_quantity", "item_unit_price", "sales_gross", "item_total_net", "item_discount"]:
        bad = d[c].isna() | d[c].lt(0)
        if c == "item_quantity":
            bad |= d[c].eq(0)
        record("2_validate", "numeric_business_domain", c, bad.sum(), "ghi nhận; không tự sửa hoặc xóa dòng", "Quantity phải dương; giá/giảm giá phải không âm trong quy ước hiện tại.")
    record("2_validate", "discount_rate_domain", "item_discount_rate",
           (~d["item_discount_rate"].between(0, 1)).sum(), "ghi nhận ngoài miền [0;1]", "Không tự chia 100 khi chưa xác minh cách lưu nguồn.")
    for name, residual in [
        ("gross_equals_price_times_quantity", d["sales_gross"] - d["item_unit_price"] * d["item_quantity"]),
        ("net_equals_gross_less_discount", d["item_total_net"] - d["sales_gross"] + d["item_discount"]),
    ]:
        record("2_validate", name, "sales_gross; item_total_net; item_discount; price; quantity",
               (residual.isna() | residual.abs().gt(0.011)).sum(), "đối chiếu nội bộ, dung sai tuyệt đối 0.011 đơn vị tiền", "Giữ nguyên giá trị nguồn; kiểm tra này không xác thực loại tiền hay chuẩn mực kế toán.")

    # Distribution diagnostics do not invent business thresholds for outliers.
    stats = d[[s["column"] for s in SCHEMA if s["dtype"] in ("Int64", "Float64")]].describe().T.reset_index(names="column")
    csv(stats, reports / "numeric_summary.csv")
    for c in ["sales_gross", "item_total_net", "order_profit_per_order", "item_profit_ratio"]:
        record("4_explore", "negative_value_review", c, d[c].lt(0).sum(), "giữ; thống kê riêng", "Lợi nhuận âm có thể hợp lệ; không xóa bằng quy tắc IQR tùy tiện.")

    profiles = []
    for s in SCHEMA:
        c = s["column"]
        profiles.append({"source_column": s["source_column"], "column": c,
                         "raw_missing": int(raw[s["source_column"]].isna().sum()),
                         "raw_missing_rate": float(raw[s["source_column"]].isna().mean()),
                         "clean_missing": int(d[c].isna().sum()), "unique_nonmissing": int(d[c].nunique()),
                         "clean_dtype_before_drop": str(d[c].dtype), "treatment": s["treatment"]})
    profile = pd.DataFrame(profiles)
    csv(profile, reports / "column_profile.csv")

    to_drop = []
    for s in SCHEMA:
        if not s["treatment"].startswith("drop_"):
            continue
        c = s["column"]
        if s["treatment"] == "drop_empty" and d[c].notna().any():
            raise ValueError(f"Previously empty column now contains values: {c}")
        if s["treatment"] == "drop_constant" and d[c].nunique(dropna=False) != 1:
            raise ValueError(f"Previously constant column changed: {c}")
        to_drop.append(c)
        record("3_clean", s["treatment"], c, len(d), "loại khỏi bảng chuẩn; giữ file raw", s["description_vi"])
    d = d.drop(columns=to_drop)

    # Do not choose a convenient 'first' silently when order headers disagree.
    grouped = d.loc[d["order_id"].notna()].groupby("order_id", sort=False)
    conflicts = grouped[ORDER_FIELDS].nunique(dropna=False).gt(1)
    conflict_counts = conflicts.sum().rename_axis("column").reset_index(name="conflicting_orders")
    csv(conflict_counts, reports / "order_header_consistency.csv")
    orders = grouped[ORDER_FIELDS].first()
    for c in ORDER_FIELDS:
        orders.loc[conflicts[c], c] = pd.NA
    orders["order_header_conflict"] = conflicts.any(axis=1).astype("Int64")
    orders["line_count"] = grouped.size().astype("Int64")
    for source_col, target in [("item_quantity", "total_quantity"), ("sales_gross", "sales_gross_total"), ("item_total_net", "item_total_net_sum")]:
        result = grouped[source_col].sum(min_count=1)
        missing_or_negative = d[source_col].isna() | d[source_col].lt(0).fillna(False)
        if source_col == "item_quantity":
            missing_or_negative |= d[source_col].eq(0).fillna(False)
        bad_order_ids = d.loc[missing_or_negative, "order_id"].dropna().unique()
        result.loc[result.index.isin(bad_order_ids)] = pd.NA
        orders[target] = result
    orders["invalid_logistics_flag"] = grouped["invalid_logistics_flag"].max()
    orders["delivery_kpi_eligible"] = (
        grouped["delivery_kpi_eligible"].min().eq(1)
        & orders["order_header_conflict"].eq(0)
        & orders["invalid_logistics_flag"].eq(0)
    ).astype("Int64")
    orders = orders.reset_index()
    record("3_clean", "order_aggregation", "order_id", len(d) - len(orders), "đổi cấp dữ liệu; không gọi là xóa dòng trùng", "Kiểm tra nhất quán header trước; giữ bảng dòng hàng riêng.")
    record("3_clean", "missing_values", "all retained columns", 0, "không gán giá trị thay thế", "Cột thiếu không thiết yếu để NA; không tạo dữ liệu giả.")

    csv(d, processed / "order_items_clean.csv")
    csv(orders, processed / "orders_clean.csv")
    csv(pd.DataFrame(log), reports / "preparation_log.csv")
    csv(pd.DataFrame(relationships), reports / "duplicate_columns.csv")
    kpis = pd.DataFrame(make_kpis(d, "order_item") + make_kpis(orders, "order"))
    csv(kpis, reports / "baseline_kpis.csv")
    status_counts = d.groupby(["delivery_status", "late_delivery_risk", "is_late_from_days"], dropna=False).size().reset_index(name="line_count")
    csv(status_counts, reports / "label_consistency.csv")
    mode_rows = []
    for (mode, eligible), sub in orders.groupby(["shipping_mode", "delivery_kpi_eligible"], dropna=False):
        mode_rows.append({"shipping_mode": mode, "delivery_kpi_eligible": eligible,
                          "order_count": len(sub), "late_count": int(sub["late_delivery_risk"].sum()),
                          "late_rate": float(sub["late_delivery_risk"].mean()),
                          "mean_actual_days": float(sub["shipping_days_actual"].mean())})
    csv(pd.DataFrame(mode_rows), reports / "shipping_mode_summary.csv")
    distributions = []
    for field in ["shipping_days_actual", "shipping_days_scheduled", "delay_days", "shipping_mode", "order_region", "delivery_status"]:
        for value, count in orders[field].value_counts(dropna=False).items():
            distributions.append({"grain": "order", "field": field, "value": value, "count": int(count)})
    csv(pd.DataFrame(distributions), reports / "initial_distributions.csv")

    dictionary = pd.DataFrame(SCHEMA).merge(profile[["source_column", "raw_missing", "raw_missing_rate", "unique_nonmissing"]], on="source_column", validate="1:1")
    dictionary["definition_source"] = "Diễn giải tiếng Việt từ tên cột; đối chiếu từ điển gốc và kiểm tra dữ liệu; xem docs/01_nguon_du_lieu.md"
    dictionary.loc[dictionary["column"].eq("order_zipcode"), "definition_source"] = "Suy luận từ tên cột; chưa có mục tương ứng trong từ điển gốc tham khảo"
    csv(dictionary, ROOT / "docs/data_dictionary.csv")
    derived = pd.DataFrame(DERIVED + ORDER_AGGREGATES, columns=["column", "dtype", "measurement_scale", "unit", "role", "formula_or_rule_vi", "availability_at_prediction"])
    csv(derived, ROOT / "docs/derived_variables.csv")
    dictionary_text = "# Data Dictionary\n\nTự sinh bởi `python -m dss_bi_delivery.prepare_data`. Sửa metadata tại `src/dss_bi_delivery/schema.py`.\n\n"
    dictionary_text += "Thang đo: nominal = định danh; nominal_binary = định danh nhị phân; interval = khoảng; ratio = tỷ lệ. Không có biến thứ bậc được xác lập trong bộ này. Mã số vẫn là định danh.\n\n"
    dictionary_text += "`assumed_at_order` là giả định cần kiểm chứng, không phải lịch sử sự kiện đã được nguồn xác nhận. Đơn vị tiền tệ chưa được xác minh; không tự đổi sang VND hoặc mặc định USD.\n\n"
    dictionary_text += "## 53 trường nguồn\n\n" + markdown(dictionary[["source_column", "column", "dtype", "measurement_scale", "unit", "role", "availability_at_prediction", "treatment", "description_vi"]])
    dictionary_text += "\n\n## Biến dẫn xuất và biến tổng hợp cấp đơn\n\n" + markdown(derived) + "\n"
    dictionary_text += "\nBảng phân tích bổ sung `orders_analysis.csv` có schema và vai trò từng trường tại "
    dictionary_text += "[analysis_schema.json](analysis_schema.json), bao gồm cờ địa lý unknown và allowlist dự báo. "
    dictionary_text += "Quy tắc dùng từng bảng tại [07_du_lieu_cho_phan_tich.md](07_du_lieu_cho_phan_tich.md).\n"
    (ROOT / "docs/02_data_dictionary.md").write_text(dictionary_text, encoding="utf-8")

    summary = {
        "input_sha256": checksum, "matches_reference_source": checksum == EXPECTED_SHA256,
        "input_bytes": source.stat().st_size, "encoding": "cp1252", "raw_rows": len(raw), "raw_columns": len(raw.columns),
        "raw_exact_duplicate_rows": int(raw.duplicated().sum()), "distinct_orders": int(d["order_id"].nunique()),
        "unique_order_item_ids": int(d["order_item_id"].nunique()), "clean_item_rows": len(d), "clean_item_columns": len(d.columns),
        "clean_order_rows": len(orders), "clean_order_columns": len(orders.columns),
        "dropped_source_columns": to_drop, "imputed_cells": 0,
        "invalid_logistics_rows": int(d["invalid_logistics_flag"].sum()),
        "conflicting_orders": int(orders["order_header_conflict"].sum()),
        "canceled_line_count": int(d["is_shipping_canceled"].sum()),
        "canceled_order_count": int(orders["is_shipping_canceled"].sum()),
        "canceled_lines_with_positive_delay": int((d["is_shipping_canceled"].eq(1) & d["delay_days"].gt(0)).sum()),
        "timestamp_duration_mismatch_rows": int(d["duration_mismatch_flag"].sum()),
        "order_datetime_min": str(d["order_datetime"].min()), "order_datetime_max": str(d["order_datetime"].max()),
        "shipping_datetime_min": str(d["shipping_datetime"].min()), "shipping_datetime_max": str(d["shipping_datetime"].max()),
        "gross_sales_sum": float(d["sales_gross"].sum()), "net_item_total_sum": float(d["item_total_net"].sum()),
        "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__,
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    (reports / "quality_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = "# Báo cáo kiểm tra và làm sạch dữ liệu\n\n"
    report += "Tự sinh từ đúng file Kaggle đã ghi SHA-256; không sử dụng số liệu chép từ notebook bên ngoài.\n\n"
    report += f"- Nguồn: **{len(raw):,} dòng × {len(raw.columns)} cột**, **{len(orders):,} đơn**.\n"
    report += f"- Khóa dòng hàng duy nhất: {summary['unique_order_item_ids']:,}; dòng trùng hoàn toàn: {summary['raw_exact_duplicate_rows']}.\n"
    report += f"- Thời điểm đặt: {summary['order_datetime_min']} đến {summary['order_datetime_max']}; thời điểm shipment đến {summary['shipping_datetime_max']}.\n"
    report += f"- Bảng dòng hàng giữ {len(d):,} dòng, {len(d.columns)} cột gồm cột dẫn xuất; bảng đơn có {len(orders):,} dòng, {len(orders.columns)} cột.\n"
    report += f"- Loại {len(to_drop)} cột nguồn theo chính sách; không xóa dòng hàng; không gán giá trị thiếu.\n"
    report += f"- Dòng logistics không hợp lệ: {summary['invalid_logistics_rows']}; đơn mâu thuẫn header: {summary['conflicting_orders']}.\n\n"
    report += "## Giá trị thiếu trong nguồn\n\n" + markdown(profile.loc[profile.raw_missing.gt(0), ["source_column", "raw_missing", "raw_missing_rate", "treatment"]]) + "\n\n"
    report += "## KPI ban đầu và kiểm tra độ nhạy\n\n" + markdown(kpis.round(6)) + "\n\n"
    report += "`all_source_labels` giữ mọi nhãn gốc, gồm hủy=0. `non_canceled_valid` loại trạng thái Shipping canceled và lỗi logistics; đây là mẫu KPI phân tích mặc định. `complete_closed_sensitivity` chỉ giữ COMPLETE/CLOSED để kiểm tra ảnh hưởng của trạng thái snapshot. Không gọi mẫu non_canceled là các đơn đã giao được xác thực.\n\n"
    report += "## Phân phối sơ bộ ở cấp đơn\n\n"
    hist = orders["shipping_days_actual"].value_counts().sort_index()
    report += "Số ngày shipping thực tế (mỗi khối xấp xỉ tỷ trọng so với nhóm lớn nhất):\n\n```text\n"
    for value, count in hist.items():
        report += f"{value} ngày | {'#' * max(1, round(40 * count / hist.max()))} {count:,}\n"
    report += "```\n\n" + markdown(pd.DataFrame(mode_rows).query("delivery_kpi_eligible == 1").round(6)) + "\n\n"
    report += "## Các vấn đề cần giải thích khi báo cáo\n\n"
    report += f"1. Đơn hủy: {summary['canceled_line_count']:,} dòng / {summary['canceled_order_count']:,} đơn. Có {summary['canceled_lines_with_positive_delay']:,} dòng hủy với delay_days>0 nhưng nhãn gốc 0; giữ hai đại lượng riêng.\n"
    report += f"2. Khoảng hai timestamp khác số ngày shipping ở {summary['timestamp_duration_mismatch_rows']:,} dòng. Không sửa duration từ timestamp; xem phân phối Same Day và giả định A04.\n"
    report += "3. CP1252 giải mã nghiêm ngặt được toàn bộ file và không sinh C1 control; Latin-1 sinh 20 ký tự C1 trong địa danh. Một số địa danh đã có dấu hỏi ngay trong nguồn, chưa phục hồi được.\n"
    report += "4. Latitude/Longitude mô tả vị trí cửa hàng; không có kho xuất phát được xác thực, điểm nhận, xe, sức chở hay khung giờ. Dữ liệu này chưa đủ tối ưu tuyến.\n"
    report += "5. Cột lợi nhuận trùng nhau và ngữ nghĩa cấp dòng chưa rõ. Giữ một cột để truy nguyên; không công bố tổng lợi nhuận đơn hoặc chi phí giao trễ từ chúng.\n"
    report += "6. Số ngày kế hoạch gắn chặt Shipping Mode trong bản này; quan hệ giữa phương thức và trễ không chứng minh phương thức gây trễ.\n"
    report += "7. Không có tổng kiểm soát độc lập từ doanh nghiệp. Kiểm tra checksum, số dòng và đối chiếu nội bộ không chứng minh dữ liệu đầy đủ so với hệ thống gốc.\n\n"
    report += "## Bằng chứng và nhật ký\n\n`column_profile.csv`: 53 cột và thiếu/miền; `preparation_log.csv`: nhật ký 4 bước và số dòng ảnh hưởng; `order_header_consistency.csv`: nhất quán cấp đơn; `numeric_summary.csv`: thống kê; `initial_distributions.csv`: phân phối sơ bộ; `label_consistency.csv`: nhãn; `baseline_kpis.csv`: KPI.\n"
    (reports / "data_quality_report.md").write_text(report, encoding="utf-8")
    from .analysis_data import export_analysis

    summary["analysis_stage"] = export_analysis(orders, ROOT)
    with (reports / "data_quality_report.md").open("a", encoding="utf-8") as output:
        output.write("\n## Làm sạch bổ sung và bàn giao phân tích\n\n"
                     "Các bảng trên giữ toàn bộ nguồn để đối chiếu. Bảng dùng cho mô tả/chẩn đoán là "
                     "`data/processed/orders_analysis.csv`; dữ liệu dự báo được tách feature/label/split. "
                     "Xem [analysis_readiness_report.md](analysis_readiness_report.md) cho xử lý địa danh hỏng, "
                     "quy tắc loại mẫu, điều tra theo tháng và kiểm tra bàn giao.\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/raw/DataCoSupplyChainDataset.csv")
    parser.add_argument("--allow-source-change", action="store_true", help="Only after manually reviewing a different source version.")
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.allow_source_change), ensure_ascii=False, indent=2))
