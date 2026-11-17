"""Build the self-contained web dashboard: dashboards/web/index.html.

Reads the validated dashboard tables in data/dashboard/, aggregates them into small
cubes (a few hundred rows each) and inlines them, with the CSS and JavaScript, into one
HTML file that opens in any browser and can be hosted as a static page.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/dashboard'
WEB = ROOT / 'dashboards/web'
MODE_ORDER = ['First Class', 'Second Class', 'Same Day', 'Standard Class']


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name, encoding='utf-8-sig')


def build_data() -> dict:
    orders = read('orders.csv')
    modes = [m for m in MODE_ORDER if m in set(orders.shipping_mode)]
    markets = sorted(orders.market.unique())
    region_market = orders.groupby('order_region').market.first()
    regions = [{'name': name, 'market': markets.index(region_market[name])} for name in sorted(region_market.index)]
    region_index = {r['name']: i for i, r in enumerate(regions)}
    months = sorted(orders.month_start.unique())
    orders['mi'] = orders.shipping_mode.map(modes.index)
    orders['ki'] = orders.market.map(markets.index)
    orders['ri'] = orders.order_region.map(region_index)
    orders['ti'] = orders.month_start.map({m: i for i, m in enumerate(months)})
    orders['late'] = orders.late_delivery_risk

    # A: every order -> counts, late orders, scheduled and actual days by mode, market, region, month.
    cube_a = (orders.groupby(['mi', 'ki', 'ri', 'ti'])
              .agg(n=('late', 'size'), late=('late', 'sum'), ss=('shipping_days_scheduled', 'sum'), sa=('shipping_days_actual', 'sum'))
              .reset_index())
    # B: test partition -> counts and late orders by predicted probability.
    test = orders[orders.partition == 'test'].copy()
    test['p'] = test.P_Late.round(6)
    cube_b = test.groupby(['mi', 'ki', 'ri', 'p']).agg(n=('late', 'size'), late=('late', 'sum')).reset_index()
    # C: promise scenarios joined to the order dimensions.
    policies = read('policies.csv').sort_values('sort_order')
    policy_index = {pid: i for i, pid in enumerate(policies.policy_id)}
    scenarios = read('promise_scenarios.csv').merge(orders[['order_id', 'mi', 'ki', 'ri']], on='order_id')
    scenarios['pi'] = scenarios.policy_id.map(policy_index)
    cube_c = (scenarios.groupby(['pi', 'mi', 'ki', 'ri'])
              .agg(n=('order_id', 'size'), ex=('exceed_proposed', 'sum'), sp=('proposed_days', 'sum'),
                   sa=('added_days', 'sum'), fb=('fallback', 'sum')).reset_index())

    metrics = read('model_metrics.csv')
    metrics = metrics[metrics.partition == 'test']
    cases = read('route_cases.csv')
    stops = read('route_stops.csv')
    stops_by_case = {}
    for index, case_id in enumerate(cases.case_id):
        part = stops[stops.case_id == case_id]
        if len(part):
            stops_by_case[index] = [[int(r.vehicle), int(r.sequence), int(r.node), float(r.x), float(r.y)] for r in part.itertuples()]

    def clean(value):
        return None if pd.isna(value) else value

    return {
        'modes': modes, 'markets': markets, 'regions': regions, 'months': [m[:7] for m in months],
        'testRange': [str(test.year_month.min()), str(test.year_month.max())],
        'A': cube_a.astype(int).values.tolist(),
        'B': [[int(r.mi), int(r.ki), int(r.ri), float(r.p), int(r.n), int(r.late)] for r in cube_b.itertuples()],
        'C': cube_c.astype(int).values.tolist(),
        'policies': [{'id': r.policy_id, 'label': r.policy_label} for r in policies.itertuples()],
        'models': [{'label': r.model_label, 'auc': float(r.roc_auc), 'ap': float(r.average_precision), 'll': float(r.log_loss)}
                   for r in metrics.sort_values('log_loss', ascending=False).itertuples()],
        'cases': [{'id': r.case_id, 'instance': r.instance, 'scenario': r.scenario, 'method': r.method, 'maxv': int(r.max_vehicles),
                   'cap': int(r.capacity), 'status': r.status, 'veh': None if pd.isna(r.vehicles_used) else int(r.vehicles_used),
                   'dist': None if pd.isna(r.distance_units) else float(r.distance_units), 'label': r.case_label} for r in cases.itertuples()],
        'stops': stops_by_case,
        'thresholds': [round(0.3 + 0.05 * i, 2) for i in range(13)],
        'params': {'km': [round(0.5 + 0.1 * i, 1) for i in range(11)], 'lit': list(range(8, 15)),
                   'price': list(range(18000, 26001, 1000))},
    }


def main() -> None:
    template = (WEB / 'template.html').read_text(encoding='utf-8')
    html = (template.replace('/*STYLE*/', (WEB / 'style.css').read_text(encoding='utf-8'))
            .replace('/*APP*/', (WEB / 'app.js').read_text(encoding='utf-8'))
            .replace('/*DATA*/', json.dumps(build_data(), ensure_ascii=False, separators=(',', ':'))))
    out = WEB / 'index.html'
    out.write_text(html, encoding='utf-8', newline='\n')
    print(f'Wrote {out.relative_to(ROOT)} ({out.stat().st_size / 1024:.0f} KB)')


if __name__ == '__main__':
    main()
