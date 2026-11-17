"""Check that the web dashboard's in-browser aggregates equal pandas on the raw CSVs.

Builds dashboards/web/index.html, injects a test script, runs it in headless Edge or Chrome
and fails if any aggregate differs. Usage: python scripts/check_dashboard_web.py [browser.exe]
"""
from __future__ import annotations

import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_dashboard_web  # noqa: E402

BROWSERS = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'msedge', 'google-chrome', 'chromium']


def expected_cases():
    data = ROOT / 'data/dashboard'
    orders = pd.read_csv(data / 'orders.csv', encoding='utf-8-sig')
    policies = pd.read_csv(data / 'policies.csv', encoding='utf-8-sig').sort_values('sort_order')
    scenarios = pd.read_csv(data / 'promise_scenarios.csv', encoding='utf-8-sig').merge(
        orders[['order_id', 'shipping_mode', 'market', 'order_region']], on='order_id')
    test = orders[orders.partition == 'test']
    rng = random.Random(7)
    modes, markets, regions = sorted(orders.shipping_mode.unique()), sorted(orders.market.unique()), sorted(orders.order_region.unique())
    combos = [(None, None, None), ('First Class', None, None), (None, 'Europe', None), ('Standard Class', 'LATAM', None), (None, None, regions[0])]
    combos += [(rng.choice(modes + [None]), rng.choice(markets + [None]), rng.choice(regions + [None])) for _ in range(12)]

    def mask(frame, mode, market, region):
        keep = pd.Series(True, index=frame.index)
        if mode: keep &= frame.shipping_mode.eq(mode)
        if market: keep &= frame.market.eq(market)
        if region: keep &= frame.order_region.eq(region)
        return keep

    cases = []
    for mode, market, region in combos:
        a = orders[mask(orders, mode, market, region)]
        item = {'f': [mode, market, region], 'A': [int(len(a)), int(a.late_delivery_risk.sum()), int(a.shipping_days_scheduled.sum()), int(a.shipping_days_actual.sum())]}
        t = test[mask(test, mode, market, region)]
        item['B'] = {}
        for thr in (0.4, 0.5, 0.8):
            alerts = t[t.P_Late >= thr - 1e-9]
            item['B'][str(thr)] = [int(len(t)), int(t.late_delivery_risk.sum()), int(len(alerts)), int(alerts.late_delivery_risk.sum())]
        s = scenarios[mask(scenarios, mode, market, region)]
        item['C'] = {}
        for pid in policies.policy_id:
            x = s[s.policy_id == pid]
            item['C'][pid] = [int(len(x)), int(x.exceed_proposed.sum()), int(x.proposed_days.sum()), int(x.added_days.sum()), int(x.fallback.sum())]
        cases.append(item)
    return cases


TEST_JS = r'''<script>
(function(){
  const api=window.__api,D=api.D,cases=%CASES%;let bad=[],checked=0;
  const idx=(list,v)=>v==null?null:list.indexOf(v), ridx=v=>v==null?null:D.regions.findIndex(r=>r.name===v);
  const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  for(const c of cases){
    const f={m:idx(D.modes,c.f[0]),k:idx(D.markets,c.f[1]),r:ridx(c.f[2])},a=api.aggA(f);
    if(!same([a.n,a.late,a.ss,a.sa],c.A))bad.push(['A',c.f,[a.n,a.late,a.ss,a.sa],c.A]);checked++;
    for(const thr of Object.keys(c.B)){const b=api.aggB(f,parseFloat(thr));if(!same([b.n,b.late,b.alerts,b.tp],c.B[thr]))bad.push(['B',c.f,thr,[b.n,b.late,b.alerts,b.tp],c.B[thr]]);checked++;}
    D.policies.forEach((p,i)=>{const q=api.aggC(f,i);if(!same([q.n,q.ex,q.sp,q.sa,q.fb],c.C[p.id]))bad.push(['C',c.f,p.id,[q.n,q.ex,q.sp,q.sa,q.fb],c.C[p.id]]);checked++;});
  }
  // every page must render without throwing under a filter
  let errors=[];
  for(const page of ['p1','p2','p3','p4']){try{api.S.mode='Second Class';api.S.market='Europe';api.showPage(page);}catch(e){errors.push(page+': '+e.message);}}
  try{api.S.mode=null;api.S.market=null;api.S.region=null;api.S.cas='r101|base|nearest_feasible';api.showPage('p4');}catch(e){errors.push('infeasible case: '+e.message);}
  document.title='RESULT '+JSON.stringify({checked:checked,bad:bad.slice(0,5),badCount:bad.length,errors:errors});
})();
</script></body>'''


def main() -> int:
    build_dashboard_web.main()
    html = (ROOT / 'dashboards/web/index.html').read_text(encoding='utf-8')
    test = html.replace('</body>', TEST_JS.replace('%CASES%', json.dumps(expected_cases())), 1)
    browser = sys.argv[1] if len(sys.argv) > 1 else next((b for b in BROWSERS if shutil.which(b) or Path(b).exists()), None)
    if not browser:
        print('No Edge/Chrome found; pass the browser path as an argument.')
        return 2
    with tempfile.TemporaryDirectory() as folder:
        page = Path(folder) / 'test.html'
        page.write_text(test, encoding='utf-8')
        out = subprocess.run([browser, '--headless', '--disable-gpu', '--force-prefers-reduced-motion', '--virtual-time-budget=6000',
                              '--dump-dom', page.as_uri()], capture_output=True, text=True, encoding='utf-8', timeout=180).stdout
    match = re.search(r'<title>RESULT (.*?)</title>', out, re.S)
    if not match:
        print('Test did not finish; the page may have a script error.')
        return 1
    result = json.loads(match.group(1).replace('&quot;', '"').replace('&amp;', '&'))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result['badCount'] == 0 and not result['errors'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
