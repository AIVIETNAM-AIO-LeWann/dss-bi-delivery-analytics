"""TV5: historical promise scenarios and separate Solomon routing experiments."""
from pathlib import Path
import hashlib, json, math, platform, argparse
import pandas as pd
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'inputs/dataco'
OUT = ROOT / 'results'
FIGURES = ROOT / 'figures'

def save(frame, name):
    frame.to_csv(OUT / name, index=False, encoding='utf-8-sig')

def promises():
    src = DATA/'orders_analysis.csv'
    a = pd.read_csv(src, dtype={'order_id':str})
    splits = pd.read_csv(DATA/'orders_model_splits.csv', dtype={'order_id':str})
    a = a.merge(splits[['order_id','partition']], on='order_id', validate='one_to_one')
    assert len(a)==62897 and a.order_id.is_unique
    assert (a.late_delivery_risk == (a.shipping_days_actual>a.shipping_days_scheduled)).all()
    train=a[a.partition=='train'].copy()
    policies={}; definitions=[]
    # Each target is a scenario, not a management-approved SLA.
    for target in [.80,.90,.95]:
        for minimum in [50,100,200]:
            name=f'q{int(target*100)}_min{minimum}'
            mode=train.groupby('shipping_mode').shipping_days_actual.quantile(target,interpolation='higher')
            stats=train.groupby(['shipping_mode','order_region']).shipping_days_actual.agg(['count'])
            q=train.groupby(['shipping_mode','order_region']).shipping_days_actual.quantile(target,interpolation='higher')
            days=[]; fallbacks=[]
            for row in a.itertuples():
                key=(row.shipping_mode,row.order_region)
                use_region=key in stats.index and stats.loc[key,'count']>=minimum
                days.append(int(q.loc[key] if use_region else mode.loc[row.shipping_mode]))
                fallbacks.append(not use_region)
            policies[name]=(np.array(days), np.array(fallbacks))
            definitions.append(dict(policy=name,target=target,min_train_group=minimum))
    policies['current']=(a.shipping_days_scheduled.to_numpy(),np.zeros(len(a),dtype=bool))
    # Bounded scenario keeps Same Day at zero; other modes may increase by <=1 day.
    qdays=policies['q90_min100'][0]
    limited=np.minimum(qdays,a.shipping_days_scheduled.to_numpy()+1)
    limited=np.where(a.shipping_mode.eq('Same Day'),0,limited)
    policies['bounded_plus1_keep_same_day']=(limited,np.zeros(len(a),dtype=bool))
    summaries=[]; groups=[]
    for name,(days,fallbacks) in policies.items():
        b=a.assign(proposed_days=days,fallback=fallbacks)
        b['late_current']=b.shipping_days_actual>b.shipping_days_scheduled
        b['exceed_proposed']=b.shipping_days_actual>b.proposed_days
        b['promise_change']=b.proposed_days-b.shipping_days_scheduled
        for partition in ['train','validation','test']:
            c=b[b.partition==partition]
            summaries.append(dict(policy=name,partition=partition,n=len(c),current_late_rate=c.late_current.mean(),
                proposed_exceedance_rate=c.exceed_proposed.mean(),mean_current_days=c.shipping_days_scheduled.mean(),
                mean_proposed_days=c.proposed_days.mean(),mean_actual_days=c.shipping_days_actual.mean(),
                changed_orders=int(c.promise_change.ne(0).sum()),fallback_orders=int(c.fallback.sum())))
        if name in ['current','q80_min100','q90_min100','q95_min100','bounded_plus1_keep_same_day']:
            test=b[b.partition=='test']
            for keys,c in test.groupby(['shipping_mode','order_region']):
                groups.append(dict(policy=name,shipping_mode=keys[0],order_region=keys[1],n=len(c),
                    proposed_days=int(c.proposed_days.iloc[0]),current_days=int(c.shipping_days_scheduled.iloc[0]),
                    current_late_rate=c.late_current.mean(),proposed_exceedance_rate=c.exceed_proposed.mean(),
                    fallback_orders=int(c.fallback.sum())))
            save(test[['order_id','shipping_mode','order_region','shipping_days_scheduled','shipping_days_actual',
                       'proposed_days','late_current','exceed_proposed','fallback']], f'promise_orders_{name}.csv')
    summary=pd.DataFrame(summaries)
    save(summary,'promise_summary.csv');save(pd.DataFrame(groups),'promise_by_mode_region_test.csv')
    save(pd.DataFrame(definitions),'promise_scenario_parameters.csv')
    # No winner selected on test. Separate validation screen for each target.
    screens=[]
    for d in definitions:
        row=summary[(summary.policy==d['policy'])&(summary.partition=='validation')].iloc[0]
        screens.append({**d,'validation_exceedance':row.proposed_exceedance_rate,
                        'passes_target_on_validation':bool(row.proposed_exceedance_rate<=1-d['target'])})
    save(pd.DataFrame(screens),'promise_validation_screen.csv')
    p=pd.read_csv(DATA/'predictions_test.csv',dtype={'order_id':str})
    assert len(p)==13071 and p.order_id.is_unique
    assert set(p.order_id)==set(a.loc[a.partition=='test','order_id'])
    p=p.merge(a[['order_id','shipping_mode']],on='order_id',validate='one_to_one',suffixes=('','_check'))
    risk=p.groupby('shipping_mode').agg(n=('order_id','count'),p_late=('P_Late','first'),
           distinct_scores=('P_Late','nunique'))
    save(risk.reset_index(),'risk_groups_test.csv')
    return [src,DATA/'orders_model_splits.csv',DATA/'predictions_test.csv']

