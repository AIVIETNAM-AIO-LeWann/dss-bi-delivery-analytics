"""
Pipeline Thong ke Mo ta & Chan doan - Hoang Quan (TV3).
Chi tap trung dung phan viec duoc giao theo bang phan cong:
1. Phan tich tre giao hang (Late delivery risk) tong the va theo cac nhom don hang.
2. Xac dinh cac yeu to/nhom co lien he voi rui ro tre (Kiem dinh Chi-binh phuong & Cramer's V).
3. Thuc hien cac phep phan tich thong ke phu hop (mo ta tan so, ty le, trung binh, phan phoi thuc te).
4. Rut ra cac nhom rui ro dang chu y.
TUYET DOI KHONG SUY LUAN, KHONG DUA RA DE XUAT, KHONG DUA RA GIA THUYET HAY MO HINH DU BAO.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
TABLES_DIR = ROOT / "tables"
FIGURES_DIR = ROOT / "figures"

TABLES_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

ORDERS_PATH = REPO_ROOT / "data/processed/orders_analysis.csv"
ORDERS_CLEAN_PATH = REPO_ROOT / "data/processed/orders_clean.csv"
ITEMS_PATH = REPO_ROOT / "data/processed/order_items_clean.csv"

def cramers_v(contingency_table):
    chi2 = stats.chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    r, k = contingency_table.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))

def run():
    print(">>> 1. Doc du lieu thuc te tu data/processed/...", flush=True)
    orders = pd.read_csv(ORDERS_PATH)
    orders_all = pd.read_csv(ORDERS_CLEAN_PATH)
    items = pd.read_csv(ITEMS_PATH, usecols=['order_id', 'category_name', 'department_name', 'late_delivery_risk', 'item_total_net'])

    N_ORDERS = len(orders)
    N_LATE = int(orders['late_delivery_risk'].sum())
    LATE_RATE = N_LATE / N_ORDERS
    print(f"    - Tong don hop le: {N_ORDERS}, Tong don tre: {N_LATE} ({LATE_RATE*100:.2f}%)", flush=True)

    # -------------------------------------------------------------------------
    # TAB 00: Overview & Sensitivity KPIs
    # -------------------------------------------------------------------------
    cohorts = [
        {
            "cohort_name": "primary_analysis_cohort",
            "source_file": "orders_analysis.csv",
            "description": "Mau phan tich chinh (da loai 2.855 don huy)",
            "total_orders": N_ORDERS,
            "late_orders": N_LATE,
            "late_rate_pct": round(LATE_RATE * 100, 2),
            "scheduled_mean": round(orders['shipping_days_scheduled'].mean(), 2),
            "actual_mean": round(orders['shipping_days_actual'].mean(), 2),
            "actual_std": round(orders['shipping_days_actual'].std(), 2),
            "delay_mean": round(orders['delay_days'].mean(), 2)
        },
        {
            "cohort_name": "all_source_orders",
            "source_file": "orders_clean.csv",
            "description": "Toan bo nguon gom ca 2.855 don huy",
            "total_orders": len(orders_all),
            "late_orders": int(orders_all['late_delivery_risk'].sum()),
            "late_rate_pct": round(orders_all['late_delivery_risk'].mean() * 100, 2),
            "scheduled_mean": round(orders_all['shipping_days_scheduled'].mean(), 2),
            "actual_mean": round(orders_all['shipping_days_actual'].mean(), 2),
            "actual_std": round(orders_all['shipping_days_actual'].std(), 2),
            "delay_mean": round(orders_all['delay_days'].mean(), 2)
        },
        {
            "cohort_name": "complete_and_closed_orders",
            "source_file": "orders_clean.csv (trang thai COMPLETE, CLOSED)",
            "description": "Don hang da hoan tat va dong chu trinh",
            "total_orders": len(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]),
            "late_orders": int(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['late_delivery_risk'].sum()),
            "late_rate_pct": round(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['late_delivery_risk'].mean() * 100, 2),
            "scheduled_mean": round(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['shipping_days_scheduled'].mean(), 2),
            "actual_mean": round(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['shipping_days_actual'].mean(), 2),
            "actual_std": round(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['shipping_days_actual'].std(), 2),
            "delay_mean": round(orders_all[orders_all['order_status'].isin(['COMPLETE', 'CLOSED'])]['delay_days'].mean(), 2)
        },
        {
            "cohort_name": "without_first_class",
            "source_file": "orders_analysis.csv (loai tru First Class)",
            "description": "Mau loai tru 9.602 don First Class",
            "total_orders": len(orders[orders['shipping_mode'] != 'First Class']),
            "late_orders": int(orders[orders['shipping_mode'] != 'First Class']['late_delivery_risk'].sum()),
            "late_rate_pct": round(orders[orders['shipping_mode'] != 'First Class']['late_delivery_risk'].mean() * 100, 2),
            "scheduled_mean": round(orders[orders['shipping_mode'] != 'First Class']['shipping_days_scheduled'].mean(), 2),
            "actual_mean": round(orders[orders['shipping_mode'] != 'First Class']['shipping_days_actual'].mean(), 2),
            "actual_std": round(orders[orders['shipping_mode'] != 'First Class']['shipping_days_actual'].std(), 2),
            "delay_mean": round(orders[orders['shipping_mode'] != 'First Class']['delay_days'].mean(), 2)
        },
        {
            "cohort_name": "timestamp_consistent_subset",
            "source_file": "orders_analysis.csv (duration_mismatch_flag == 0)",
            "description": "Don khong lech ngay giua timestamp va ngay nguyen",
            "total_orders": len(orders[orders['duration_mismatch_flag'] == 0]),
            "late_orders": int(orders[orders['duration_mismatch_flag'] == 0]['late_delivery_risk'].sum()),
            "late_rate_pct": round(orders[orders['duration_mismatch_flag'] == 0]['late_delivery_risk'].mean() * 100, 2),
            "scheduled_mean": round(orders[orders['duration_mismatch_flag'] == 0]['shipping_days_scheduled'].mean(), 2),
            "actual_mean": round(orders[orders['duration_mismatch_flag'] == 0]['shipping_days_actual'].mean(), 2),
            "actual_std": round(orders[orders['duration_mismatch_flag'] == 0]['shipping_days_actual'].std(), 2),
            "delay_mean": round(orders[orders['duration_mismatch_flag'] == 0]['delay_days'].mean(), 2)
        }
    ]
    df_tab00 = pd.DataFrame(cohorts)
    df_tab00.to_csv(TABLES_DIR / "00_overview_baseline_kpis.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 01: Shipping Mode Detailed Metrics
    # -------------------------------------------------------------------------
    mode_agg = orders.groupby('shipping_mode').agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        scheduled_mean=('shipping_days_scheduled', 'mean'),
        scheduled_std=('shipping_days_scheduled', 'std'),
        actual_mean=('shipping_days_actual', 'mean'),
        actual_std=('shipping_days_actual', 'std'),
        actual_p25=('shipping_days_actual', lambda x: x.quantile(0.25)),
        actual_p50=('shipping_days_actual', 'median'),
        actual_p75=('shipping_days_actual', lambda x: x.quantile(0.75)),
        actual_p90=('shipping_days_actual', lambda x: x.quantile(0.90)),
        actual_p95=('shipping_days_actual', lambda x: x.quantile(0.95)),
        delay_mean=('delay_days', 'mean')
    ).reset_index()
    mode_agg['order_share_pct'] = round(mode_agg['order_count'] / N_ORDERS * 100, 2)
    mode_agg['late_rate_pct'] = round(mode_agg['late_rate'] * 100, 2)
    mode_agg['scheduled_mean'] = round(mode_agg['scheduled_mean'], 2)
    mode_agg['scheduled_std'] = round(mode_agg['scheduled_std'].fillna(0), 2)
    mode_agg['actual_mean'] = round(mode_agg['actual_mean'], 2)
    mode_agg['actual_std'] = round(mode_agg['actual_std'], 2)
    mode_agg['delay_mean'] = round(mode_agg['delay_mean'], 2)
    cols_mode = ['shipping_mode', 'order_count', 'order_share_pct', 'late_count', 'late_rate_pct', 'scheduled_mean', 'scheduled_std', 'actual_mean', 'actual_std', 'actual_p25', 'actual_p50', 'actual_p75', 'actual_p90', 'actual_p95', 'delay_mean']
    df_tab01 = mode_agg[cols_mode].sort_values(by='late_rate_pct', ascending=False)
    df_tab01.to_csv(TABLES_DIR / "01_shipping_mode_detailed.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 02: Mode Actual Days Distribution (0 to 6 days)
    # -------------------------------------------------------------------------
    mode_dist = pd.crosstab(orders['shipping_mode'], orders['shipping_days_actual'])
    for col in range(7):
        if col not in mode_dist.columns:
            mode_dist[col] = 0
    mode_dist = mode_dist[[0, 1, 2, 3, 4, 5, 6]]
    mode_dist_pct = mode_dist.div(mode_dist.sum(axis=1), axis=0) * 100
    df_tab02 = mode_dist.copy()
    df_tab02.columns = [f'count_day_{c}' for c in df_tab02.columns]
    for c in range(7):
        df_tab02[f'pct_day_{c}'] = mode_dist_pct[c].round(2)
    df_tab02['total_orders'] = mode_dist.sum(axis=1)
    df_tab02.reset_index(inplace=True)
    df_tab02.to_csv(TABLES_DIR / "02_mode_actual_days_distribution.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 03: Market Performance
    # -------------------------------------------------------------------------
    mkt_agg = orders.groupby('market').agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        scheduled_mean=('shipping_days_scheduled', 'mean'),
        actual_mean=('shipping_days_actual', 'mean'),
        delay_mean=('delay_days', 'mean')
    ).reset_index().sort_values(by='order_count', ascending=False)
    mkt_agg['order_share_pct'] = round(mkt_agg['order_count'] / N_ORDERS * 100, 2)
    mkt_agg['late_rate_pct'] = round(mkt_agg['late_rate'] * 100, 2)
    mkt_agg['scheduled_mean'] = round(mkt_agg['scheduled_mean'], 2)
    mkt_agg['actual_mean'] = round(mkt_agg['actual_mean'], 2)
    mkt_agg['delay_mean'] = round(mkt_agg['delay_mean'], 2)
    cols_mkt = ['market', 'order_count', 'order_share_pct', 'late_count', 'late_rate_pct', 'scheduled_mean', 'actual_mean', 'delay_mean']
    df_tab03 = mkt_agg[cols_mkt]
    df_tab03.to_csv(TABLES_DIR / "03_market_performance.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 04: Region Performance
    # -------------------------------------------------------------------------
    reg_agg = orders.groupby(['order_region', 'market']).agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        scheduled_mean=('shipping_days_scheduled', 'mean'),
        actual_mean=('shipping_days_actual', 'mean'),
        delay_mean=('delay_days', 'mean')
    ).reset_index().sort_values(by='order_count', ascending=False)
    reg_agg['order_share_pct'] = round(reg_agg['order_count'] / N_ORDERS * 100, 2)
    reg_agg['late_rate_pct'] = round(reg_agg['late_rate'] * 100, 2)
    reg_agg['scheduled_mean'] = round(reg_agg['scheduled_mean'], 2)
    reg_agg['actual_mean'] = round(reg_agg['actual_mean'], 2)
    reg_agg['delay_mean'] = round(reg_agg['delay_mean'], 2)
    cols_reg = ['order_region', 'market', 'order_count', 'order_share_pct', 'late_count', 'late_rate_pct', 'scheduled_mean', 'actual_mean', 'delay_mean']
    df_tab04 = reg_agg[cols_reg]
    df_tab04.to_csv(TABLES_DIR / "04_region_performance.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 05: Temporal Weekday & Weekend
    # -------------------------------------------------------------------------
    weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    orders['weekday_name'] = orders['order_weekday'].map(weekday_map)
    wk_agg = orders.groupby(['order_weekday', 'weekday_name', 'order_is_weekend']).agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean'),
        scheduled_mean=('shipping_days_scheduled', 'mean')
    ).reset_index()
    wk_agg['order_share_pct'] = round(wk_agg['order_count'] / N_ORDERS * 100, 2)
    wk_agg['late_rate_pct'] = round(wk_agg['late_rate'] * 100, 2)
    wk_agg['actual_mean'] = round(wk_agg['actual_mean'], 2)
    wk_agg['scheduled_mean'] = round(wk_agg['scheduled_mean'], 2)
    df_tab05 = wk_agg
    df_tab05.to_csv(TABLES_DIR / "05_temporal_weekday_weekend.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 06: Temporal Year Month (37 months)
    # -------------------------------------------------------------------------
    ym_agg = orders.groupby(['order_year', 'order_month']).agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean'),
        scheduled_mean=('shipping_days_scheduled', 'mean')
    ).reset_index()
    ym_agg['late_rate_pct'] = round(ym_agg['late_rate'] * 100, 2)
    ym_agg['actual_mean'] = round(ym_agg['actual_mean'], 2)
    ym_agg['scheduled_mean'] = round(ym_agg['scheduled_mean'], 2)
    df_tab06 = ym_agg
    df_tab06.to_csv(TABLES_DIR / "06_temporal_year_month.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 07: Order Complexity & Size
    # -------------------------------------------------------------------------
    orders['qty_bracket'] = pd.cut(orders['total_quantity'], bins=[0, 1, 2, 5, 10, 50], labels=['1 item', '2 items', '3-5 items', '6-10 items', '>10 items'])
    comp_line = orders.groupby('line_count').agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean')
    ).reset_index()
    comp_line['group_type'] = 'line_count'
    comp_line.rename(columns={'line_count': 'bracket_value'}, inplace=True)
    comp_line['bracket_value'] = comp_line['bracket_value'].astype(str)

    comp_qty = orders.groupby('qty_bracket', observed=False).agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean')
    ).reset_index()
    comp_qty['group_type'] = 'quantity_bracket'
    comp_qty.rename(columns={'qty_bracket': 'bracket_value'}, inplace=True)
    comp_qty['bracket_value'] = comp_qty['bracket_value'].astype(str)

    df_tab07 = pd.concat([comp_line, comp_qty], ignore_index=True)
    df_tab07['order_share_pct'] = round(df_tab07['order_count'] / N_ORDERS * 100, 2)
    df_tab07['late_rate_pct'] = round(df_tab07['late_rate'] * 100, 2)
    df_tab07['actual_mean'] = round(df_tab07['actual_mean'], 2)
    df_tab07 = df_tab07[['group_type', 'bracket_value', 'order_count', 'order_share_pct', 'late_count', 'late_rate_pct', 'actual_mean']]
    df_tab07.to_csv(TABLES_DIR / "07_order_complexity_size.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 08: Customer Segment & Payment Type
    # -------------------------------------------------------------------------
    seg_agg = orders.groupby('customer_segment').agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean')
    ).reset_index()
    seg_agg['group_type'] = 'customer_segment'
    seg_agg.rename(columns={'customer_segment': 'category'}, inplace=True)

    pay_agg = orders.groupby('payment_type').agg(
        order_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        actual_mean=('shipping_days_actual', 'mean')
    ).reset_index()
    pay_agg['group_type'] = 'payment_type'
    pay_agg.rename(columns={'payment_type': 'category'}, inplace=True)

    df_tab08 = pd.concat([seg_agg, pay_agg], ignore_index=True)
    df_tab08['order_share_pct'] = round(df_tab08['order_count'] / N_ORDERS * 100, 2)
    df_tab08['late_rate_pct'] = round(df_tab08['late_rate'] * 100, 2)
    df_tab08['actual_mean'] = round(df_tab08['actual_mean'], 2)
    df_tab08 = df_tab08[['group_type', 'category', 'order_count', 'order_share_pct', 'late_count', 'late_rate_pct', 'actual_mean']]
    df_tab08.to_csv(TABLES_DIR / "08_customer_segment_payment.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 09: Departments & Categories
    # -------------------------------------------------------------------------
    dept_agg = items.groupby('department_name').agg(
        item_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        total_revenue=('item_total_net', 'sum')
    ).reset_index().sort_values(by='item_count', ascending=False)
    dept_agg['item_share_pct'] = round(dept_agg['item_count'] / len(items) * 100, 2)
    dept_agg['late_rate_pct'] = round(dept_agg['late_rate'] * 100, 2)
    dept_agg['total_revenue'] = round(dept_agg['total_revenue'], 2)
    dept_agg['level'] = 'Department'
    dept_agg.rename(columns={'department_name': 'name'}, inplace=True)

    cat_agg = items.groupby('category_name').agg(
        item_count=('order_id', 'count'),
        late_count=('late_delivery_risk', 'sum'),
        late_rate=('late_delivery_risk', 'mean'),
        total_revenue=('item_total_net', 'sum')
    ).reset_index().sort_values(by='item_count', ascending=False).head(20)
    cat_agg['item_share_pct'] = round(cat_agg['item_count'] / len(items) * 100, 2)
    cat_agg['late_rate_pct'] = round(cat_agg['late_rate'] * 100, 2)
    cat_agg['total_revenue'] = round(cat_agg['total_revenue'], 2)
    cat_agg['level'] = 'Category'
    cat_agg.rename(columns={'category_name': 'name'}, inplace=True)

    df_tab09 = pd.concat([dept_agg, cat_agg], ignore_index=True)[['level', 'name', 'item_count', 'item_share_pct', 'late_count', 'late_rate_pct', 'total_revenue']]
    df_tab09.to_csv(TABLES_DIR / "09_departments_categories.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 10: Shipping Mode by Market Matrix
    # -------------------------------------------------------------------------
    mat_cnt = pd.crosstab(orders['shipping_mode'], orders['market'])
    mat_late = pd.crosstab(orders['shipping_mode'], orders['market'], values=orders['late_delivery_risk'], aggfunc='sum')
    mat_rate = pd.crosstab(orders['shipping_mode'], orders['market'], values=orders['late_delivery_risk'], aggfunc='mean') * 100
    rows_mat = []
    for mode in sorted(orders['shipping_mode'].unique()):
        for mkt in sorted(orders['market'].unique()):
            rows_mat.append({
                'shipping_mode': mode,
                'market': mkt,
                'order_count': int(mat_cnt.loc[mode, mkt]),
                'late_count': int(mat_late.loc[mode, mkt]),
                'late_rate_pct': round(float(mat_rate.loc[mode, mkt]), 2)
            })
    df_tab10 = pd.DataFrame(rows_mat).sort_values(by=['shipping_mode', 'order_count'], ascending=[True, False])
    df_tab10.to_csv(TABLES_DIR / "10_shipping_mode_by_market_matrix.csv", index=False)

    # -------------------------------------------------------------------------
    # TAB 11: Chi2 Independence Tests & Cramer's V
    # -------------------------------------------------------------------------
    vars_to_test = [
        ('shipping_mode', 'Phuong thuc van chuyen'),
        ('order_region', 'Vung dia ly nhan hang (23 vung)'),
        ('market', 'Thi truong (5 chau luc)'),
        ('customer_segment', 'Phan khuc khach hang'),
        ('payment_type', 'Hinh thuc thanh toan'),
        ('line_count', 'So dong hang trong don (1-5)'),
        ('order_is_weekend', 'Cuoi tuan vs Ngay thuong'),
        ('order_weekday', 'Thu trong tuan (Thu 2 - Chu Nhat)'),
        ('order_year', 'Nam dat hang (2015-2018)')
    ]
    chi_rows = []
    for var, vname in vars_to_test:
        ct = pd.crosstab(orders[var], orders['late_delivery_risk'])
        chi2, p, dof, ex = stats.chi2_contingency(ct)
        cv = cramers_v(ct)
        chi_rows.append({
            'variable': var,
            'variable_label': vname,
            'chi2_stat': round(float(chi2), 2),
            'df': int(dof),
            'p_value': float(p),
            'p_value_formatted': '< 0.0001' if p < 0.0001 else f"{p:.4f}",
            'cramers_v': round(float(cv), 4),
            'association_strength': 'Rat manh' if cv >= 0.35 else ('Trung binh' if cv >= 0.15 else 'Khong dang ke'),
            'statistically_significant': 'Co (p < 0.05)' if p < 0.05 else 'Khong (p >= 0.05)'
        })
    df_tab11 = pd.DataFrame(chi_rows)
    df_tab11.to_csv(TABLES_DIR / "11_chi2_independence_tests.csv", index=False)

    # Remove lingering tab 12 if exists
    tab12_path = TABLES_DIR / "12_logistic_regression_submodel.csv"
    if tab12_path.exists():
        tab12_path.unlink()

    print("    -> 12 bang CSV mo ta va chan doan da xuat hoan tat vao tables/.", flush=True)

    # -------------------------------------------------------------------------
    # FIGURES GENERATION (6 CHARTS)
    # -------------------------------------------------------------------------
    print(">>> 2. Ve 6 bieu do truc quan hoa chat luong cao vao figures/...", flush=True)
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

    # Fig 1: Late Rate by Mode
    fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
    colors = ['#c0392b', '#2980b9', '#e67e22', '#27ae60']
    bars = ax.bar(df_tab01['shipping_mode'], df_tab01['late_rate_pct'], color=colors, width=0.55, edgecolor='#333333', linewidth=1)
    ax.axhline(LATE_RATE * 100, color='#2c3e50', linestyle='--', linewidth=1.5, label=f'Baseline toan he thong ({LATE_RATE*100:.2f}%)')
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1.5, f"{h:.2f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.set_ylabel('Ty le giao tre (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Phuong thuc van chuyen (Shipping Mode)', fontsize=12, fontweight='bold')
    ax.set_title('Hinh 1: Ty le giao hang tre theo Phuong thuc van chuyen', fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig01_late_rate_by_shipping_mode.png")
    plt.close()

    # Fig 2: Actual Days Stacked Bar
    fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
    pct_cols = [f'pct_day_{i}' for i in range(7)]
    df_p2 = df_tab02.set_index('shipping_mode')[pct_cols].copy()
    df_p2.columns = [f'{i} ngay' for i in range(7)]
    df_p2.plot(kind='bar', stacked=True, ax=ax, colormap='Spectral', edgecolor='#333333', linewidth=0.8)
    ax.set_ylabel('Ty le phan phoi (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Phuong thuc van chuyen', fontsize=12, fontweight='bold')
    ax.set_title('Hinh 2: Phan phoi Thoi gian giao hang thuc te (0 den 6 ngay) trong du lieu', fontsize=13, fontweight='bold', pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontweight='bold')
    ax.legend(title='So ngay thuc te', bbox_to_anchor=(1.02, 1), loc='upper left')
    ax.set_ylim(0, 105)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig02_actual_days_distribution.png")
    plt.close()

    # Fig 3: Market Performance
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    x = np.arange(len(df_tab03))
    w = 0.35
    r1 = ax.bar(x - w/2, df_tab03['late_rate_pct'], w, label='Ty le giao tre (%)', color='#e67e22', edgecolor='#333333')
    r2 = ax.bar(x + w/2, df_tab03['order_share_pct'], w, label='Ty trong don hang (%)', color='#3498db', edgecolor='#333333')
    for r in r1:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2., h + 1, f'{h:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    for r in r2:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2., h + 1, f'{h:.1f}%', ha='center', va='bottom', fontsize=10)
    ax.set_xticks(x)
    ax.set_xticklabels(df_tab03['market'], fontweight='bold', fontsize=11)
    ax.set_ylabel('Ty le (%)', fontsize=12, fontweight='bold')
    ax.set_title('Hinh 3: Ty le giao tre va Co cau don hang theo Thi truong (Market)', fontsize=13, fontweight='bold', pad=15)
    ax.set_ylim(0, 75)
    ax.legend(frameon=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig03_market_performance.png")
    plt.close()

    # Fig 4: Monthly Trend
    fig, ax1 = plt.subplots(figsize=(12, 5), dpi=300)
    df_tab06['ym'] = df_tab06['order_year'].astype(str) + '-' + df_tab06['order_month'].astype(str).str.zfill(2)
    c1 = '#2980b9'
    ax1.set_xlabel('Thang dat hang (2015-01 den 2018-01)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('So luong don hang', color=c1, fontsize=12, fontweight='bold')
    l1 = ax1.plot(range(len(df_tab06)), df_tab06['order_count'], color=c1, marker='o', linewidth=2, label='So don hang')
    ax1.tick_params(axis='y', labelcolor=c1)

    ax2 = ax1.twinx()
    c2 = '#c0392b'
    ax2.set_ylabel('Ty le giao tre (%)', color=c2, fontsize=12, fontweight='bold')
    l2 = ax2.plot(range(len(df_tab06)), df_tab06['late_rate_pct'], color=c2, linestyle='--', marker='s', linewidth=2, label='Ty le tre (%)')
    ax2.tick_params(axis='y', labelcolor=c2)
    ax2.set_ylim(45, 70)

    step = 3
    ax1.set_xticks(range(0, len(df_tab06), step))
    ax1.set_xticklabels(df_tab06['ym'].iloc[::step], rotation=45, ha='right', fontsize=9)
    lines = l1 + l2
    ax1.legend(lines, [l.get_label() for l in lines], loc='upper right', frameon=True)
    plt.title('Hinh 4: Dien bien San luong va Ty le giao tre qua 37 thang lich su', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig04_monthly_trend.png")
    plt.close()

    # Fig 5: Weekday
    fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
    bars = ax.bar(df_tab05['weekday_name'], df_tab05['late_rate_pct'], color='#16a085', width=0.55, edgecolor='#333333')
    ax.axhline(LATE_RATE * 100, color='#d35400', linestyle='--', linewidth=1.5, label=f'Trung binh chung ({LATE_RATE*100:.2f}%)')
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 1, f"{h:.2f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_ylim(40, 70)
    ax.set_ylabel('Ty le giao tre (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Thu trong tuan', fontsize=11, fontweight='bold')
    ax.set_title('Hinh 5: Ty le giao tre theo Thu trong tuan (Thu Hai den Chu Nhat)', fontsize=13, fontweight='bold', pad=15)
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig05_weekday_performance.png")
    plt.close()

    # Fig 6: Risk Matrix Heatmap
    piv = df_tab10.pivot(index='shipping_mode', columns='market', values='late_rate_pct')
    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)
    sns.heatmap(piv, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Ty le giao tre (%)'}, linewidths=1, linecolor='white', ax=ax, annot_kws={'size': 12, 'weight': 'bold'})
    ax.set_title('Hinh 6: Ma tran Ty le Giao tre (Shipping Mode x Thi truong)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Thi truong (Market)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Phuong thuc van chuyen (Shipping Mode)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "fig06_risk_heatmap.png")
    plt.close()
    print("    -> 6 bieu do PNG da xuat hoan tat vao figures/.", flush=True)

    print(">>> HOAN TAT PIPELINE TU DONG HOA 100%!", flush=True)

if __name__ == "__main__":
    run()
