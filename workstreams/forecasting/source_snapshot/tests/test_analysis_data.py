"""Protect decisions where silent cleaning would corrupt labels or select the sample."""

import unittest

import numpy as np
import pandas as pd

from dss_bi_delivery.analysis_data import FEATURES, UNKNOWN, build_analysis


def order(**overrides):
    values = dict(order_id="1", order_datetime="2016-01-01 12:00:00", shipping_datetime="2016-01-03 12:00:00",
                  shipping_days_actual=2, shipping_days_scheduled=1, delivery_status="Late delivery", late_delivery_risk=1,
                  shipping_mode="First Class", market="Europe", order_region="Western Europe", order_country="France",
                  order_city="Paris", order_state="Ile-de-France", customer_segment="Consumer", payment_type="DEBIT",
                  line_count=1, total_quantity=2, invalid_logistics_flag=0, order_header_conflict=0)
    return values | overrides


class CleaningDecisions(unittest.TestCase):
    def test_damaged_location_is_not_guessed_or_row_deleted(self):
        source = pd.DataFrame([order(order_city="Bra?ov", order_state="   State   Name  ")])
        original = source.copy(deep=True)
        result = build_analysis(source)
        self.assertEqual(len(result["analysis"]), 1)
        row = result["analysis"].iloc[0]
        self.assertEqual(row.order_city, UNKNOWN)
        self.assertEqual(row.order_city_unknown_flag, 1)
        self.assertEqual(row.order_state, "State Name")
        pd.testing.assert_frame_equal(source, original)

    def test_cancellation_excluded_without_relabeling_as_bad_label(self):
        result = build_analysis(pd.DataFrame([order(delivery_status="Shipping canceled", late_delivery_risk=0)]))
        self.assertTrue(result["analysis"].empty)
        self.assertEqual(result["excluded"].iloc[0].exclusion_reasons, "shipping_canceled")

    def test_same_day_half_day_kept_in_primary_excluded_from_strict(self):
        result = build_analysis(pd.DataFrame([order(shipping_mode="Same Day", shipping_days_actual=0,
            shipping_days_scheduled=0, delivery_status="Shipping on time", late_delivery_risk=0,
            shipping_datetime="2016-01-02 00:00:00")]))
        self.assertEqual(len(result["analysis"]), 1)
        self.assertTrue(result["timestamp_consistent"].empty)
        self.assertEqual(result["labels"].iloc[0].late_delivery_risk, 0)

    def test_missing_or_infinite_quantity_quarantined(self):
        for value in [pd.NA, np.inf, -1, 0, 1.5]:
            with self.subTest(quantity=value):
                result = build_analysis(pd.DataFrame([order(total_quantity=value)]))
                self.assertTrue(result["analysis"].empty)
                self.assertIn("invalid_numeric_domain", result["excluded"].iloc[0].exclusion_reasons)

    def test_duplicate_orders_never_arbitrarily_deduplicated(self):
        result = build_analysis(pd.DataFrame([order(), order(order_city="Lyon")]))
        self.assertTrue(result["analysis"].empty)
        self.assertEqual(len(result["excluded"]), 2)

    def test_inconsistent_target_quarantined_not_rewritten(self):
        result = build_analysis(pd.DataFrame([order(late_delivery_risk=0)]))
        self.assertTrue(result["analysis"].empty)
        self.assertIn("invalid_or_inconsistent_label", result["excluded"].iloc[0].exclusion_reasons)

    def test_forecast_view_excludes_outcomes_and_boundary_is_purged(self):
        source = pd.DataFrame([order(), order(order_id="2", order_datetime="2016-12-29 12:00:00",
                                              shipping_datetime="2016-12-31 12:00:00")])
        result = build_analysis(source)
        self.assertEqual(list(result["features"].columns), ["order_id", "order_datetime", *FEATURES])
        self.assertEqual(result["splits"].set_index("order_id").loc["2", "partition"], "purged_boundary")
        self.assertNotIn("shipping_days_actual", result["features"])
        self.assertEqual(result["labels"].late_delivery_risk.tolist(), [1, 1])


if __name__ == "__main__":
    unittest.main()
