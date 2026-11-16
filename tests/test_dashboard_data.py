"""Contract checks for generated dashboard inputs, independent of Power BI."""
from pathlib import Path
import unittest
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


class DashboardContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder=ROOT/'data/dashboard'
        if not (folder/'orders.csv').exists():
            raise unittest.SkipTest('Run python -m dss_bi_delivery.dashboard_data first')
        cls.orders=pd.read_csv(folder/'orders.csv',dtype={'order_id':str})
        cls.scenarios=pd.read_csv(folder/'promise_scenarios.csv',dtype={'order_id':str})
        cls.cases=pd.read_csv(folder/'route_cases.csv')

    def test_test_only_probability_never_leaks_to_training(self):
        self.assertEqual(len(self.orders),62897)
        self.assertTrue(self.orders.loc[self.orders.partition.ne('test'),'P_Late'].isna().all())
        self.assertEqual(self.orders.P_Late.notna().sum(),13071)

    def test_threshold_boundaries_and_undefined_precision(self):
        test=self.orders[self.orders.partition.eq('test')]
        self.assertEqual(test.P_Late.ge(0).sum(),13071)
        self.assertEqual(test.P_Late.ge(.4).sum(),13071)
        self.assertEqual(test.P_Late.ge(.5).sum(),4560)
        alerts=test[test.P_Late.ge(.5)]
        self.assertEqual(alerts.late_delivery_risk.sum(),4057)
        standard=test[test.shipping_mode.eq('Standard Class')]
        self.assertEqual(standard.P_Late.ge(.5).sum(),0)

    def test_policy_filters_retain_one_row_per_test_order(self):
        test=self.orders[self.orders.partition.eq('test')]
        for policy,frame in self.scenarios.groupby('policy_id'):
            with self.subTest(policy=policy):
                self.assertEqual(len(frame),13071)
                self.assertTrue(frame.order_id.is_unique)
                self.assertEqual(set(frame.order_id),set(test.order_id))
        current=self.scenarios[self.scenarios.policy_id.eq('current')]
        self.assertEqual(int(current.exceed_proposed.sum()),7524)
        self.assertTrue(current.added_days.eq(0).all())

    def test_unsolved_routes_stay_missing_and_fuel_is_linear(self):
        missing=self.cases[self.cases.status.ne('feasible')]
        self.assertTrue(missing.distance_units.isna().all())
        self.assertTrue(missing.vehicles_used.isna().all())
        route=self.cases[self.cases.case_id.eq('c101|base|ortools')].iloc[0]
        self.assertAlmostEqual(route.distance_units,828.936866942834)
        base=route.distance_units*1*10/100*22000
        double_price=route.distance_units*1*10/100*44000
        self.assertAlmostEqual(double_price,2*base)


if __name__=='__main__':
    unittest.main()
