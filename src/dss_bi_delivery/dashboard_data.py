"""Build validated, minimal Power BI inputs from the team's frozen handoffs."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
POLICIES = {
    'current': 'Hiện tại',
    'bounded_plus1_keep_same_day': 'Thêm một ngày',
    'q80_min100': 'Mục tiêu 80% đúng hẹn',
    'q90_min100': 'Mục tiêu 90% đúng hẹn',
    'q95_min100': 'Mục tiêu 95% đúng hẹn',
}


def build(root: Path = ROOT, output: Path | None = None) -> dict:
    output = output or root / 'data/dashboard'
    sources = {}
    checks = []

    def check(condition, message):
        if not condition:
            raise ValueError(message)
        checks.append(message)

    def read(path):
        source = root / path
        sources[path] = hashlib.sha256(source.read_bytes()).hexdigest()
        return pd.read_csv(source, encoding='utf-8-sig', dtype={'order_id': 'string'})

    orders = read('data/processed/orders_analysis.csv')
    splits = read('data/processed/orders_model_splits.csv')
    predictions = read('workstreams/forecasting/results/predictions_test.csv')
    check(len(orders) == 62897 and orders.order_id.is_unique, '62,897 unique analysis orders')
    check(int(orders.late_delivery_risk.sum()) == 36048, '36,048 unchanged source late labels')
    check(splits.order_id.is_unique and set(splits.order_id) == set(orders.order_id), 'Split keys match the analysis population')
    orders = orders.merge(splits[['order_id', 'partition']], on='order_id', validate='one_to_one')
    test_ids = set(orders.loc[orders.partition.eq('test'), 'order_id'])
    check(len(test_ids) == 13071 and predictions.order_id.is_unique and set(predictions.order_id) == test_ids, 'Prediction keys match exactly 13,071 test orders')
    comparison = orders.merge(predictions, on='order_id', validate='one_to_one', suffixes=('', '_prediction'))
    check((comparison.late_delivery_risk == comparison.late_delivery_risk_prediction).all(), 'Prediction labels match analysis labels')
    check(predictions.P_Late.between(0, 1).all(), 'All P_Late values are probabilities in [0,1]')
    check(predictions.groupby('shipping_mode').P_Late.nunique().eq(1).all(), 'Selected baseline has one probability per shipping mode')
    orders = orders.merge(predictions[['order_id', 'P_Late']], on='order_id', how='left', validate='one_to_one')
    orders['order_date'] = orders.order_datetime.str[:10]
    orders['year_month'] = orders.order_datetime.str[:7]
    orders['month_start'] = orders['year_month'] + '-01'
    selected = ['order_id', 'order_date', 'year_month', 'month_start', 'shipping_mode', 'market', 'order_region',
                'customer_segment', 'shipping_days_scheduled', 'shipping_days_actual', 'late_delivery_risk',
                'partition', 'P_Late', 'duration_mismatch_flag']
    orders = orders[selected]
    check(orders.loc[~orders.partition.eq('test'), 'P_Late'].isna().all(), 'P_Late is absent outside the test population')
    test = orders[orders.partition.eq('test')].copy()
    metrics = read('workstreams/forecasting/results/model_comparison.csv')
    baseline = metrics[metrics.model.eq('mode_baseline') & metrics.partition.eq('test')].iloc[0]
    alert = test.P_Late.ge(.5)
    actual = test.late_delivery_risk.eq(1)
    confusion = dict(tp=int((alert & actual).sum()), fp=int((alert & ~actual).sum()),
                     fn=int((~alert & actual).sum()), tn=int((~alert & ~actual).sum()))
    check(all(confusion[k] == int(baseline[k]) for k in confusion), 'Recomputed test confusion matrix matches TV4 at threshold 0.5')
    scenario_frames = []
    summaries = read('workstreams/prescriptive/results/promise_summary.csv')
    reference = test.set_index('order_id')
    for policy in POLICIES:
        frame = read(f'workstreams/prescriptive/results/promise_orders_{policy}.csv')
        check(frame.order_id.is_unique and set(frame.order_id) == test_ids, f'{policy}: exact test IDs')
        frame = frame.set_index('order_id').loc[reference.index].reset_index()
        check(np.array_equal(frame.shipping_days_actual, reference.shipping_days_actual), f'{policy}: actual duration unchanged')
        check(np.array_equal(frame.shipping_days_scheduled, reference.shipping_days_scheduled), f'{policy}: original promise unchanged')
        frame['late_current'] = frame.late_current.astype(int)
        frame['exceed_proposed'] = frame.exceed_proposed.astype(int)
        frame['fallback'] = frame.fallback.astype(int)
        check(np.array_equal(frame.exceed_proposed, frame.shipping_days_actual.gt(frame.proposed_days).astype(int)), f'{policy}: exceedance recomputed per order')
        check(np.array_equal(frame.late_current, reference.late_delivery_risk), f'{policy}: current late flags match source')
        expected = summaries[summaries.policy.eq(policy) & summaries.partition.eq('test')].iloc[0]
        check(math.isclose(frame.exceed_proposed.mean(), expected.proposed_exceedance_rate, abs_tol=1e-12), f'{policy}: test summary reconciles')
        frame['policy_id'] = policy
        frame['added_days'] = frame.proposed_days - frame.shipping_days_scheduled
        scenario_frames.append(frame[['order_id', 'policy_id', 'proposed_days', 'exceed_proposed', 'fallback', 'added_days']])
    scenarios = pd.concat(scenario_frames, ignore_index=True)
    check(not scenarios.duplicated(['order_id', 'policy_id']).any(), 'Scenario grain is one order per policy')
    cases = read('workstreams/prescriptive/results/routing_summary.csv')
    cases['case_id'] = cases.instance + '|' + cases.scenario + '|' + cases.method
    check(cases.case_id.is_unique, 'Routing cases have unique keys')
    case_columns = ['case_id', 'instance', 'scenario', 'method', 'max_vehicles', 'capacity', 'status', 'vehicles_used', 'distance_units']
    cases = cases[case_columns]
    stop_frames = []
    for case in cases.itertuples(index=False):
        if case.status != 'feasible':
            check(pd.isna(case.distance_units) and pd.isna(case.vehicles_used), f'{case.case_id}: missing solution stays blank, not zero')
            continue
        stops = read(f'workstreams/prescriptive/results/route_stops_{case.instance}_{case.scenario}_{case.method}.csv')
        check(len(stops) == 100 and set(stops.node) == set(range(1, 101)), f'{case.case_id}: every customer visited once')
        check(stops.service_start.between(stops.ready - 1e-8, stops.due + 1e-8).all(), f'{case.case_id}: time windows respected')
        check(stops.load.le(case.capacity).all(), f'{case.case_id}: capacity respected')
        path = f'workstreams/prescriptive/inputs/{case.instance}.txt'
        p = root/path
        sources[path] = hashlib.sha256(p.read_bytes()).hexdigest()
        nodes = {}
        for line in p.read_text().splitlines():
            values = line.split()
            if len(values) == 7 and values[0].isdigit():
                nodes[int(values[0])] = list(map(float, values[1:]))
        depot_x, depot_y = nodes[0][:2]
        distance = 0
        for vehicle, route in stops.groupby('vehicle'):
            route = route.sort_values('sequence')
            points = [(depot_x, depot_y)] + list(zip(route.x, route.y)) + [(depot_x, depot_y)]
            distance += sum(math.dist(a, b) for a,b in zip(points, points[1:]))
            coords = route[['sequence', 'node', 'x', 'y']].copy()
            coords = pd.concat([pd.DataFrame([{'sequence': 0, 'node': 0, 'x': depot_x, 'y': depot_y}]), coords,
                                pd.DataFrame([{'sequence': len(route)+1, 'node': 0, 'x': depot_x, 'y': depot_y}])], ignore_index=True)
            coords['vehicle'] = str(vehicle)
            coords['case_id'] = case.case_id
            coords['stop_key'] = coords.case_id + '|' + coords.vehicle + '|' + coords.sequence.astype(str)
            stop_frames.append(coords)
        check(math.isclose(distance, case.distance_units, rel_tol=1e-10, abs_tol=1e-7), f'{case.case_id}: full depot-to-depot distance recomputed')
    stops = pd.concat(stop_frames, ignore_index=True)
    check(stops.stop_key.is_unique, 'Route stop keys are unique, including depot returns')
    from .route_assets import route_svg

    labels = {'nearest_feasible': 'Điểm gần nhất', 'ortools': 'OR Tools'}
    cases['case_label'] = cases.apply(
        lambda row: f"{row.instance.upper()}, tải {int(row.capacity)}, tối đa {int(row.max_vehicles)} xe, {labels[row.method]}", axis=1)
    cases['route_image'] = [route_svg(stops[stops.case_id.eq(case_id)]) for case_id in cases.case_id]
    metrics['model_label'] = metrics.model.map({
        'mode_baseline': 'Theo phương thức', 'logistic_regression': 'Hồi quy logistic',
        'hist_gradient_boosting': 'Gradient boosting'})
    check(metrics.model_label.notna().all(), 'Model presentation labels map to the original models')
    check(cases.case_label.is_unique, 'Friendly route labels retain unique case identities')
    check(cases.route_image.str.len().lt(32766).all(), 'Native route maps fit the Power BI text field limit')
    policies = pd.DataFrame([{'policy_id': k, 'policy_label': v, 'sort_order': i} for i,(k,v) in enumerate(POLICIES.items())])
    tables = {'orders.csv': orders, 'promise_scenarios.csv': scenarios, 'policies.csv': policies,
              'route_cases.csv': cases, 'route_stops.csv': stops, 'model_metrics.csv': metrics}
    output.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(output/name, index=False, encoding='utf-8-sig', lineterminator='\n')
    result = {'scope': 'Dashboard input validation, not native Power BI execution', 'all_passed': True,
              'checks_passed': len(checks), 'checks': checks, 'source_sha256': sources,
              'tables': {name: {'rows': len(frame), 'columns': list(frame.columns),
                        'sha256': hashlib.sha256((output/name).read_bytes()).hexdigest()} for name,frame in tables.items()},
              'baseline_test_confusion_at_0_5': confusion,
              'test_late_rate': float(actual.mean()), 'primary_late_rate': float(orders.late_delivery_risk.mean())}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'data/dashboard')
    args = parser.parse_args()
    result = build(output=args.output)
    report = ROOT/'reports/dashboard/input_validation.json'
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"PASS: {result['checks_passed']} dashboard input checks; {len(result['tables'])} tables")


if __name__ == '__main__':
    main()
