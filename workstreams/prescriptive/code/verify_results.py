"""Read back delivered outputs and independently recompute key quantities."""
from pathlib import Path
import json, math, csv, argparse
import pandas as pd
R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--results',default='results')
args=parser.parse_args()
O=R/args.results
checks=[]
summary=pd.read_csv(O/'promise_summary.csv')
for path in O.glob('promise_orders_*.csv'):
    policy=path.stem.removeprefix('promise_orders_')
    x=pd.read_csv(path,dtype={'order_id':str})
    assert len(x)==13071 and x.order_id.is_unique
    expected=(x.shipping_days_actual>x.proposed_days).mean()
    row=summary[(summary.policy==policy)&(summary.partition=='test')].iloc[0]
    assert abs(expected-row.proposed_exceedance_rate)<1e-12
    assert abs(x.proposed_days.mean()-row.mean_proposed_days)<1e-12
    checks.append(policy+': test row count, unique keys, exceedance and promise average OK')
routing=pd.read_csv(O/'routing_summary.csv')
for row in routing.itertuples():
    if row.status!='feasible':continue
    nodes={}
    for line in (R/'inputs'/f'{row.instance}.txt').read_text().splitlines():
        parts=line.split()
        if len(parts)==7:
            try:v=list(map(int,parts));nodes[v[0]]=v
            except ValueError:pass
    path=O/f'route_{row.instance}_{row.scenario}_{row.method}.json'
    routes=json.loads(path.read_text());seen=[];total=0
    assert len(routes)<=row.max_vehicles
    for route in routes:
        t=0;load=0;prev=0
        for j in route+[0]:
            distance=math.hypot(nodes[prev][1]-nodes[j][1],nodes[prev][2]-nodes[j][2])
            total+=distance;t=max(t+distance,nodes[j][4])
            assert t<=nodes[j][5]+1e-7
            t+=nodes[j][6];load+=nodes[j][3]
            assert load<=row.capacity
            if j:seen.append(j)
            prev=j
    assert sorted(seen)==list(range(1,101))
    assert abs(total-row.distance_units)<1e-7
    checks.append(f'{path.name}: 100 customers exactly once, capacity/windows/depot/distance OK')
f=pd.read_csv(O/'fuel_scenarios.csv')
expected=f.distance_units*f.km_per_unit_assumption*f.liters_per_100km_assumption/100*f.vnd_per_liter_assumption
assert (expected-f.scenario_fuel_vnd).abs().max()<1e-6
checks.append('Fuel scenario costs recomputed OK')
bounds=pd.read_csv(O/'fleet_sizing_bounds.csv')
for b in bounds.itertuples():
    total=0
    for line in (R/'inputs'/f'{b.instance}.txt').read_text().splitlines():
        parts=line.split()
        if len(parts)==7:
            try:total+=int(parts[3])
            except ValueError:pass
    assert total==b.total_demand
    lb=math.ceil(total/b.vehicle_capacity)
    assert lb==b.capacity_lower_bound
    routing_row=routing[(routing.instance==b.instance)&(routing.scenario==b.scenario)&(routing.method=='ortools')].iloc[0]
    assert routing_row.status=='feasible'
    assert b.feasible_vehicles_used==routing_row.vehicles_used
    assert bool(b.minimum_fleet_certified)==(b.feasible_vehicles_used==lb)
    assert lb<=b.feasible_vehicles_used<=b.max_vehicles
    checks.append(f'{b.instance}/{b.scenario}: source demand, fleet bounds, certification logic OK')
(O/'verification.json').write_text(json.dumps({'passed':True,'checks':checks},ensure_ascii=False,indent=2))
print('PASS:',len(checks),'readback checks')
