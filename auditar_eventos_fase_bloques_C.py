"""Cross-validate the fixed structural-event rule for C modular phases.

The rule (phase changes iff the entering bar confirms a strict new global
extreme or radius-1 local pivot) was defined in auditar_fase_base3_C.py. This
script adds temporally disjoint component holdouts; it does not tune the rule.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import auditar_validacion_bloques_disjuntos_C as block_audit


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
PAIR_CSV = ROOT / "transiciones_C_fase_base3.csv"
RESULT = ROOT / "resultado_C_eventos_fase_bloques.json"
RESIDUAL = ROOT / "residuos_C_eventos_fase_bloques.csv"
TARGETS = ("3", "9")


def as_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def metrics(actual: list[bool], predicted: list[bool]) -> dict[str, Any]:
    tp = sum(a and p for a, p in zip(actual, predicted))
    tn = sum((not a) and (not p) for a, p in zip(actual, predicted))
    fp = sum((not a) and p for a, p in zip(actual, predicted))
    fn = sum(a and (not p) for a, p in zip(actual, predicted))
    n = len(actual)
    return {
        "n": n, "TP": tp, "FP": fp, "FN": fn, "TN": tn,
        "accuracy": (tp + tn) / n if n else None,
        "actual_change_rate": sum(actual) / n if n else None,
    }


def main() -> None:
    master_bytes = MASTER.read_bytes()
    cases = json.loads(master_bytes.decode("utf-8"))["cases"]
    case_component, component_summary = block_audit.temporal_components(cases)
    with PAIR_CSV.open(encoding="utf-8-sig", newline="") as handle:
        source_pairs = list(csv.DictReader(handle))
    integer_pairs = [row for row in source_pairs if as_bool(row["integer_endpoints"])]
    assert (len(source_pairs), len(integer_pairs)) == (87, 66)

    pairs: list[dict[str, Any]] = []
    for row in integer_pairs:
        prev_id, curr_id = row["previous_case_id"], row["current_case_id"]
        component = case_component[prev_id]
        assert component == case_component[curr_id]
        pairs.append({
            "component": component,
            "dt": int(row["dt_seconds"]),
            "START": row["START"],
            "END_current": row["END_current"],
            "previous_case_id": prev_id,
            "current_case_id": curr_id,
            "event": as_bool(row["any_predeclared_event"]),
            "C_previous": float(row["C_previous"]),
            "C_current": float(row["C_current"]),
            "delta_C": float(row["delta_C"]),
            "changed_mod_3": as_bool(row["C_phase_changed_mod_3"]),
            "changed_mod_9": as_bool(row["C_phase_changed_mod_9"]),
        })

    prediction_rows: list[dict[str, Any]] = []
    fold_summary: list[dict[str, Any]] = []
    for component in component_summary:
        fold = int(component["component"])
        test = [pair for pair in pairs if pair["component"] == fold]
        train = [pair for pair in pairs if pair["component"] != fold]
        target_results: dict[str, Any] = {}
        for target in TARGETS:
            label_key = f"changed_mod_{target}"
            training_labels = [pair[label_key] for pair in train]
            training_counts = Counter(training_labels)
            baseline_label = training_counts[True] > training_counts[False]
            actual = [pair[label_key] for pair in test]
            event_prediction = [pair["event"] for pair in test]
            baseline_prediction = [baseline_label] * len(test)
            target_results[target] = {
                "training_pairs": len(train),
                "test_pairs": len(test),
                "training_majority_prediction": baseline_label,
                "event_rule": metrics(actual, event_prediction),
                "other_components_majority_baseline": metrics(actual, baseline_prediction),
            }
            for pair, event_hat, baseline_hat in zip(test, event_prediction, baseline_prediction):
                prediction_rows.append({
                    **pair,
                    "target_modulus": int(target),
                    "actual_phase_changed": pair[label_key],
                    "event_rule_prediction": event_hat,
                    "other_components_majority_prediction": baseline_hat,
                })
        fold_summary.append({"component": fold, "targets": target_results})

    aggregate: dict[str, Any] = {}
    for target in TARGETS:
        rows = [row for row in prediction_rows if row["target_modulus"] == int(target)]
        actual = [row["actual_phase_changed"] for row in rows]
        aggregate[target] = {
            "event_rule": metrics(actual, [row["event_rule_prediction"] for row in rows]),
            "other_components_majority_baseline": metrics(
                actual, [row["other_components_majority_prediction"] for row in rows]
            ),
            "by_source_seconds": {
                str(delta): {
                    "event_rule": metrics(
                        [row["actual_phase_changed"] for row in rows if row["dt"] == delta],
                        [row["event_rule_prediction"] for row in rows if row["dt"] == delta],
                    ),
                    "other_components_majority_baseline": metrics(
                        [row["actual_phase_changed"] for row in rows if row["dt"] == delta],
                        [row["other_components_majority_prediction"] for row in rows if row["dt"] == delta],
                    ),
                }
                for delta in sorted({row["dt"] for row in rows})
            },
        }

    fields = list(prediction_rows[0])
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(prediction_rows)
    output = {
        "status": "fixed_phase_event_rule_audited_with_disjoint_temporal_blocks",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "pair_definition": "Same START, one source interval forward, exact OHLCV prefix; endpoints both integer within tolerance 1e-7.",
        "event_rule": "Predict phase change iff the entering bar makes a strict new global high/low or confirms a radius-1 local high/low.",
        "baseline": "For each fold and modulus, predict True only when the other components contain more changed than unchanged phases; ties predict False.",
        "temporal_components": len(component_summary),
        "all_adjacent_pairs": len(source_pairs),
        "integer_endpoint_pairs": len(integer_pairs),
        "folds": fold_summary,
        "aggregate_leave_component_out": aggregate,
        "residual_rows": len(prediction_rows),
        "residual_csv": str(RESIDUAL),
        "limitation": "The 15-second transitions all belong to one overlapping episode; labels are known and this is not a prospective test. Predicting phase alone cannot predict C's level or amplitude.",
    }
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "temporal_components": output["temporal_components"],
        "integer_endpoint_pairs": output["integer_endpoint_pairs"],
        "aggregate_leave_component_out": aggregate,
        "component_6": next(f for f in fold_summary if f["component"] == 6),
        "residual_rows": output["residual_rows"],
        "files": {"result_json": str(RESULT), "residual_csv": str(RESIDUAL)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
