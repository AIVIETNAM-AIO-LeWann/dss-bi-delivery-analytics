"""Create a self-contained, offline review dashboard; not a Power BI renderer."""
from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]


def build():
    folder=ROOT/'data/dashboard'
    orders=pd.read_csv(folder/'orders.csv',dtype={'order_id':str})
    scenarios=pd.read_csv(folder/'promise_scenarios.csv',dtype={'order_id':str})
    policies=pd.read_csv(folder/'policies.csv').sort_values('sort_order')
    modes=sorted(orders.shipping_mode.unique())
    markets=sorted(orders.market.unique())
    market_idx={m:i for i,m in enumerate(markets)}
    regions=sorted(orders.order_region.unique())
    months=sorted(orders.year_month.unique())
    mode_idx={m:i for i,m in enumerate(modes)}
    region_idx={m:i for i,m in enumerate(regions)}
    month_idx={m:i for i,m in enumerate(months)}
    keys=list(policies.policy_id)
    scenario_index={k:frame.set_index('order_id') for k,frame in scenarios.groupby('policy_id')}
    records=[]
    for row in orders.itertuples(index=False):
        test=row.partition=='test'
        record=[month_idx[row.year_month],mode_idx[row.shipping_mode],region_idx[row.order_region],
                market_idx[row.market],int(row.late_delivery_risk),int(row.shipping_days_scheduled),int(row.shipping_days_actual),int(test),
                float(row.P_Late) if test else None]
        if test:
            values=[]
            for key in keys:
                s=scenario_index[key].loc[row.order_id]
                values.append([int(s.proposed_days),int(s.exceed_proposed),int(s.fallback),int(s.added_days)])
            record.append(values)
        records.append(record)
    def data(name):
        return json.loads(pd.read_csv(folder/name).to_json(orient='records'))
    stops=pd.read_csv(folder/'route_stops.csv',dtype={'vehicle':str})
    payload={'markets':markets,'modes':modes,'regions':regions,'months':months,'orders':records,
             'policies':dict(zip(policies.policy_id,policies.policy_label)),
             'cases':data('route_cases.csv'),'stops':json.loads(stops.to_json(orient='records')),
             'metrics':data('model_metrics.csv')}
    template=ROOT/'dashboards/preview/index.template.html'
    html=template.read_text(encoding='utf-8').replace('__DASHBOARD_DATA__',json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    destination=ROOT/'dashboards/preview/delivery_dashboard.html'
    destination.write_text(html,encoding='utf-8',newline='\n')
    print('Built offline review dashboard:',destination)


if __name__=='__main__':
    build()
