"""Recompute inherited facts and every promise scenario from the packaged source data."""
from pathlib import Path
import json, math, hashlib, argparse
import pandas as pd
import numpy as np

R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--results',default='results')
args=parser.parse_args()
O=R/args.results;E=R/'evidence';D=R/'inputs/dataco'
checks=[]
def check(condition, description):
    if not condition:raise AssertionError(description)
    checks.append(description)

a=pd.read_csv(D/'orders_analysis.csv',dtype={'order_id':str})
split=pd.read_csv(D/'orders_model_splits.csv',dtype={'order_id':str})
a=a.merge(split[['order_id','partition']],on='order_id',validate='one_to_one')
check(len(a)==62897 and a.order_id.is_unique,'TV2: 62,897 distinct non-canceled analysis orders')
check(a.late_delivery_risk.sum()==36048,'TV2/TV3: 36,048 source late labels')
check((a.late_delivery_risk==(a.shipping_days_actual>a.shipping_days_scheduled)).all(),'Source label agrees with duration comparison on this cohort')
check(a.partition.value_counts().to_dict()==dict(train=39568,test=13071,validation=9497,purged_boundary=761),'TV2/TV4: exact split counts, including excluded purge')
for b in pd.read_csv(E/'TV3_phuong_thuc.csv').itertuples():
    c=a[a.shipping_mode==b.shipping_mode]
    check(len(c)==b.order_count and c.late_delivery_risk.sum()==b.late_count,f'TV3 {b.shipping_mode}: order and late counts')
    check(abs(round(c.late_delivery_risk.mean()*100,2)-b.late_rate_pct)<1e-8,f'TV3 {b.shipping_mode}: rounded late percentage')
train=a[a.partition=='train'];test=a[a.partition=='test']
p=pd.read_csv(D/'predictions_test.csv',dtype={'order_id':str})
joined=test.merge(p,on='order_id',validate='one_to_one',suffixes=('','_tv4'))
check(len(joined)==13071 and set(p.order_id)==set(test.order_id),'TV4: exact test IDs match TV5 evaluation IDs')
check((joined.late_delivery_risk==joined.late_delivery_risk_tv4).all(),'TV4: per-order labels match source')
check((joined.shipping_mode==joined.shipping_mode_tv4).all(),'TV4: per-order shipping modes match source')
mean=train.groupby('shipping_mode').late_delivery_risk.mean()
check(np.allclose(joined.P_Late,joined.shipping_mode.map(mean),atol=1e-11,rtol=0),'TV4 P_Late equals train-only mode baseline')
selection=json.loads((E/'TV4_model_selection.json').read_text())
check(selection['selected_model']=='mode_baseline' and selection['selected_before_test_evaluation'],'TV4 selected baseline before test evaluation')
check(p.groupby('shipping_mode').P_Late.nunique().eq(1).all(),'TV4 has one risk score within each mode')
alert=p.P_Late>=.5;y=p.late_delivery_risk==1
check((int(alert.sum()),int((alert&y).sum()),int((alert&~y).sum()),int((~alert&y).sum()))==(4560,4057,503,3467),'TV4 threshold 0.5: 4,560 alerts, 4,057 TP, 503 FP, 3,467 FN')

def higher(values,q):
    values=sorted(values)
    return values[math.ceil(q*(len(values)-1))]

summary=pd.read_csv(O/'promise_summary.csv')
all_days={};all_fallback={}
for target in [.8,.9,.95]:
    mode={k:higher(c.shipping_days_actual.tolist(),target) for k,c in train.groupby('shipping_mode')}
    for minimum in [50,100,200]:
        name=f'q{int(target*100)}_min{minimum}'
        region={k:higher(c.shipping_days_actual.tolist(),target) for k,c in train.groupby(['shipping_mode','order_region']) if len(c)>=minimum}
        keys=list(zip(a.shipping_mode,a.order_region))
        all_days[name]=np.array([region[k] if k in region else mode[k[0]] for k in keys])
        all_fallback[name]=np.array([k not in region for k in keys])
all_days['current']=a.shipping_days_scheduled.to_numpy()
all_fallback['current']=np.zeros(len(a),dtype=bool)
all_days['bounded_plus1_keep_same_day']=np.where(a.shipping_mode.eq('Same Day'),0,np.minimum(all_days['q90_min100'],a.shipping_days_scheduled+1))
all_fallback['bounded_plus1_keep_same_day']=np.zeros(len(a),dtype=bool)
for row in summary.itertuples():
    mask=a.partition.eq(row.partition).to_numpy();c=a[mask];days=all_days[row.policy][mask]
    expected={'n':len(c),'current_late_rate':float(c.late_delivery_risk.mean()),
        'proposed_exceedance_rate':float((c.shipping_days_actual.to_numpy()>days).mean()),
        'mean_proposed_days':float(days.mean()),'mean_current_days':float(c.shipping_days_scheduled.mean()),
        'mean_actual_days':float(c.shipping_days_actual.mean()),
        'changed_orders':int((days!=c.shipping_days_scheduled).sum()),
        'fallback_orders':int(all_fallback[row.policy][mask].sum())}
    check(all(abs(float(getattr(row,k))-v)<1e-10 for k,v in expected.items()),f'{row.policy}/{row.partition}: train-only policy and all summary fields independently recomputed')
