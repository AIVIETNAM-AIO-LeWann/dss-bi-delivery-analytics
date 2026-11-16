"""Capacity lower bound plus saved feasible routing: certify minimum fleet where possible."""
from pathlib import Path
import csv
import math
import argparse

ROOT = Path(__file__).resolve().parents[1]

def write_bounds(results_dir=None):
    result_path = Path(results_dir) if results_dir is not None else ROOT / 'results'
    demands = {}
    for name in ['c101', 'r101', 'rc101']:
        total = 0
        for line in (ROOT / 'inputs' / (name + '.txt')).read_text().splitlines():
            cols = line.split()
            if len(cols) == 7:
                try:
                    total += int(cols[3])
                except ValueError:
                    pass
        demands[name] = total
    with (result_path / 'routing_summary.csv').open(encoding='utf-8-sig') as f:
        records = list(csv.DictReader(f))
    output = []
    for row in records:
        if row['method'] != 'ortools':
            continue
        demand = demands[row['instance']]
        lower = math.ceil(demand / int(row['capacity']))
        used = int(float(row['vehicles_used'])) if row['status'] == 'feasible' else None
        output.append(dict(instance=row['instance'], scenario=row['scenario'],
            total_demand=demand, vehicle_capacity=int(row['capacity']),
            capacity_lower_bound=lower, max_vehicles=int(row['max_vehicles']),
            feasible_vehicles_used=used, minimum_fleet_certified=used == lower,
            proof='capacity_bound_equals_verified_feasible_fleet' if used == lower else 'not_certified'))
    p = result_path / 'fleet_sizing_bounds.csv'
    with p.open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    return output

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--results',default='results')
    args=parser.parse_args()
    for row in write_bounds(ROOT/args.results):
        print(row)
