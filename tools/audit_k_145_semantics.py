#!/usr/bin/env python3
"""Audit the 145 measured Lite cases under both bar-count and elapsed-time semantics."""
from __future__ import annotations

import datetime as dt
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "master_all_C_cases.json"
OUTPUT = ROOT / "data" / "audit_k_145_semantics.json"


def round_half_up(value: float) -> int:
    return math.floor(value + 0.5)


def elapsed_seconds(case: dict[str, Any]) -> int:
    start = dt.datetime.fromisoformat(case["START"])
    end = dt.datetime.fromisoformat(case["END"])
    return int((end - start).total_seconds())


def summarize(cases: list[dict[str, Any]], basis: str) -> dict[str, Any]:
    short_rows: list[dict[str, Any]] = []
    long_rows: list[dict[str, Any]] = []
    for case in cases:
        step = int(case["source_seconds"])
        elapsed = elapsed_seconds(case)
        if basis == "elapsed":
            duration = elapsed
            n_source = math.floor(duration / step + 1e-12)
        else:
            n_source = int(case["bars"])
            duration = n_source * step

        c_observed = float(case["C_Lite"])
        row = {
            "id": case["id"],
            "source_seconds": step,
            "bars_master": int(case["bars"]),
            "n_source_for_basis": int(n_source),
            "elapsed_seconds": elapsed,
            "duration_seconds_for_basis": int(duration),
            "C_observed": c_observed,
            "prior_split": case.get("prior_split"),
            "blind_or_prospective": bool(case.get("blind_or_prospective", False)),
        }
        if n_source < 21:
            predicted = max(float(step), duration * 10.0 / 183.0)
            row.update({
                "C_predicted": predicted,
                "abs_error": abs(c_observed - predicted),
            })
            short_rows.append(row)
        else:
            base = round_half_up(duration / 18.3)
            c_integer = round_half_up(c_observed)
            d_c = c_integer - base
            row.update({
                "C_integer": c_integer,
                "integer_residual": abs(c_observed - c_integer),
                "base_round_T_over_18_3": base,
                "dC": d_c,
                "k_dC_over_9": d_c / 9.0,
                "dC_mod_9": d_c % 9,
                "dC_mod_3": d_c % 3,
            })
            long_rows.append(row)

    by_timeframe: dict[str, Any] = {}
    for step in sorted({int(case["source_seconds"]) for case in cases}):
        s = [r for r in short_rows if r["source_seconds"] == step]
        l = [r for r in long_rows if r["source_seconds"] == step]
        errors = [r["abs_error"] for r in s]
        integer_errors = [r["integer_residual"] for r in l]
        by_timeframe[str(step)] = {
            "total": len(s) + len(l),
            "short_count": len(s),
            "short_exact_within_1e_9": sum(e < 1e-9 for e in errors),
            "short_max_abs_error": max(errors, default=None),
            "long_count": len(l),
            "long_integer_C_within_1e_9": sum(e < 1e-9 for e in integer_errors),
            "long_max_integer_residual": max(integer_errors, default=None),
            "long_dC_multiple_of_9": sum(r["dC_mod_9"] == 0 for r in l),
        }

    short_errors = [r["abs_error"] for r in short_rows]
    long_integer_errors = [r["integer_residual"] for r in long_rows]
    mod9 = Counter(r["dC_mod_9"] for r in long_rows)
    d_c = Counter(r["dC"] for r in long_rows)
    return {
        "basis": basis,
        "short_count": len(short_rows),
        "short_exact_within_1e_9": sum(e < 1e-9 for e in short_errors),
        "short_max_abs_error": max(short_errors, default=None),
        "long_count": len(long_rows),
        "long_integer_C_within_1e_9": sum(e < 1e-9 for e in long_integer_errors),
        "long_max_integer_residual": max(long_integer_errors, default=None),
        "long_dC_multiple_of_9": sum(r["dC_mod_9"] == 0 for r in long_rows),
        "long_dC_not_multiple_of_9": sum(r["dC_mod_9"] != 0 for r in long_rows),
        "long_dC_min": min((r["dC"] for r in long_rows), default=None),
        "long_dC_max": max((r["dC"] for r in long_rows), default=None),
        "long_dC_mod_9_distribution": {str(k): mod9[k] for k in range(9)},
        "long_dC_distribution": {str(k): v for k, v in sorted(d_c.items())},
        "by_source_seconds": by_timeframe,
        "short_cases": short_rows,
        "long_cases": long_rows,
    }


def main() -> None:
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    cases = [c for c in master.get("cases", []) if c.get("C_Lite") is not None]
    relation = Counter()
    for case in cases:
        step = int(case["source_seconds"])
        ratio = elapsed_seconds(case) / step
        relation[str(int(case["bars"]) - math.floor(ratio + 1e-12))] += 1

    report = {
        "schema_version": 1,
        "dataset": str(MASTER.name),
        "lite_measured_cases": len(cases),
        "all_cases_bars_minus_elapsed_intervals": dict(relation),
        "notes": [
            "Legacy-bar-count basis reproduces the earlier analysis that defines T = bars * source_seconds.",
            "Elapsed basis matches Pine v1.3 duration_T = END - START and n_source_bars = floor(T / dt).",
            "k is integer exactly when dC = C_integer - round(T / 18.3) is divisible by 9.",
            "A discrete integer C does not imply an integer k on a 9-second lattice.",
            "This is a descriptive audit, not a blind holdout; the master labels all Lite cases as non-prospective.",
        ],
        "legacy_bar_count_basis": summarize(cases, "legacy_bar_count"),
        "pine_elapsed_basis": summarize(cases, "elapsed"),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for label in ("legacy_bar_count_basis", "pine_elapsed_basis"):
        summary = report[label]
        print(
            f"{label}: short={summary['short_count']} exact="
            f"{summary['short_exact_within_1e_9']} max_short_error={summary['short_max_abs_error']}; "
            f"long={summary['long_count']} integer_C="
            f"{summary['long_integer_C_within_1e_9']} dC_multiple_9="
            f"{summary['long_dC_multiple_of_9']}"
        )
    print(f"bar_count_minus_elapsed_intervals={dict(relation)}")
    print(f"report={OUTPUT}")


if __name__ == "__main__":
    main()