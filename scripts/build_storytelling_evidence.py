"""Reconcile existing handoff results for the storytelling flow; no model refits.

Run from any directory. --check compares current source tables with the saved
evidence without rewriting any handoff, dataset, or generated report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports/storytelling/evidence.json"
SOURCES = {
    "baseline": "reports/data_quality/baseline_kpis.csv",
    "modes": "workstreams/descriptive/tables/01_shipping_mode_detailed.csv",
    "tests": "workstreams/descriptive/tables/11_chi2_independence_tests.csv",
    "selection": "workstreams/forecasting/results/model_selection.json",
    "models": "workstreams/forecasting/results/model_comparison.csv",
    "mode_probabilities": "workstreams/forecasting/results/mode_baseline_train.csv",
    "subgroups": "workstreams/forecasting/results/subgroups_test.csv",
    "promises": "workstreams/prescriptive/results/promise_summary.csv",
    "pilot_modes": "workstreams/prescriptive/results/pilot_by_mode_test.csv",
    "routes": "workstreams/prescriptive/results/routing_summary.csv",
    "fleet": "workstreams/prescriptive/results/fleet_sizing_bounds.csv",
}


def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / SOURCES[name]).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def one(records: list[dict], **filters: str) -> dict:
    found = [row for row in records if all(row[k] == v for k, v in filters.items())]
    if len(found) != 1:
        raise ValueError(f"Expected exactly one record matching {filters}, got {len(found)}")
    return found[0]


def build() -> dict:
    checks = []

    def require(name: str, condition: bool) -> None:
        if not condition:
            raise ValueError(f"Evidence reconciliation failed: {name}")
        checks.append(name)

    baseline = one(rows("baseline"), grain="order", cohort="non_canceled_valid")
    n, late = int(baseline["records_in_cohort"]), int(baseline["late_count"])
    modes = rows("modes")
    require("mode order counts reconcile to main cohort", sum(int(r["order_count"]) for r in modes) == n)
    require("mode late counts reconcile to main cohort", sum(int(r["late_count"]) for r in modes) == late)
    require("main late rate matches numerator/denominator", math.isclose(float(baseline["late_rate"]), late / n))
    method_evidence = []
    for row in modes:
        count, late_count = int(row["order_count"]), int(row["late_count"])
        require(f"{row['shipping_mode']} rounded late percentage matches counts",
                abs(late_count / count * 100 - float(row["late_rate_pct"])) <= 0.0051)
        method_evidence.append({
            "shipping_mode": row["shipping_mode"], "orders": count, "late_count": late_count,
            "late_rate": late_count / count, "share_of_all_late_orders": late_count / late,
            "scheduled_mean_days": float(row["scheduled_mean"]), "actual_mean_days_rounded": float(row["actual_mean"]),
        })
    tests = rows("tests")
    test_evidence = {r["variable"]: {"p_value": float(r["p_value"]), "cramers_v": float(r["cramers_v"])}
                     for r in tests if r["variable"] in {"shipping_mode", "market", "order_region"}}
    selection = json.loads((ROOT / SOURCES["selection"]).read_text(encoding="utf-8"))
    models = rows("models")
    selected = selection["selected_model"]
    selected_val = one(models, model=selected, partition="validation")
    validation_candidates = [float(r["log_loss"]) for r in models if r["partition"] == "validation"]
    require("selected model minimizes validation log loss", float(selected_val["log_loss"]) == min(validation_candidates))
    test = one(models, model=selected, partition="test")
    tn, fp, fn, tp = (int(test[k]) for k in ["tn", "fp", "fn", "tp"])
    test_n, test_late = int(test["n"]), int(test["late_count"])
    require("test confusion matrix sums to population", tn + fp + fn + tp == test_n)
    require("test confusion matrix sums to late orders", fn + tp == test_late)
    require("test precision matches confusion counts", math.isclose(float(test["precision"]), tp / (tp + fp), abs_tol=1e-10))
    require("test recall matches confusion counts", math.isclose(float(test["recall"]), tp / (tp + fn), abs_tol=1e-10))
    probabilities = rows("mode_probabilities")
    require("baseline training counts match main training split", sum(int(r["count"]) for r in probabilities) == 39568)
    mode_groups = [r for r in rows("subgroups") if r["field"] == "shipping_mode"]
    require("model mode subgroup counts sum to test", sum(int(r["n"]) for r in mode_groups) == test_n)
    require("model mode subgroup misses sum to test misses", sum(int(r["fn"]) for r in mode_groups) == fn)
    promise_rows = rows("promises")
    current = one(promise_rows, policy="current", partition="test")
    pilot = one(promise_rows, policy="bounded_plus1_keep_same_day", partition="test")
    require("policy and model use equal test population counts", int(current["n"]) == int(pilot["n"]) == test_n)
    require("policy baseline rate equals model test label rate", math.isclose(float(current["current_late_rate"]), test_late / test_n))
    require("duration is unchanged by promise scenario", float(current["mean_actual_days"]) == float(pilot["mean_actual_days"]))
    pilot_modes = rows("pilot_modes")
    require("policy mode counts sum to test", sum(int(r["n"]) for r in pilot_modes) == test_n)
    exceedances = sum(int(r["proposed_exceedance_count"]) for r in pilot_modes)
    require("policy exceedances reconcile across mode/summary", math.isclose(exceedances / test_n, float(pilot["proposed_exceedance_rate"])))
    for row in pilot_modes:
        forecast_group = one(mode_groups, group=row["shipping_mode"])
        require(f"{row['shipping_mode']} policy/model subgroup counts agree", int(row["n"]) == int(forecast_group["n"]))
        require(f"{row['shipping_mode']} policy/model late counts agree", int(row["current_late_count"]) == int(forecast_group["late_count"]))
    routes = rows("routes")
    nearest = one(routes, instance="c101", scenario="base", method="nearest_feasible")
    ortools = one(routes, instance="c101", scenario="base", method="ortools")
    require("C101 comparison has two feasible results", nearest["status"] == ortools["status"] == "feasible")
    require("C101 comparison uses identical capacity/fleet constraints",
            all(nearest[k] == ortools[k] for k in ["capacity", "max_vehicles"]))
    fleet = one(rows("fleet"), instance="c101", scenario="base")
    lower_bound = math.ceil(float(fleet["total_demand"]) / float(fleet["vehicle_capacity"]))
    require("C101 vehicle lower bound agrees with feasible fleet", lower_bound == int(fleet["capacity_lower_bound"]) == int(float(ortools["vehicles_used"])))
    return {
        "scope": "Reconciliation of saved aggregate handoffs, not a rerun of training/solving or a per-order join audit",
        "source_sha256": {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES.values()},
        "population": {"non_canceled_orders": n, "late_orders": late, "late_rate": late / n,
                       "model_policy_test_orders": test_n, "test_late_orders": test_late},
        "shipping_modes": method_evidence, "association_tests": test_evidence,
        "forecast": {"selected_model": selected, "selection_criterion": selection["criterion"],
                     "roc_auc_test": float(test["roc_auc"]), "threshold": float(test["threshold"]),
                     "alerts": tp + fp, "true_alerts": tp, "false_alerts": fp, "missed_late": fn,
                     "precision": tp / (tp + fp), "recall": tp / (tp + fn), "alert_share_of_test": (tp + fp) / test_n,
                     "group_risk_levels": {r["shipping_mode"]: float(r["mean"]) for r in probabilities}},
        "bounded_promise": {"test_orders": test_n, "current_exceedance_rate": test_late / test_n,
                            "proposed_exceedance_count": exceedances, "proposed_exceedance_rate": exceedances / test_n,
                            "reduction_percentage_points": (test_late - exceedances) / test_n * 100,
                            "added_mean_promise_days": float(pilot["mean_proposed_days"]) - float(current["mean_current_days"]),
                            "unchanged_mean_actual_days": float(pilot["mean_actual_days"]),
                            "second_class_remaining_exceedance_rate": float(one(pilot_modes, shipping_mode="Second Class")["proposed_exceedance_rate"])},
        "routing_c101": {"scope": "Solomon C101, capacity 200, 100 benchmark customers; independent of DataCo",
                         "nearest_distance_units": float(nearest["distance_units"]), "ortools_distance_units": float(ortools["distance_units"]),
                         "distance_reduction_pct": (1 - float(ortools["distance_units"]) / float(nearest["distance_units"])) * 100,
                         "nearest_vehicles": int(float(nearest["vehicles_used"])), "ortools_vehicles": int(float(ortools["vehicles_used"])),
                         "vehicle_lower_bound": lower_bound, "distance_optimality_proven": False},
        "checks": checks, "checks_passed": len(checks),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify saved evidence without writing files")
    args = parser.parse_args()
    evidence = build()
    if args.check:
        saved = json.loads(OUTPUT.read_text(encoding="utf-8"))
        if saved != evidence:
            raise ValueError("Saved evidence differs from current handoffs; review and regenerate it.")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"PASS: {evidence['checks_passed']} aggregate reconciliations; saved evidence {'matches' if args.check else 'written'}")
