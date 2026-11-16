"""Score a supplied feature CSV with the frozen model; does not train or alter labels."""
import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from forecast import assert_safe_features, csv


def score(model_path, input_path, output_path):
    artifact = joblib.load(model_path)
    columns = artifact["feature_columns"]
    assert_safe_features(columns)
    frame = pd.read_csv(input_path, dtype={"order_id": "string"})
    if not {"order_id", "order_datetime", *columns}.issubset(frame.columns):
        raise ValueError("Input needs order_id, order_datetime and all approved feature columns")
    if frame.order_id.isna().any() or not frame.order_id.is_unique or frame[columns].isna().any().any():
        raise ValueError("Missing data or duplicate order IDs")
    result = frame[["order_id", "order_datetime"]].copy()
    result["P_Late"] = artifact["estimator"].predict_proba(frame[columns])[:, 1]
    if not (np.isfinite(result.P_Late).all() and result.P_Late.between(0, 1).all()):
        raise ValueError("Invalid model output")
    result["predicted_late_at_0_5"] = result.P_Late.ge(artifact["threshold"]).astype(int)
    result["model"] = artifact["selected_model"]
    result["prediction_context"] = "supplied_input_not_an_evaluation"
    csv(result, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    score(args.model, args.input, args.output)
