"""Independent readback of exported results and the saved model in a fresh process."""
import json
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score, log_loss, brier_score_loss, confusion_matrix

root = Path(sys.argv[1])
m = json.loads((root / "results/run_manifest.json").read_text(encoding="utf-8"))
p = pd.read_csv(root / "results/predictions_test.csv", dtype={"order_id": "string"})
all_p = pd.read_csv(root / "results/predictions_by_partition.csv", dtype={"order_id": "string"})
x = pd.read_csv(root / "inputs/orders_model_features.csv", dtype={"order_id": "string"})
y = pd.read_csv(root / "inputs/orders_model_labels.csv", dtype={"order_id": "string"})
s = pd.read_csv(root / "inputs/orders_model_splits.csv", dtype={"order_id": "string"})
checks = {}
checks["test_unique_exact_ids"] = p.order_id.is_unique and set(p.order_id) == set(s.loc[s.partition.eq("test"), "order_id"])
checks["all_export_ids_exclude_purged"] = all_p.order_id.is_unique and set(all_p.order_id) == set(s.loc[s.partition.ne("purged_boundary"), "order_id"])
checks["test_context_correct"] = p.partition.eq("test").all() and p.prediction_context.eq("untouched_test").all()
joined = p.merge(y, on="order_id", validate="one_to_one", suffixes=("", "_source"))
checks["exported_labels_unchanged"] = joined.late_delivery_risk.eq(joined.late_delivery_risk_source).all()
checks["finite_valid_probabilities"] = np.isfinite(p.P_Late).all() and p.P_Late.between(0, 1).all()
checks["predicted_class_matches_threshold"] = p.predicted_late_at_0_5.eq(p.P_Late.ge(.5).astype(int)).all()
independent = {"roc_auc": roc_auc_score(p.late_delivery_risk, p.P_Late), "average_precision": average_precision_score(p.late_delivery_risk, p.P_Late),
               "log_loss": log_loss(p.late_delivery_risk, p.P_Late), "brier": brier_score_loss(p.late_delivery_risk, p.P_Late)}
checks["metrics_recomputed_from_csv"] = all(abs(value - m["test_metrics"][key]) < 1e-10 for key, value in independent.items())
tn, fp, fn, tp = confusion_matrix(p.late_delivery_risk, p.predicted_late_at_0_5, labels=[0, 1]).ravel()
checks["confusion_counts_reconcile"] = [int(tn), int(fp), int(fn), int(tp)] == [m["test_metrics"][k] for k in ["tn", "fp", "fn", "tp"]]
comparison = pd.read_csv(root / "results/model_comparison.csv")
winner = comparison.loc[comparison.partition.eq("validation")].sort_values("log_loss", kind="stable").iloc[0].model
checks["selected_by_validation_logloss"] = winner == m["selected_model"]
artifact = joblib.load(root / "models/selected_model.joblib")
test_x = p[["order_id"]].merge(x, on="order_id", validate="one_to_one", sort=False)
restored_p = artifact["estimator"].predict_proba(test_x[artifact["feature_columns"]])[:, 1]
checks["fresh_process_model_load_and_predictions"] = np.allclose(restored_p, p.P_Late, rtol=0, atol=1e-10)
for name in ["validation_results", "analysis_validation"]:
    upstream = json.loads((root / f"provenance/{name}.json").read_text(encoding="utf-8"))
    checks[f"upstream_{name}"] = bool(upstream["all_passed"])
result = {"checks": {k: bool(v) for k, v in checks.items()}, "passed": int(sum(checks.values())), "total": len(checks), "all_passed": bool(all(checks.values()))}
(root / "results/output_verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
if not result["all_passed"]:
    raise SystemExit(1)