def read_instance(path):
    lines=path.read_text().splitlines(); cap=None; nodes=[]
    for line in lines:
        cols=line.split()
        if len(cols)==2 and all(x.isdigit() for x in cols) and cap is None:
            vehicles,cap=map(int,cols)
        if len(cols)==7:
            try: nodes.append(list(map(int,cols)))
            except ValueError: pass
    assert len(nodes)==101 and [n[0] for n in nodes]==list(range(101))
    return np.array(nodes),vehicles,cap

def greedy(nodes, dist, k, q):
    unseen=set(range(1,len(nodes))); routes=[]
    while unseen and len(routes)<k:
        route=[]; prev=0; t=0.; load=0
        while True:
            candidates=[]
            for j in unseen:
                start=max(t+dist[prev,j],nodes[j,4])
                if load+nodes[j,3]<=q and start<=nodes[j,5]+1e-8 and start+nodes[j,6]+dist[j,0]<=nodes[0,5]+1e-8:
                    candidates.append((dist[prev,j],j,start))
            if not candidates: break
            _,j,start=min(candidates)
            route.append(j); unseen.remove(j);load+=nodes[j,3];t=start+nodes[j,6];prev=j
        if not route: break
        routes.append(route)
    return routes if not unseen else None

def verify_routes(nodes, dist, routes, k, q):
    seen=[];rows=[];total=0.
    assert len(routes)<=k
    for v,route in enumerate(routes,1):
        prev=0;t=0.;load=0;length=0.
        for seq,j in enumerate(route,1):
            assert j>0
            arrival=t+dist[prev,j];start=max(arrival,nodes[j,4]);load+=int(nodes[j,3])
            assert start<=nodes[j,5]+1e-7 and load<=q
            rows.append(dict(vehicle=v,sequence=seq,node=j,x=nodes[j,1],y=nodes[j,2],
                arrival=arrival,service_start=start,ready=nodes[j,4],due=nodes[j,5],load=load))
            length+=dist[prev,j];t=start+nodes[j,6];prev=j;seen.append(j)
        length+=dist[prev,0];assert t+dist[prev,0]<=nodes[0,5]+1e-7
        total+=length
    assert sorted(seen)==list(range(1,len(nodes)))
    return total,rows

def solve(nodes,dist,k,q,seed=None):
    manager=pywrapcp.RoutingIndexManager(len(nodes),k,0)
    model=pywrapcp.RoutingModel(manager)
    scale=1000
    # Conservative ceil of distance/time at 0.001 resolution. Never compare to BKS as identical arithmetic.
    travel=np.ceil(dist*scale-1e-9).astype(int)
    def cost(i,j):return int(travel[manager.IndexToNode(i),manager.IndexToNode(j)])
    def transit(i,j):return cost(i,j)+int(nodes[manager.IndexToNode(i),6])*scale
    c=model.RegisterTransitCallback(cost);model.SetArcCostEvaluatorOfAllVehicles(c)
    tt=model.RegisterTransitCallback(transit)
    horizon=int(nodes[0,5])*scale
    model.AddDimension(tt,horizon,horizon,True,'Time')
    time=model.GetDimensionOrDie('Time')
    for j in range(1,len(nodes)):
        time.CumulVar(manager.NodeToIndex(j)).SetRange(int(nodes[j,4])*scale,int(nodes[j,5])*scale)
    demand=model.RegisterUnaryTransitCallback(lambda i:int(nodes[manager.IndexToNode(i),3]))
    model.AddDimensionWithVehicleCapacity(demand,0,[q]*k,True,'Capacity')
    params=pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    params.local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.seconds=8
    assignment=model.ReadAssignmentFromRoutes(seed,True) if seed else None
    solution=model.SolveFromAssignmentWithParameters(assignment,params) if assignment else model.SolveWithParameters(params)
    if not solution:return None
    routes=[]
    for v in range(k):
        index=model.Start(v);route=[]
        while not model.IsEnd(index):
            n=manager.IndexToNode(index)
            if n:route.append(n)
            index=solution.Value(model.NextVar(index))
        if route:routes.append(route)
    return routes

