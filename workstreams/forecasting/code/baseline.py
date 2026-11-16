"""Importable custom estimator, including when forecast.py runs as a CLI."""
import numpy as np
import pandas as pd


class ModeBaseline:
    """Empirical train-only P(late|shipping_mode); unseen mode -> train prevalence."""
    def fit(self, X, y):
        self.prevalence_ = float(np.mean(y))
        temp = pd.DataFrame({"shipping_mode": X.shipping_mode.to_numpy(), "y": np.asarray(y)})
        self.rates_ = temp.groupby("shipping_mode", dropna=False).y.mean().to_dict()
        return self

    def predict_proba(self, X):
        p = X.shipping_mode.map(self.rates_).fillna(self.prevalence_).to_numpy(dtype=float)
        return np.column_stack([1 - p, p])
