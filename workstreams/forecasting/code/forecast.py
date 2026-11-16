"""Reproducible order-level DataCo forecast. Run --help for input/output paths."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path
from datetime import datetime, timezone

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, brier_score_loss,
                             confusion_matrix, f1_score, log_loss, precision_score,
                             recall_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from threadpoolctl import threadpool_limits
from baseline import ModeBaseline

COMMIT = "6fd157327b8fc05d6011e71659db86048dead818"
SEED = 42
CAT = ["shipping_mode", "market", "order_region", "order_country", "customer_segment", "payment_type"]
ALLOWLIST = ["order_year", "order_month", "order_weekday", "order_is_weekend",
             "shipping_days_scheduled", "shipping_mode", "market", "order_region",
             "order_country", "customer_segment", "payment_type", "line_count", "total_quantity"]


def csv(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig", float_format="%.12g", date_format="%Y-%m-%d %H:%M:%S")


def write_json(value, path):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def assert_safe_features(columns):
    if not columns or len(columns) != len(set(columns)) or not set(columns).issubset(ALLOWLIST):
        raise ValueError("Predictors must be a nonempty unique subset of the approved pre-order allowlist")


def join_tables(x, y, splits):
    for name, table in [("features", x), ("labels", y), ("splits", splits)]:
        if table.order_id.isna().any() or not table.order_id.is_unique:
            raise ValueError(f"{name}: missing or duplicate order_id")
        if set(table.order_id) != set(x.order_id):
            raise ValueError(f"{name}: order IDs differ")
    result = x.merge(y, on="order_id", validate="one_to_one", sort=False)
    result = result.merge(splits.rename(columns={"order_datetime": "split_datetime"}), on="order_id", validate="one_to_one", sort=False)
    result["order_datetime"] = pd.to_datetime(result.order_datetime, errors="raise")
    if result.order_datetime.isna().any() or not result.order_datetime.eq(pd.to_datetime(result.split_datetime, errors="raise")).all():
        raise ValueError("Feature/split timestamps disagree or are missing")
    result = result.drop(columns="split_datetime")
    if result.late_delivery_risk.isna().any() or not result.late_delivery_risk.isin([0, 1]).all():
        raise ValueError("Target must contain only source labels 0 and 1")
    return result


def validate_partitions(d):
    if not set(d.partition).issubset({"train", "validation", "test", "purged_boundary"}):
        raise ValueError("Unexpected partition")
    ranges = []
    for name in ["train", "validation", "test"]:
        t = d.loc[d.partition.eq(name), "order_datetime"]
        if t.empty or t.isna().any():
            raise ValueError(f"{name} empty or missing timestamps")
        ranges.append((t.min(), t.max()))
    if not (ranges[0][1] < pd.Timestamp("2016-12-25")
            and ranges[1][0] >= pd.Timestamp("2017-01-01")
            and ranges[1][1] < pd.Timestamp("2017-06-24")
            and ranges[2][0] >= pd.Timestamp("2017-07-01")):
        raise ValueError("Time split or seven-day purge violated")


def build_models(columns):
    assert_safe_features(columns)
    cat = [c for c in CAT if c in columns]
    num = [c for c in columns if c not in cat]
    logistic_pre = ColumnTransformer([
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OneHotEncoder(handle_unknown="ignore"))]), cat),
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), num),
    ])
    boost_pre = ColumnTransformer([
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))]), cat),
        ("num", SimpleImputer(strategy="median"), num),
    ], sparse_threshold=0)
    return {
        "logistic_regression": Pipeline([("preprocess", logistic_pre), ("model", LogisticRegression(C=1, max_iter=2000, solver="lbfgs", random_state=SEED))]),
        "hist_gradient_boosting": Pipeline([("preprocess", boost_pre), ("model", HistGradientBoostingClassifier(
            learning_rate=.07, max_iter=150, max_leaf_nodes=15, min_samples_leaf=100,
            l2_regularization=10, early_stopping=False, categorical_features=list(range(len(cat))), random_state=SEED))]),
    }


def probabilities(model, X):
    p = model.predict_proba(X)[:, 1]
    if not (np.isfinite(p).all() and ((p >= 0) & (p <= 1)).all()):
        raise ValueError("Invalid probabilities")
    return p


def metrics(y, p, threshold=.5):
    y = np.asarray(y, dtype=int)
    pred = (np.asarray(p) >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {"n": len(y), "late_count": int(y.sum()), "late_rate": float(y.mean()),
            "roc_auc": float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None,
            "average_precision": float(average_precision_score(y, p)),
            "log_loss": float(log_loss(y, p, labels=[0, 1])), "brier": float(brier_score_loss(y, p)),
            "accuracy": float(accuracy_score(y, pred)), "precision": float(precision_score(y, pred, zero_division=0)),
            "recall": float(recall_score(y, pred, zero_division=0)), "f1": float(f1_score(y, pred, zero_division=0)),
            "threshold": threshold, "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)}


def calibration(y, p):
    temp = pd.DataFrame({"y": np.asarray(y), "p": p})
    temp["bin"] = pd.cut(temp.p, np.linspace(0, 1, 11), include_lowest=True)
    result = temp.groupby("bin", observed=True).agg(n=("y", "size"), mean_probability=("p", "mean"), late_rate=("y", "mean")).reset_index()
    result["bin"] = result.bin.astype(str)
    return result


def run(source_root, output):
    source_root, output = Path(source_root), Path(output)
    for folder in [output, output / "results", output / "figures", output / "models", output / "inputs", output / "provenance"]:
        folder.mkdir(parents=True, exist_ok=True)
    data = source_root / "data/processed"
    schema = json.loads((source_root / "docs/analysis_schema.json").read_text(encoding="utf-8"))
    columns = schema["model_feature_columns"]
    if columns != ALLOWLIST:
        raise ValueError("Upstream allowlist changed; review before fitting")
    assert_safe_features(columns)
    frames = [pd.read_csv(data / f"orders_model_{name}.csv", dtype={"order_id": "string"}) for name in ["features", "labels", "splits"]]
    if list(frames[0].columns) != ["order_id", "order_datetime", *columns]:
        raise ValueError("Feature input is not the exact approved schema")
    d = join_tables(*frames)
    validate_partitions(d)
    if d[columns].isna().any().any():
        raise ValueError("Prepared source unexpectedly contains missing candidate features")
    parts = {p: d.loc[d.partition.eq(p)].copy() for p in ["train", "validation", "test"]}
    tr, va, te = (parts[p] for p in ["train", "validation", "test"])
    models = {"mode_baseline": ModeBaseline(), **build_models(columns)}
    scores = []
    probs = {}
    for name, model in models.items():
        print(f"Fitting {name} on {len(tr):,} orders", flush=True)
        model.fit(tr[columns], tr.late_delivery_risk)
        p = probabilities(model, va[columns])
        probs[(name, "validation")] = p
        scores.append({"model": name, "partition": "validation", **metrics(va.late_delivery_risk, p)})
    # Freeze the winner before reading any test score. Ties prefer the earlier, simpler model.
    selected = min(scores, key=lambda row: row["log_loss"])["model"]
    selection = {"selected_model": selected, "criterion": "minimum validation log_loss; exact ties prefer earlier simpler model",
                 "threshold": .5, "refit_after_selection": False,
                 "selected_before_test_evaluation": True,
                 "candidate_parameters": {n: str(m) for n, m in models.items()}}
    write_json(selection, output / "results/model_selection.json")
    print(f"Selected from validation only: {selected}", flush=True)
    for name, model in models.items():
        p = probabilities(model, te[columns])
        probs[(name, "test")] = p
        scores.append({"model": name, "partition": "test", **metrics(te.late_delivery_risk, p)})
    score_table = pd.DataFrame(scores)
    csv(score_table, output / "results/model_comparison.csv")
    selected_model = models[selected]
    p_test = probs[(selected, "test")]
    p_val = probs[(selected, "validation")]
    test_export = te[["order_id", "order_datetime", "partition", "shipping_mode", "order_region", "order_country", "late_delivery_risk"]].copy()
    test_export["P_Late"] = p_test
    test_export["predicted_late_at_0_5"] = (p_test >= .5).astype(int)
    test_export["model"] = selected
    test_export["prediction_context"] = "untouched_test"
    for name in models:
        test_export[f"P_{name}"] = probs[(name, "test")]
    csv(test_export, output / "results/predictions_test.csv")
    all_export = []
    contexts = {"train": "in_sample_not_for_evaluation", "validation": "used_for_model_selection", "test": "untouched_test"}
    for part, sub in parts.items():
        table = sub[["order_id", "order_datetime", "partition", "shipping_mode", "order_region", "late_delivery_risk"]].copy()
        table["P_Late"] = probabilities(selected_model, sub[columns])
        table["model"] = selected
        table["prediction_context"] = contexts[part]
        all_export.append(table)
    csv(pd.concat(all_export, ignore_index=True), output / "results/predictions_by_partition.csv")
    csv(pd.DataFrame([{"partition": p, "orders": len(sub), "start": sub.order_datetime.min(), "end": sub.order_datetime.max(),
                       "late_count": int(sub.late_delivery_risk.sum()), "late_rate": sub.late_delivery_risk.mean()} for p, sub in parts.items()]
                     + [{"partition": "purged_boundary", "orders": int(d.partition.eq("purged_boundary").sum()), "start": None, "end": None,
                         "late_count": None, "late_rate": None}]), output / "results/split_summary.csv")
    csv(pd.DataFrame([{"threshold": float(t), **metrics(va.late_delivery_risk, p_val, float(t))} for t in [.2, .3, .4, .5, .6, .7, .8, .9]]), output / "results/thresholds_validation.csv")
    cal = calibration(te.late_delivery_risk, p_test)
    csv(cal, output / "results/calibration_test.csv")
    subgroup = []
    for col in ["shipping_mode", "order_region"]:
        for group, sub in test_export.groupby(col, observed=True):
            subgroup.append({"field": col, "group": group, **metrics(sub.late_delivery_risk, sub.P_Late)})
    csv(pd.DataFrame(subgroup), output / "results/subgroups_test.csv")
    monthly = []
    for month, sub in test_export.groupby(test_export.order_datetime.dt.to_period("M")):
        monthly.append({"month": str(month), **metrics(sub.late_delivery_risk, sub.P_Late)})
    csv(pd.DataFrame(monthly), output / "results/monthly_test.csv")
    # Sensitivity experiments are reported separately and never change the frozen winner.
    analysis = pd.read_csv(data / "orders_analysis.csv", dtype={"order_id": "string"})
    sensitivity = []
    for name, mask in [("test_without_First_Class", te.shipping_mode.ne("First Class").to_numpy()),
                       ("test_timestamp_consistent", te.order_id.isin(analysis.loc[analysis.duration_mismatch_flag.eq(0), "order_id"]).to_numpy())]:
        sensitivity.append({"experiment": name, "model": selected, **metrics(te.late_delivery_risk.to_numpy()[mask], p_test[mask])})
    reduced = [c for c in columns if c not in ["shipping_mode", "shipping_days_scheduled"]]
    ablation = build_models(reduced)["logistic_regression"]
    ablation.fit(tr[reduced], tr.late_delivery_risk)
    for part in ["validation", "test"]:
        sub = parts[part]
        sensitivity.append({"experiment": f"{part}_without_mode_and_scheduled_days", "model": "logistic_regression_ablation",
                            **metrics(sub.late_delivery_risk, probabilities(ablation, sub[reduced]))})
    csv(pd.DataFrame(sensitivity), output / "results/sensitivity.csv")
    rng = np.random.default_rng(SEED)
    base_loss = log_loss(va.late_delivery_risk, p_val)
    importance = []
    for col in columns:
        changes = []
        for _ in range(3):
            permuted = va[columns].copy()
            permuted[col] = rng.permutation(permuted[col].to_numpy())
            changes.append(log_loss(va.late_delivery_risk, probabilities(selected_model, permuted)) - base_loss)
        importance.append({"feature": col, "validation_log_loss_increase": float(np.mean(changes)), "repeat_std": float(np.std(changes))})
    csv(pd.DataFrame(importance).sort_values("validation_log_loss_increase", ascending=False), output / "results/permutation_importance_validation.csv")
    mode_table = tr.groupby("shipping_mode").late_delivery_risk.agg(["count", "sum", "mean"]).reset_index()
    csv(mode_table, output / "results/mode_baseline_train.csv")
    artifact = {"estimator": selected_model, "feature_columns": columns, "threshold": .5, "selected_model": selected,
                "train_end": str(tr.order_datetime.max()), "scope": schema["forecast_scope"], "upstream_commit": COMMIT}
    joblib.dump(artifact, output / "models/selected_model.joblib")
    saved = joblib.load(output / "models/selected_model.joblib")
    np.testing.assert_allclose(probabilities(saved["estimator"], te[columns]), p_test, rtol=0, atol=1e-14)
    # Copy the small modeling inputs, never personal raw fields, into the handoff.
    import shutil
    for name in ["orders_model_features.csv", "orders_model_labels.csv", "orders_model_splits.csv"]:
        shutil.copyfile(data / name, output / "inputs" / name)
    shutil.copyfile(source_root / "docs/analysis_schema.json", output / "inputs/analysis_schema.json")
    for name in ["source_manifest.json", "07_du_lieu_cho_phan_tich.md"]:
        shutil.copyfile(source_root / "docs" / name, output / "provenance" / name)
    for name in ["validation_results.json", "analysis_validation.json", "analysis_summary.json"]:
        shutil.copyfile(source_root / "reports" / name, output / "provenance" / name)
    manifest = {"run_utc": datetime.now(timezone.utc).isoformat(), "upstream_commit": COMMIT,
                "source_sha256": json.loads((source_root / "docs/source_manifest.json").read_text())["csv_sha256"],
                "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__, "sklearn": sklearn.__version__,
                "random_state": SEED, "feature_columns": columns, "selected_model": selected, "selection": selection,
                "partition_counts": {k: int(v) for k, v in d.partition.value_counts().items()},
                "test_metrics": metrics(te.late_delivery_risk, p_test),
                "majority_baseline_test_accuracy": float(max(te.late_delivery_risk.mean(), 1-te.late_delivery_risk.mean())),
                "input_sha256": {p.name: sha(p) for p in (output / "inputs").iterdir()},
                "purged_rows_fitted_or_scored": 0, "model_reload_matches": True,
                "business_scope": schema["forecast_scope"]}
    write_json(manifest, output / "results/run_manifest.json")
    from figures import build_figures
    build_figures(output, models, probs, parts, selected, cal)
    print(json.dumps({"selected_model": selected, "test_metrics": manifest["test_metrics"]}, indent=2), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True, help="Pinned upstream repo after prepare_data and verify_data")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with threadpool_limits(limits=2):
        run(args.source_root, args.output)
