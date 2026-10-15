"""Descriptive audit of modulo-3 / modulo-9 phase transitions in Lite C.

No model is fitted. The event definition matches the predeclared sweep audit:
strict new window high/low or radius-1 local pivot confirmed by the entering bar.
All input pairs are adjacent END windows with exact OHLCV-prefix equality.
"""
from __future__ import annotations

import collections
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
SWEEP = ROOT / "C_barrido_END_1855_1920_1924_15s.json"
RESULT = ROOT / "resultado_C_fase_base3.json"
RESIDUAL = ROOT / "transiciones_C_fase_base3.csv"
INTEGER_TOLERANCE = 1e-7


def is_integer_measurement(value: float) -> bool:
    return abs(value - round(value)) <= INTEGER_TOLERANCE


def entering_events(previous: dict[str, Any], entering: dict[str, Any]) -> dict[str, bool]:
    bars = previous["OHLCV"]
    prior_high = max(float(b["high"]) for b in bars)
    prior_low = min(float(b["low"]) for b in bars)
    new_global_high = float(entering["high"]) > prior_high
    new_global_low = float(entering["low"]) < prior_low
    confirmed_local_high = (
        len(bars) >= 2
        and float(bars[-1]["high"]) > float(bars[-2]["high"])
        and float(bars[-1]["high"]) >= float(entering["high"])
    )
    confirmed_local_low = (
        len(bars) >= 2
        and float(bars[-1]["low"]) < float(bars[-2]["low"])
        and float(bars[-1]["low"]) <= float(entering["low"])
    )
    return {
        "new_global_high": new_global_high,
        "new_global_low": new_global_low,
        "confirmed_local_high_radius1": confirmed_local_high,
        "confirmed_local_low_radius1": confirmed_local_low,
        "any_predeclared_event": bool(
            new_global_high or new_global_low or confirmed_local_high or confirmed_local_low
        ),
    }


def row_metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    integer_rows = [r for r in rows if r["integer_endpoints"]]
    result: dict[str, Any] = {
        "pairs": len(rows),
        "integer_endpoint_pairs": len(integer_rows),
        "nonzero_integer_endpoint_pairs": sum(round(r["delta_C"]) != 0 for r in integer_rows),
        "event_pairs_integer": sum(r["any_predeclared_event"] for r in integer_rows),
        "no_event_pairs_integer": sum(not r["any_predeclared_event"] for r in integer_rows),
    }
    for modulus in (3, 9):
        result[f"delta_C_divisible_by_{modulus}"] = sum(
            r[f"delta_C_mod_{modulus}"] == 0 for r in integer_rows
        )
        result[f"nonzero_delta_C_divisible_by_{modulus}"] = sum(
            r[f"delta_C_mod_{modulus}"] == 0 and round(r["delta_C"]) != 0
            for r in integer_rows
        )
        result[f"C_phase_changed_mod_{modulus}"] = sum(
            r[f"C_phase_changed_mod_{modulus}"] for r in integer_rows
        )
        result[f"phase_change_mod_{modulus}_by_event"] = {
            label: {
                "n": sum(bool(r["any_predeclared_event"]) == event for r in integer_rows),
                "changed": sum(
                    bool(r["any_predeclared_event"]) == event
                    and r[f"C_phase_changed_mod_{modulus}"]
                    for r in integer_rows
                ),
            }
            for label, event in (("event", True), ("no_event", False))
        }
    return result


def _modulus_metrics(rows: list[dict[str, Any]], delta: int, modulus: int) -> dict[str, int]:
    selected = [r for r in rows if r["integer_endpoints"] and r["dt_seconds"] == delta]
    nonzero = [r for r in selected if round(r["delta_C"]) != 0]
    return {
        "n": len(selected),
        "delta_C_divisible": sum(r[f"delta_C_mod_{modulus}"] == 0 for r in selected),
        "n_nonzero": len(nonzero),
        "delta_C_divisible_nonzero": sum(r[f"delta_C_mod_{modulus}"] == 0 for r in nonzero),
    }


