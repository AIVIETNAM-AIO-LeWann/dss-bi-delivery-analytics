"""Đối chiếu file nguồn trong repo với giá trị kỳ vọng của các con số được trích trong mục 7.1.

Chạy từ gốc repo:
    python deliverables/report/section_vii/limitations/code/verify_figures.py

Mã chỉ đọc CSV/JSON/mã nguồn có sẵn trong repo; không đọc dữ liệu thô, không huấn luyện
lại mô hình, không chạy bộ giải tuyến và không ghi vào thư mục kết quả bàn giao.
Kết quả kiểm tra được ghi vào tables/figure_checks.csv cạnh thư mục code/.
"""

import argparse
import csv
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(root, rel):
    with open(root / rel, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def one(table, **where):
    found = [r for r in table if all(r[k] == v for k, v in where.items())]
    assert len(found) == 1, (where, len(found))
    return found[0]


def vn(value, decimals=0):
    """Định dạng số kiểu Việt Nam: dấu chấm phân nghìn, dấu phẩy thập phân."""
    text = f'{value:,.{decimals}f}'
    return text.replace(',', '_').replace('.', ',').replace('_', '.')


def pct(value, decimals=2):
    return vn(100 * value, decimals) + '%'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', default='.', help='Gốc repo chung')
    parser.add_argument('--output', default=str(HERE.parent / 'tables' / 'figure_checks.csv'))
    args = parser.parse_args()
    root = Path(args.source_root).resolve()
    checks = []

    def check(key, actual, expected, source):
        checks.append({'key': key, 'value': actual, 'expected': expected,
                       'ok': actual == expected, 'source': source})

    # --- Nguồn và mẫu -------------------------------------------------------
    src = 'reports/data_quality/baseline_kpis.csv'
    kpi = rows(root, src)
    item_all = one(kpi, grain='order_item', cohort='all_source_labels')
    order_all = one(kpi, grain='order', cohort='all_source_labels')
    order_main = one(kpi, grain='order', cohort='non_canceled_valid')
    order_cc = one(kpi, grain='order', cohort='complete_closed_sensitivity')
    check('source_lines', vn(int(item_all['records_in_cohort'])), '180.519', src)
    check('source_orders', vn(int(order_all['records_in_cohort'])), '65.752', src)
    check('main_orders', vn(int(order_main['records_in_cohort'])), '62.897', src)
    check('main_late', vn(int(order_main['late_count'])), '36.048', src)
    check('main_late_rate', pct(float(order_main['late_rate'])), '57,31%', src)
    check('all_source_late_rate', pct(float(order_all['late_rate'])), '54,82%', src)
    check('complete_closed_orders', vn(int(order_cc['records_in_cohort'])), '28.965', src)
    check('complete_closed_late_rate', pct(float(order_cc['late_rate'])), '57,42%', src)

    src = 'reports/data_quality/analysis_exclusion_summary.csv'
    check('canceled_orders', vn(int(one(rows(root, src), reason='shipping_canceled')['excluded_orders'])), '2.855', src)

    src = 'reports/data_quality/label_consistency.csv'
    lab = one(rows(root, src), delivery_status='Shipping canceled', late_delivery_risk='0', is_late_from_days='1')
    check('canceled_lines_label0_daysLate', vn(int(lab['line_count'])), '4.423', src)

    src = 'reports/data_quality/analysis_sensitivity.csv'
    sens = rows(root, src)
    ts = one(sens, cohort='timestamp_consistent_only')
    primary = one(sens, cohort='primary_source_duration')
    check('timestamp_consistent_orders', vn(int(ts['orders'])), '59.490', src)
    check('same_day_orders_main', vn(int(primary['same_day_orders'])), '3.407', src)
    check('mismatch_equals_all_same_day',
          int(primary['orders']) - int(ts['orders']) == int(primary['same_day_orders']), True, src)

    # --- Mô tả ----------------------------------------------------------------
    src = 'workstreams/descriptive/tables/06_temporal_year_month.csv'
    months = rows(root, src)
    rates = [float(r['late_rate']) for r in months]
    check('months_observed', len(months), 37, src)
    check('monthly_late_rate_min', pct(min(rates), 1), '55,0%', src)
    check('monthly_late_rate_max', pct(max(rates), 1), '59,9%', src)

    src = 'workstreams/descriptive/tables/03_market_performance.csv'
    mk = [float(r['late_rate_pct']) for r in rows(root, src)]
    check('market_late_rate_range', f'{vn(min(mk), 2)}–{vn(max(mk), 2)}%', '56,55–57,68%', src)

    src = 'workstreams/descriptive/tables/02_mode_actual_days_distribution.csv'
    dist = {r['shipping_mode']: r for r in rows(root, src)}
    fc = dist['First Class']
    check('first_class_all_2_days', int(fc['count_day_2']) == int(fc['total_orders']), True, src)
    for mode, expected in [('Second Class', '2.453/2.422/2.473/2.452/2.456'),
                           ('Standard Class', '7.610/7.517/7.510/7.458/7.537')]:
        counts = [int(dist[mode][f'count_day_{d}']) for d in range(2, 7)]
        check(f'{mode}_days_2_to_6', '/'.join(vn(c) for c in counts), expected, src)
        shares = [c / int(dist[mode]['total_orders']) for c in counts]
        check(f'{mode}_share_range', f'{pct(min(shares), 1)}–{pct(max(shares), 1)}',
              {'Second Class': '19,8%–20,2%', 'Standard Class': '19,8%–20,2%'}[mode], src)
    sd = dist['Same Day']
    check('same_day_only_0_or_1_day',
          int(sd['count_day_0']) + int(sd['count_day_1']) == int(sd['total_orders']), True, src)
    max_day = max(d for d in range(7) for r in dist.values() if int(r[f'count_day_{d}']) > 0)
    check('max_actual_days', max_day, 6, src)

    src = 'workstreams/descriptive/tables/01_shipping_mode_detailed.csv'
    md = {r['shipping_mode']: r for r in rows(root, src)}
    check('scheduled_days_constant_within_mode',
          all(float(r['scheduled_std']) == 0 for r in md.values()), True, src)
    check('first_class_late_rate', md['First Class']['late_rate_pct'], '100.0', src)
    check('same_day_late_rate', md['Same Day']['late_rate_pct'], '48.37', src)

    src = 'workstreams/descriptive/tables/11_chi2_independence_tests.csv'
    chi = {r['variable']: r for r in rows(root, src)}
    check('chi2_tests_count', len(chi), 9, src)
    check('mode_cramers_v', chi['shipping_mode']['cramers_v'], '0.4807', src)
    others = [float(r['cramers_v']) for k, r in chi.items() if k != 'shipping_mode']
    check('max_v_non_mode', vn(max(others), 4), '0,0221', src)
    check('non_mode_all_p_ge_005',
          all(float(r['p_value']) >= 0.05 for k, r in chi.items() if k != 'shipping_mode'), True, src)
    check('order_month_not_tested', 'order_month' not in chi, True, src)

    for rel, pattern in [('workstreams/descriptive/BAO_CAO_MO_TA_VA_CHAN_DOAN.md', 'đều độc lập với rủi ro trễ'),
                         ('workstreams/descriptive/README.md', 'hoàn toàn độc lập với rủi ro trễ')]:
        text = (root / rel).read_text(encoding='utf-8')
        line = next((i + 1 for i, l in enumerate(text.splitlines()) if pattern in l), None)
        check(f'wording_line:{rel}', line, {'BAO_CAO': 144, 'README': 66}['BAO_CAO' if 'BAO' in rel else 'README'], rel)

    # --- Dự báo ---------------------------------------------------------------
    src = 'workstreams/forecasting/results/split_summary.csv'
    sp = {r['partition']: r for r in rows(root, src)}
    check('split_sizes', '/'.join(vn(int(sp[p]['orders'])) for p in ['train', 'validation', 'test', 'purged_boundary']),
          '39.568/9.497/13.071/761', src)
    check('test_window', f"{sp['test']['start'][:10]}..{sp['test']['end'][:10]}", '2017-07-01..2018-01-31', src)

    src = 'workstreams/forecasting/results/model_comparison.csv'
    mc = rows(root, src)
    base = one(mc, model='mode_baseline', partition='test')
    logi = one(mc, model='logistic_regression', partition='test')
    check('test_late', vn(int(base['late_count'])), '7.524', src)
    check('base_auc', vn(float(base['roc_auc']), 3), '0,746', src)
    check('base_precision', pct(float(base['precision'])), '88,97%', src)
    check('base_recall', pct(float(base['recall'])), '53,92%', src)
    check('base_tp_fp_fn', f"{vn(int(base['tp']))}/{vn(int(base['fp']))}/{vn(int(base['fn']))}", '4.057/503/3.467', src)
    check('logistic_ap_auc', f"{vn(float(logi['average_precision']), 3)}/{vn(float(logi['roc_auc']), 3)}", '0,840/0,751', src)
    src_split = 'reports/data_quality/analysis_readiness_report.md'
    readiness = (root / src_split).read_text(encoding='utf-8')
    check('two_purge_windows_before_cutoffs',
          f"{sp['validation']['start'][:10]}/{sp['test']['start'][:10]}/"
          f"{'| purged_boundary | 761 | 2016-12-25 00:02:00 | 2017-06-30 23:25:00 |' in readiness}",
          '2017-01-01/2017-07-01/True', 'workstreams/forecasting/results/split_summary.csv; ' + src_split)
    vlog = {r['model']: float(r['log_loss']) for r in mc if r['partition'] == 'validation'}
    check('val_logloss', '/'.join(vn(vlog[m], 4) for m in ['mode_baseline', 'logistic_regression', 'hist_gradient_boosting']),
          '0,5418/0,5452/0,5456', src)

    src = 'workstreams/prescriptive/results/risk_groups_test.csv'
    rg = rows(root, src)
    check('distinct_scores_per_mode', all(r['distinct_scores'] == '1' for r in rg), True, src)
    check('risk_group_count', len(rg), 4, src)

    src = 'workstreams/forecasting/results/subgroups_test.csv'
    sg = {r['group']: r for r in rows(root, src) if r['field'] == 'shipping_mode'}
    check('fn_standard', vn(int(sg['Standard Class']['fn'])), '3.073', src)
    check('fn_same_day', vn(int(sg['Same Day']['fn'])), '394', src)
    check('fn_sum', int(sg['Standard Class']['fn']) + int(sg['Same Day']['fn']), int(base['fn']), src)
    check('alerts_equal_first_plus_second',
          int(base['tp']) + int(base['fp']) == int(sg['First Class']['n']) + int(sg['Second Class']['n']), True, src)
    check('within_mode_auc_0_5', all(sg[m]['roc_auc'] == '0.5' for m in ['Same Day', 'Second Class', 'Standard Class']), True, src)

    src = 'workstreams/forecasting/results/thresholds_validation.csv'
    th = {r['threshold']: r for r in rows(root, src)}
    check('thr_0.2_0.4_alert_all', all(int(th[t]['fn']) == 0 and int(th[t]['tn']) == 0 for t in ['0.2', '0.3', '0.4']), True, src)
    check('thr_0.5_to_0.8_identical', len({(th[t]['tp'], th[t]['fp']) for t in ['0.5', '0.6', '0.7', '0.8']}), 1, src)
    check('thr_0.9_tp', vn(int(th['0.9']['tp'])), '1.429', src)

    src = 'workstreams/forecasting/results/sensitivity.csv'
    se = {r['experiment']: r for r in rows(root, src)}
    check('auc_without_first_class', vn(float(se['test_without_First_Class']['roc_auc']), 3), '0,656', src)
    check('auc_ablation_test', vn(float(se['test_without_mode_and_scheduled_days']['roc_auc']), 3), '0,499', src)
    check('auc_ablation_val', vn(float(se['validation_without_mode_and_scheduled_days']['roc_auc']), 3), '0,501', src)

    src = 'workstreams/forecasting/results/mode_baseline_train.csv'
    mb = {r['shipping_mode']: r for r in rows(root, src)}
    check('first_class_train', f"{vn(int(mb['First Class']['sum']))}/{vn(int(mb['First Class']['count']))}", '6.050/6.050', src)

    # --- Cam kết --------------------------------------------------------------
    src = 'workstreams/prescriptive/results/promise_summary.csv'
    ps = rows(root, src)
    test_actual = {round(float(r['mean_actual_days']), 4) for r in ps if r['partition'] == 'test'}
    check('test_mean_actual_constant', test_actual, {3.4968}, src)
    check('policy_count', len({r['policy'] for r in ps}), 11, src)
    b1 = one(ps, policy='bounded_plus1_keep_same_day', partition='test')
    check('plus1_test', f"{pct(float(b1['current_late_rate']))}→{pct(float(b1['proposed_exceedance_rate']))}", '57,56%→26,82%', src)
    check('plus1_days', vn(float(b1['mean_proposed_days']) - float(b1['mean_current_days']), 2), '0,94', src)
    q90 = one(ps, policy='q90_min50', partition='test')
    check('q90_test_exceed_and_days', f"{pct(float(q90['proposed_exceedance_rate']))}/{vn(float(q90['mean_proposed_days']), 2)}", '0,00%/5,12', src)
    q80v = one(ps, policy='q80_min50', partition='validation')
    q80t = one(ps, policy='q80_min50', partition='test')
    check('q80_val_test_exceed', f"{pct(float(q80v['proposed_exceedance_rate']))}/{pct(float(q80t['proposed_exceedance_rate']))}", '7,20%/5,11%', src)

    src = 'workstreams/prescriptive/results/pilot_by_mode_test.csv'
    pm = {r[list(r)[0]]: r for r in rows(root, src)}
    check('pilot_modes', sorted(pm), ['First Class', 'Same Day', 'Second Class', 'Standard Class'], src)
    check('first_class_new_promise_exceed', (pm['First Class']['proposed_days'], pm['First Class']['proposed_exceedance_count']), ('2', '0'), src)
    check('standard_test_n', vn(int(pm['Standard Class']['n'])), '7.780', src)
    q95 = one(ps, policy='q95_min50', partition='test')
    check('q95_test_exceed', pct(float(q95['proposed_exceedance_rate'])), '0,00%', src)
    check('first_class_test_p_late', one(rg, shipping_mode='First Class')['p_late'], '1.0', 'workstreams/prescriptive/results/risk_groups_test.csv')

    sec = sg['Second Class']
    check('second_class_precision', f"{vn(int(sec['tp']))}/{vn(int(sec['tp']) + int(sec['fp']))}={pct(float(sec['precision']))}",
          '2.083/2.586=80,55%', 'workstreams/forecasting/results/subgroups_test.csv')
    check('first_class_auc_undefined', sg['First Class']['roc_auc'], '', 'workstreams/forecasting/results/subgroups_test.csv')
    check('second_standard_late_rates', f"{md['Second Class']['late_rate_pct']}/{md['Standard Class']['late_rate_pct']}",
          '79.99/39.85', 'workstreams/descriptive/tables/01_shipping_mode_detailed.csv')

    src = 'workstreams/prescriptive/results/promise_by_mode_region_test.csv'
    q90days = sorted({(r['shipping_mode'], r['proposed_days']) for r in rows(root, src) if r['policy'] == 'q90_min100'})
    check('q90_days_equal_max_per_mode', q90days,
          [('First Class', '2'), ('Same Day', '1'), ('Second Class', '6'), ('Standard Class', '6')], src)
    q95days = sorted({(r['shipping_mode'], r['proposed_days']) for r in rows(root, src) if r['policy'] == 'q95_min100'})
    check('q95_days_equal_q90', q95days, q90days, src)

    src = 'workstreams/prescriptive/results/replay_validation.json'
    variations = json.loads((root / src).read_text(encoding='utf-8'))['timed_heuristic_variations']
    check('only_rc101_varied_on_replay', [v['instance'] for v in variations], ['rc101'], src)

    src = 'deliverables/report/section_vi_results_and_recommendations.md'
    sec6 = (root / src).read_text(encoding='utf-8')
    check('section_vi_pages_scope', all(s in sec6 for s in ['**02 · Rủi ro**', '**03 · Cam kết**', '`13.071` đơn tập test']), True, src)
    check('section_vi_no_independence_wording', 'hoàn toàn độc lập với rủi ro' in sec6 or 'đều độc lập với rủi ro' in sec6, False, src)

    src = 'README.md'
    check('readme_153_comparisons', '153 phép so sánh' in (root / src).read_text(encoding='utf-8'), True, src)
    src = 'workstreams/prescriptive/code/run_analysis.py'
    code_ra = (root / src).read_text(encoding='utf-8')
    check('verify_checks_capacity_window_all_customers',
          all(s in code_ra for s in ['load<=q', 'start<=nodes[j,5]', 'sorted(seen)==list(range(1,len(nodes)))']), True, src)
    check('homogeneous_fleet', '[q]*k' in code_ra, True, src)
    check('guided_local_search', 'GUIDED_LOCAL_SEARCH' in code_ra, True, src)
    src = 'reports/data_quality/analysis_readiness_report.md'
    check('first_class_37_of_37_months', '37/37' in (root / src).read_text(encoding='utf-8'), True, src)

    # --- Tuyến ----------------------------------------------------------------
    src = 'workstreams/prescriptive/results/routing_summary.csv'
    rs = rows(root, src)
    c_or = one(rs, instance='c101', scenario='base', method='ortools')
    c_nf = one(rs, instance='c101', scenario='base', method='nearest_feasible')
    check('c101_or', f"{int(float(c_or['vehicles_used']))}/{vn(float(c_or['distance_units']), 2)}", '10/828,94', src)
    check('c101_nf', f"{int(float(c_nf['vehicles_used']))}/{vn(float(c_nf['distance_units']), 2)}", '21/1.870,69', src)
    check('c101_reduction', pct(1 - float(c_or['distance_units']) / float(c_nf['distance_units'])), '55,69%', src)
    fails = sorted(f"{r['instance']}/{r['scenario']}" for r in rs if r['status'] == 'no_solution_found')
    check('nearest_failures', fails, ['c101/fleet10', 'r101/base', 'rc101/base'], src)
    c240 = one(rs, instance='c101', scenario='capacity240', method='nearest_feasible')
    check('nf_same_at_q200_q240', (c240['vehicles_used'], c240['distance_units']) == (c_nf['vehicles_used'], c_nf['distance_units']), True, src)

    src = 'workstreams/prescriptive/results/fleet_sizing_bounds.csv'
    fb = rows(root, src)
    certified = sorted(f"{r['instance']}/{r['scenario']}" for r in fb if r['minimum_fleet_certified'] == 'True')
    check('certified_configs', certified, ['c101/base', 'c101/fleet10'], src)
    gaps = {f"{r['instance']}/{r['scenario']}": f"{r['capacity_lower_bound']}–{r['feasible_vehicles_used']}" for r in fb}
    check('r101_gap', gaps['r101/base'], '8–21', src)
    check('rc101_gap', gaps['rc101/base'], '9–17', src)

    src = 'workstreams/prescriptive/results/run_manifest.json'
    man = json.loads((root / src).read_text(encoding='utf-8'))
    check('time_limit_s', man['routing_time_limit_seconds_per_run'], 8, src)
    check('no_vehicle_fixed_cost', 'no vehicle fixed cost' in man['routing_objective'], True, src)
    check('mirror_not_verified', 'not independently verified' in man['provenance_limit'], True, src)

    src = 'workstreams/prescriptive/results/replay_validation.json'
    rp = json.loads((root / src).read_text(encoding='utf-8'))['timed_heuristic_variations'][0]
    check('replay_rc101', f"{int(rp['published_vehicles'])}/{vn(rp['published_distance'], 2)}→{int(rp['replayed_vehicles'])}/{vn(rp['replayed_distance'], 2)}",
          '17/1.700,09→16/1.718,55', src)

    src = 'workstreams/prescriptive/code/run_analysis.py'
    code = (root / src).read_text(encoding='utf-8')
    check('warm_start_from_greedy', 'candidate=solve(nodes,dist,k,q,baseline)' in code, True, src)
    check('single_time_limit_8', len(re.findall(r'time_limit\.seconds=8', code)), 1, src)

    src = 'workstreams/prescriptive/results/fuel_scenarios.csv'
    fu = [r for r in rows(root, src) if r['instance'] == 'c101' and r['scenario'] == 'base' and r['method'] == 'ortools']
    vals = [float(r['scenario_fuel_vnd']) for r in fu]
    check('fuel_combos_c101_or', len(fu), 27, src)
    check('fuel_range_vnd', f'{vn(min(vals))}–{vn(max(vals))}', '596.835–6.896.755', src)
    check('fuel_ratio', vn(max(vals) / min(vals), 2), '11,56', src)

    src = 'workstreams/prescriptive/results/context_manifest.json'
    ctx = json.loads((root / src).read_text(encoding='utf-8'))
    check('kaggle_identity_verified', ctx['identity_between_kaggle_uploads_verified'], False, src)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['key', 'value', 'expected', 'ok', 'source'])
        writer.writeheader()
        for c in checks:
            writer.writerow({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, set, dict)) else v)
                             for k, v in {**c, 'value': sorted(c['value']) if isinstance(c['value'], set) else c['value'],
                                          'expected': sorted(c['expected']) if isinstance(c['expected'], set) else c['expected']}.items()})
    bad = [c for c in checks if not c['ok']]
    for c in bad:
        print('MISMATCH', c['key'], 'actual =', c['value'], 'expected =', c['expected'], '|', c['source'])
    print(f'{len(checks) - len(bad)}/{len(checks)} phép đối chiếu với nguồn đạt.')
    raise SystemExit(1 if bad else 0)


if __name__ == '__main__':
    main()
