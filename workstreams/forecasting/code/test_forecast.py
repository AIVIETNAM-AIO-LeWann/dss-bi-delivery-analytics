"""Contract tests: join identity, leakage exclusion, chronology and unseen modes."""
import unittest
import pandas as pd
import numpy as np
import os
import subprocess
import sys
from pathlib import Path

try:
    import forecast
except ImportError:
    forecast = None


class ForecastTests(unittest.TestCase):
    def setUp(self):
        if forecast is None:
            self.fail("Forecast implementation is missing")

    def fixture(self):
        x = pd.DataFrame({"order_id": ["a", "b", "c"],
                          "order_datetime": ["2016-06-01", "2017-03-01", "2017-09-01"],
                          "shipping_mode": ["A", "B", "A"]})
        y = pd.DataFrame({"order_id": ["c", "a", "b"], "late_delivery_risk": [1, 0, 1]})
        s = pd.DataFrame({"order_id": ["b", "c", "a"],
                          "order_datetime": ["2017-03-01", "2017-09-01", "2016-06-01"],
                          "partition": ["validation", "test", "train"]})
        return x, y, s

    def test_join_uses_order_id_not_row_position(self):
        x, y, s = self.fixture()
        joined = forecast.join_tables(x, y, s)
        self.assertEqual(joined.late_delivery_risk.tolist(), [0, 1, 1])
        self.assertEqual(joined.partition.tolist(), ["train", "validation", "test"])

    def test_duplicate_or_missing_ids_are_rejected(self):
        x, y, s = self.fixture()
        with self.assertRaises(ValueError):
            forecast.join_tables(x, pd.concat([y, y.iloc[:1]]), s)
        with self.assertRaises(ValueError):
            forecast.join_tables(x, y.iloc[:2], s)

    def test_timestamp_disagreement_is_rejected(self):
        x, y, s = self.fixture()
        s.loc[s.order_id.eq("a"), "order_datetime"] = "2016-06-02"
        with self.assertRaises(ValueError):
            forecast.join_tables(x, y, s)

    def test_outcomes_and_join_keys_cannot_enter_predictors(self):
        for col in ["late_delivery_risk", "shipping_days_actual", "delay_days", "delivery_status", "order_id", "order_datetime"]:
            with self.subTest(col=col), self.assertRaises(ValueError):
                forecast.assert_safe_features(["shipping_mode", col])

    def test_purged_rows_cannot_be_reassigned_to_train(self):
        x, y, s = self.fixture()
        joined = forecast.join_tables(x, y, s)
        forecast.validate_partitions(joined)
        joined.loc[joined.partition.eq("train"), "order_datetime"] = pd.Timestamp("2016-12-29")
        with self.assertRaises(ValueError):
            forecast.validate_partitions(joined)

    def test_unseen_mode_uses_train_prevalence(self):
        model = forecast.ModeBaseline().fit(pd.DataFrame({"shipping_mode": ["A", "A", "B", "B"]}), [0, 0, 1, 0])
        p = model.predict_proba(pd.DataFrame({"shipping_mode": ["A", "B", "NEW"]}))[:, 1]
        np.testing.assert_allclose(p, [0, .5, .25], atol=1e-12)

    def test_preprocessing_does_not_learn_validation_categories(self):
        train = pd.DataFrame({"shipping_mode": ["A", "A", "B", "B"], "line_count": [1, 2, 1, 2]})
        model = forecast.build_models(["shipping_mode", "line_count"])["logistic_regression"]
        model.fit(train, [0, 1, 1, 0])
        encoder = model.named_steps["preprocess"].named_transformers_["cat"].named_steps["encode"]
        before = encoder.categories_[0].tolist()
        p = model.predict_proba(pd.DataFrame({"shipping_mode": ["NEW"], "line_count": [3]}))
        self.assertEqual(before, ["A", "B"])
        self.assertEqual(encoder.categories_[0].tolist(), ["A", "B"])
        self.assertTrue(np.isfinite(p).all())

    def test_cli_baseline_can_be_loaded_in_fresh_process(self):
        # Execute the same definitions under __main__, as the documented script CLI does.
        code_dir = Path(__file__).resolve().parent
        source = (code_dir / "forecast.py").read_text(encoding="utf-8").split('if __name__ == "__main__":')[0]
        producer = source + "\nimport io, base64\nm=ModeBaseline().fit(pd.DataFrame({'shipping_mode':['A','B']}),[0,1])\nb=io.BytesIO()\njoblib.dump({'estimator':m},b)\nprint(base64.b64encode(b.getvalue()).decode())\n"
        env = dict(os.environ, PYTHONPATH=str(code_dir), PYTHONIOENCODING="utf-8")
        created = subprocess.run([sys.executable, "-c", producer], text=True, capture_output=True, env=env, check=True)
        consumer = "import io,base64,joblib,sys; import pandas as pd; m=joblib.load(io.BytesIO(base64.b64decode(sys.stdin.read())))['estimator']; assert m.predict_proba(pd.DataFrame({'shipping_mode':['A']}))[0,1] == 0"
        loaded = subprocess.run([sys.executable, "-c", consumer], input=created.stdout, text=True, capture_output=True, env=env)
        self.assertEqual(loaded.returncode, 0, loaded.stderr)


if __name__ == "__main__":
    unittest.main()