def phase_rule_score(rows: list[dict[str, Any]], event_key: str, modulus: int) -> dict[str, Any]:
    selected = [r for r in rows if r["integer_endpoints"]]
    if not selected:
        return {"n": 0, "event_n": 0, "correct": 0, "accuracy": None, "always_class_accuracy": None}
    truth = [bool(r[f"C_phase_changed_mod_{modulus}"]) for r in selected]
    prediction = [bool(r[event_key]) for r in selected]
    tp = sum(p and y for p, y in zip(prediction, truth))
    fp = sum(p and not y for p, y in zip(prediction, truth))
    fn = sum(not p and y for p, y in zip(prediction, truth))
    tn = sum(not p and not y for p, y in zip(prediction, truth))
    return {
        "n": len(selected),
        "event_n": sum(prediction),
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
        "accuracy": (tp + tn) / len(selected),
        "always_class_accuracy": max(sum(truth), len(truth) - sum(truth)) / len(truth),
    }


def main() -> None:
    master_bytes = MASTER.read_bytes()
    cases = json.loads(master_bytes.decode("utf-8"))["cases"]
    by_anchor = {
        (int(c["source_seconds"]), int(c["START_unix"]), int(c["END_unix"])): c
        for c in cases
    }
    rows: list[dict[str, Any]] = []
    for current in cases:
        delta = int(current["source_seconds"])
        previous = by_anchor.get((delta, int(current["START_unix"]), int(current["END_unix"]) - delta))
        if previous is None or previous["OHLCV"] != current["OHLCV"][:-1]:
            continue
        if previous["C_Lite"] is None or current["C_Lite"] is None:
            continue
        c_previous = float(previous["C_Lite"])
        c_current = float(current["C_Lite"])
        integer_endpoints = is_integer_measurement(c_previous) and is_integer_measurement(c_current)
        events = entering_events(previous, current["OHLCV"][-1])
        row: dict[str, Any] = {
            "dt_seconds": delta,
            "START": current["START"],
            "END_previous": previous["END"],
            "END_current": current["END"],
            "previous_case_id": previous["id"],
            "current_case_id": current["id"],
            "n_previous": previous["bars"],
            "C_previous": c_previous,
            "C_current": c_current,
            "delta_C": c_current - c_previous,
            "integer_endpoints": integer_endpoints,
            **events,
        }
        if integer_endpoints:
            cp, cc = int(round(c_previous)), int(round(c_current))
            d_c = cc - cp
            for modulus in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
                row[f"delta_C_mod_{modulus}"] = d_c % modulus
            row["C_previous_mod_3"] = cp % 3
            row["C_current_mod_3"] = cc % 3
            row["C_phase_changed_mod_3"] = cp % 3 != cc % 3
            row["C_previous_mod_9"] = cp % 9
            row["C_current_mod_9"] = cc % 9
            row["C_phase_changed_mod_9"] = cp % 9 != cc % 9
        else:
            for modulus in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
                row[f"delta_C_mod_{modulus}"] = None
            for key in (
                "C_previous_mod_3", "C_current_mod_3", "C_phase_changed_mod_3",
                "C_previous_mod_9", "C_current_mod_9", "C_phase_changed_mod_9",
            ):
                row[key] = None
        rows.append(row)

    assert len(rows) == 87
    integer_rows = [r for r in rows if r["integer_endpoints"]]
    assert len(integer_rows) == 66
    by_delta = {
        str(delta): row_metrics([r for r in rows if r["dt_seconds"] == delta])
        for delta in (15, 30, 60, 120)
    }
    modulus_scan = {
        str(modulus): {
            str(delta): _modulus_metrics(rows, delta, modulus)
            for delta in (15, 30, 60, 120)
        }
        for modulus in range(2, 13)
    }
    event_phase_tables = {}
    for modulus in (3, 9):
        event_phase_tables[str(modulus)] = {
            "event_changed": sum(r["integer_endpoints"] and r["any_predeclared_event"] and r[f"C_phase_changed_mod_{modulus}"] for r in rows),
            "event_unchanged": sum(r["integer_endpoints"] and r["any_predeclared_event"] and not r[f"C_phase_changed_mod_{modulus}"] for r in rows),
            "no_event_changed": sum(r["integer_endpoints"] and not r["any_predeclared_event"] and r[f"C_phase_changed_mod_{modulus}"] for r in rows),
            "no_event_unchanged": sum(r["integer_endpoints"] and not r["any_predeclared_event"] and not r[f"C_phase_changed_mod_{modulus}"] for r in rows),
        }
    event_rule_scores = {
        scope: {
            str(modulus): {
                event_key: phase_rule_score(group, event_key, modulus)
                for event_key in (
                    "new_global_high", "new_global_low", "confirmed_local_high_radius1",
                    "confirmed_local_low_radius1", "any_predeclared_event",
                )
            }
            for modulus in (3, 9)
        }
        for scope, group in {
            "all": rows,
            "15": [r for r in rows if r["dt_seconds"] == 15],
            "60": [r for r in rows if r["dt_seconds"] == 60],
            "120": [r for r in rows if r["dt_seconds"] == 120],
        }.items()
    }
    sweep_keys = {
        (int(c["dt"]), c["START"], c["END"])
        for c in json.loads(SWEEP.read_text(encoding="utf-8"))["cases"]
    }
    sweep_pairs = [
        r for r in rows
        if (r["dt_seconds"], r["START"], r["END_current"]) in sweep_keys
    ]
    assert len(sweep_pairs) == 16
    by_track: dict[tuple[int, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        by_track[(int(row["dt_seconds"]), str(row["START"]))].append(row)
    track_summary = []
    for (delta, start), track in sorted(by_track.items()):
        metrics = row_metrics(track)
        track_summary.append({"dt_seconds": delta, "START": start, **metrics})

    output = {
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "scope": "Descriptive arithmetic audit only; no fitted or predictive rule.",
        "integer_tolerance": INTEGER_TOLERANCE,
        "pair_definition": "same START, END advances one source interval, exact OHLCV prefix match, both cases have Lite decimal measurements",
        "event_definition": "strict new global high/low or radius-1 local high/low confirmed by the entering bar",
        "all_pairs": len(rows),
        "integer_endpoint_pairs": len(integer_rows),
        "integer_endpoint_fraction": len(integer_rows) / len(rows),
        "by_source_seconds": by_delta,
        "modulus_scan_2_to_12": modulus_scan,
        "phase_change_event_tables": event_phase_tables,
        "univariate_event_phase_rule_scores": event_rule_scores,
        "sweep_pairs": row_metrics(sweep_pairs),
        "tracks_by_start": track_summary,
        "interpretation": (
            "A modulo-3/9 phase-preservation pattern is a working hypothesis, not a law: "+
            "the 66 integer-endpoint pairs are overlapping windows, event association is descriptive, "+
            "and no rule for the quotient/amplitude or fractional outputs is identified."
        ),
        "residual_csv": str(RESIDUAL),
    }
    fields = list(rows[0])
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    compact_by_delta = {
        delta: {
            "integer_pairs": by_delta[delta]["integer_endpoint_pairs"],
            "nonzero_pairs": by_delta[delta]["nonzero_integer_endpoint_pairs"],
            "nonzero_delta_divisible_by_3": by_delta[delta]["nonzero_delta_C_divisible_by_3"],
            "nonzero_delta_divisible_by_9": by_delta[delta]["nonzero_delta_C_divisible_by_9"],
            "phase_changes_mod_3": by_delta[delta]["C_phase_changed_mod_3"],
        }
        for delta in ("15", "30", "60", "120")
    }
    compact_rule_scores = {
        scope: {
            modulus: {
                event_key: {
                    "accuracy": event_rule_scores[scope][modulus][event_key]["accuracy"],
                    "baseline": event_rule_scores[scope][modulus][event_key]["always_class_accuracy"],
                }
                for event_key in ("new_global_high", "any_predeclared_event")
            }
            for modulus in ("3", "9")
        }
        for scope in ("all", "15", "60")
    }
    print(json.dumps({
        "all_pairs": output["all_pairs"],
        "integer_endpoint_pairs": output["integer_endpoint_pairs"],
        "by_source_seconds": compact_by_delta,
        "phase_change_event_tables": event_phase_tables,
        "event_rule_accuracy_vs_baseline": compact_rule_scores,
        "sweep_pairs": output["sweep_pairs"],
        "tracks": len(track_summary),
        "files": {"result_json": str(RESULT), "transition_csv": str(RESIDUAL)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