def svg_routes(nodes,routes,name):
    colors=['#2563eb','#dc2626','#059669','#9333ea','#ea580c','#0891b2']
    def pos(n):return (40+nodes[n,1]*6,650-nodes[n,2]*6)
    bits=['<svg xmlns="http://www.w3.org/2000/svg" width="760" height="720" viewBox="0 0 760 720">',
          '<rect width="760" height="720" fill="white"/>',f'<text x="30" y="25" font-family="sans-serif" font-size="18">{name}: benchmark coordinates (not a road map)</text>']
    for v,route in enumerate(routes):
        points=' '.join(f'{pos(n)[0]},{pos(n)[1]}' for n in [0]+route+[0])
        bits.append(f'<polyline points="{points}" fill="none" stroke="{colors[v%len(colors)]}" stroke-width="1.4" opacity="0.7"/>')
    for n in range(len(nodes)):
        x,y=pos(n);bits.append(f'<circle cx="{x}" cy="{y}" r="{5 if n==0 else 2.5}" fill="{"black" if n==0 else "#334155"}"/>')
    bits.append('</svg>');(FIGURES/f'{name}.svg').write_text('\n'.join(bits))

def routing():
    summaries=[];files=[]
    for name in ['c101','r101','rc101']:
        path=ROOT/'inputs'/f'{name}.txt';files.append(path)
        nodes,k,q=read_instance(path)
        dist=np.linalg.norm(nodes[:,None,1:3]-nodes[None,:,1:3],axis=2)
        scenarios=[('base',k,q)]
        if name=='c101':scenarios += [('fleet10',10,q),('capacity160',k,160),('capacity240',k,240)]
        for scenario,k,q in scenarios:
            baseline=greedy(nodes,dist,k,q)
            candidate=solve(nodes,dist,k,q,baseline)
            for method,routes in [('nearest_feasible',baseline),('ortools',candidate)]:
                row=dict(instance=name,scenario=scenario,method=method,max_vehicles=k,capacity=q,
                         status='feasible' if routes else 'no_solution_found',vehicles_used=None,distance_units=None)
                if routes:
                    d,stops=verify_routes(nodes,dist,routes,k,q)
                    row.update(vehicles_used=len(routes),distance_units=d)
                    save(pd.DataFrame(stops),f'route_stops_{name}_{scenario}_{method}.csv')
                    (OUT/f'route_{name}_{scenario}_{method}.json').write_text(json.dumps(routes))
                    if scenario=='base':svg_routes(nodes,routes,f'{name}_{method}')
                summaries.append(row)
            print(name,scenario,[(s['method'],s['status'],s['distance_units']) for s in summaries[-2:]],flush=True)
    frame=pd.DataFrame(summaries);save(frame,'routing_summary.csv')
    # Explicitly hypothetical normalization, not current Vietnam fuel prices.
    fuel=[]
    for row in frame[frame.status=='feasible'].to_dict('records'):
        for km_per_unit in [.5,1.,2.]:
            for liters_per_100km in [8.,12.,16.]:
                for vnd_per_liter in [18000.,22000.,26000.]:
                    km=row['distance_units']*km_per_unit
                    fuel.append({**row,'km_per_unit_assumption':km_per_unit,'liters_per_100km_assumption':liters_per_100km,
                        'vnd_per_liter_assumption':vnd_per_liter,'scenario_km':km,
                        'scenario_fuel_vnd':km*liters_per_100km/100*vnd_per_liter})
    save(pd.DataFrame(fuel),'fuel_scenarios.csv')
    return files

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default='replay',help='Separate output folder; published results are not overwritten by default')
    args=parser.parse_args()
    OUT=ROOT/args.output
    OUT.mkdir(parents=True,exist_ok=True)
    FIGURES=OUT/'figures'
    FIGURES.mkdir(exist_ok=True)
    sources=promises()+routing()
    manifest={'python':platform.python_version(),'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
       'solomon_original_reference':'https://www.sintef.no/projectweb/top/vrptw/100-customers/',
       'download_mirror':'https://raw.githubusercontent.com/ashishshukla77/solomon-vrptw-optimization/main/data/solomon/{instance}.txt',
       'provenance_limit':'SINTEF ZIP returned HTTP 403. Files downloaded from mirror; byte identity with original ZIP not independently verified.',
       'routing_objective':'minimize scaled distance subject to max fleet, capacity, hard windows; no vehicle fixed cost; no global optimality claim',
       'routing_time_limit_seconds_per_run':8,'distance_time_scale':1000,'rounding':'ceil distance arcs; validate output separately using double Euclidean',
       'fuel':'all conversion/consumption/price values are illustrative scenario assumptions, not current observed prices',
       'promise':'all quantiles fit on train; report validation and test separately; service targets not approved; no causal effect claim'}
    (OUT/'run_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
    print('Done',flush=True)
