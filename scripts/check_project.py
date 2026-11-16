"""Read-only integrity and handoff checks; run from any working directory."""
from pathlib import Path
import csv, hashlib, json

ROOT = Path(__file__).resolve().parents[1]

def rows(path):
    with (ROOT/path).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def keyed(path):
    data = rows(path)
    result = {row['order_id']: row for row in data}
    if len(data) != len(result):
        raise ValueError(f'Duplicate order_id: {path}')
    return result

def main():
    count = 0
    for manifest in ['references/resource_manifest.json', 'references/restored_data_manifest.json']:
        for record in json.loads((ROOT/manifest).read_text(encoding='utf-8')):
            path = ROOT/record['path']
            if hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
                raise ValueError(f'Checksum mismatch: {path}')
            count += 1
    print(f'PASS: {count} source/restored checksums')
    analysis = keyed('data/processed/orders_analysis.csv')
    assert len(analysis) == 62897
    assert sum(int(row['late_delivery_risk']) for row in analysis.values()) == 36048
    splits = keyed('data/processed/orders_model_splits.csv')
    test_ids = {key for key,row in splits.items() if row['partition'] == 'test'}
    datasets = [keyed(p) for p in [
        'data/external/predictions_test_handoff.csv',
        'workstreams/forecasting/results/predictions_test.csv',
        'workstreams/prescriptive/inputs/dataco/predictions_test.csv',
        'workstreams/prescriptive/results/dashboard_orders_test.csv']]
    assert len(test_ids) == 13071
    for dataset in datasets:
        assert set(dataset) == test_ids
        for key,row in dataset.items():
            assert 0 <= float(row['P_Late']) <= 1
            assert abs(float(row['P_Late'])-float(datasets[0][key]['P_Late'])) < 1e-10
            assert row['late_delivery_risk'] == analysis[key]['late_delivery_risk']
    print('PASS: 62,897 analysis orders; 36,048 late labels; four handoffs match 13,071 test IDs, labels and P_Late')

if __name__ == '__main__':
    main()