for path in O.glob('promise_orders_*.csv'):
    name=path.stem.removeprefix('promise_orders_');out=pd.read_csv(path,dtype={'order_id':str})
    expected=a.assign(expected_days=all_days[name])[a.partition=='test'][['order_id','expected_days']]
    j=out.merge(expected,on='order_id',validate='one_to_one')
    check(len(j)==13071 and j.proposed_days.eq(j.expected_days).all(),name+': every exported promise matches source train policy')
    check(j.exceed_proposed.eq(j.shipping_days_actual>j.proposed_days).all(),name+': every exported exceedance flag matches its promise')
    source=test[['order_id','shipping_mode','order_region','shipping_days_scheduled','shipping_days_actual']]
    matched=out.merge(source,on='order_id',validate='one_to_one',suffixes=('','_source'))
    check(all(matched[c].eq(matched[c+'_source']).all() for c in source.columns if c!='order_id'),name+': all exported source context and durations match original test rows')
    check(matched.late_current.eq(matched.shipping_days_actual>matched.shipping_days_scheduled).all(),name+': every current-late flag matches source duration')

# Additional decision-facing summaries are derived from the frozen submitted outputs.
bounded=pd.read_csv(O/'promise_orders_bounded_plus1_keep_same_day.csv',dtype={'order_id':str})
dashboard=bounded.merge(p[['order_id','order_datetime','P_Late','late_delivery_risk']],on='order_id',validate='one_to_one')
dashboard['scenario_id']='bounded_plus1_keep_same_day'
check(len(dashboard)==13071 and dashboard.order_id.is_unique,'TV6 handoff: 13,071 unique test rows, exact TV4 probabilities and TV5 promises')
dashboard.to_csv(O/'dashboard_orders_test.csv',index=False,encoding='utf-8-sig')
rows=[]
for mode,c in bounded.groupby('shipping_mode'):
    rows.append(dict(shipping_mode=mode,n=len(c),current_days=int(c.shipping_days_scheduled.iloc[0]),
        proposed_days=int(c.proposed_days.iloc[0]),current_late_count=int(c.late_current.sum()),
        proposed_exceedance_count=int(c.exceed_proposed.sum()),current_late_rate=c.late_current.mean(),
        proposed_exceedance_rate=c.exceed_proposed.mean()))
pd.DataFrame(rows).to_csv(O/'pilot_by_mode_test.csv',index=False,encoding='utf-8-sig')
sens=bounded.merge(test[['order_id','duration_mismatch_flag']],on='order_id',validate='one_to_one')
rows=[]
for label,c in [('all_test',sens),('timestamp_consistent_only',sens[sens.duration_mismatch_flag==0])]:
    rows.append(dict(cohort=label,n=len(c),current_late_rate=c.late_current.mean(),
        proposed_exceedance_rate=c.exceed_proposed.mean(),same_day_orders=int(c.shipping_mode.eq('Same Day').sum())))
pd.DataFrame(rows).to_csv(O/'pilot_duration_sensitivity.csv',index=False,encoding='utf-8-sig')

# Check independently exported stop schedules against routes and original node records.
routing=pd.read_csv(O/'routing_summary.csv')
for b in routing[routing.status=='feasible'].itertuples():
    nodes={}
    for line in (R/'inputs'/f'{b.instance}.txt').read_text().splitlines():
        cols=line.split()
        if len(cols)==7:
            try:v=list(map(int,cols));nodes[v[0]]=v
            except ValueError:pass
    routes=json.loads((O/f'route_{b.instance}_{b.scenario}_{b.method}.json').read_text())
    stops=pd.read_csv(O/f'route_stops_{b.instance}_{b.scenario}_{b.method}.csv')
    check(len(stops)==100 and stops.node.is_unique,f'{b.instance}/{b.scenario}/{b.method}: exported stops cover all 100 customers')
    for vehicle,route in enumerate(routes,1):
        prev=0;t=0.;load=0
        c=stops[stops.vehicle==vehicle].sort_values('sequence')
        check(c.node.tolist()==route,f'{b.instance}/{b.scenario}/{b.method}/vehicle{vehicle}: stop sequence matches route')
        for j,s in zip(route,c.itertuples()):
            arrival=t+math.hypot(nodes[prev][1]-nodes[j][1],nodes[prev][2]-nodes[j][2])
            start=max(arrival,nodes[j][4]);load+=nodes[j][3]
            assert abs(s.arrival-arrival)<1e-7 and abs(s.service_start-start)<1e-7 and s.load==load
            assert s.x==nodes[j][1] and s.y==nodes[j][2] and s.ready==nodes[j][4] and s.due==nodes[j][5]
            t=start+nodes[j][6];prev=j
    checks.append(f'{b.instance}/{b.scenario}/{b.method}: every stop time, coordinate and load independently recomputed')

(O/'handoff_audit.json').write_text(json.dumps({'passed':True,'check_count':len(checks),'checks':checks},ensure_ascii=False,indent=2))
print('PASS:',len(checks),'source/decision/stop-schedule checks')
