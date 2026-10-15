r"""Describe output-level base-3/base-9 residues without fitting a rule.

Uses only measured Lite labels from the frozen master. Fractional short-regime
values are kept separate and never rounded into residue classes. Frequencies
are descriptive because windows overlap, especially the 15-second sweep.

Run from any directory with Python 3:
    python G:\trading\guias\analisis\auditar_niveles_modulares_C.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
RESULT = ROOT / "resultado_C_niveles_modulares.json"
RESIDUAL = ROOT / "residuos_C_niveles_modulares.csv"
INTEGER_TOLERANCE = 1e-7
MODULI = (3, 9, 27)


def is_integer_output(value: float) -> bool:
    return abs(value - round(value)) <= INTEGER_TOLERANCE


def main() -> None:
    master_bytes = MASTER.read_bytes()
    cases = json.loads(master_bytes.decode("utf-8"))["cases"]
    lite = [case for case in cases if case["C_Lite"] is not None]
    assert (len(cases), len(lite)) == (179, 145)

    grouped: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for case in lite:
        n = int(case["bars"])
        regime = "short_n_lt_21" if n < 21 else "long_n_ge_21"
        grouped[(int(case["source_seconds"]), regime)].append(case)

    groups: list[dict[str, Any]] = []
    for (delta, regime), rows in sorted(grouped.items()):
        ints = [case for case in rows if is_integer_output(float(case["C_Lite"]))]
        fractions = [case for case in rows if not is_integer_output(float(case["C_Lite"]))]
        value_counts = Counter(int(round(float(case["C_Lite"]))) for case in ints)
        residues: dict[str, Any] = {}
        for modulus in MODULI:
            residue_counts = Counter(value % modulus for value in value_counts.elements())
            unique_residue_counts = Counter(value % modulus for value in value_counts)
            residues[str(modulus)] = {
                "case_counts": {str(r): int(residue_counts.get(r, 0)) for r in range(modulus)},
                "unique_output_value_counts": {
                    str(r): int(unique_residue_counts.get(r, 0)) for r in range(modulus)
                },
                "largest_case_share": (
                    max(residue_counts.values()) / len(ints) if ints else None
                ),
                "uniform_reference_share": 1.0 / modulus,
            }
        groups.append({
            "source_seconds": delta,
            "regime": regime,
            "cases": len(rows),
            "integer_cases": len(ints),
            "fractional_cases": len(fractions),
            "unique_integer_C_values": len(value_counts),
            "integer_C_frequency": {str(value): int(count) for value, count in sorted(value_counts.items())},
            "integer_output_residues": residues,
            "fractional_cases_exact": [
                {"case_id": case["id"], "n": int(case["bars"]), "C_Lite": float(case["C_Lite"])}
                for case in fractions
            ],
        })

    sweep_start = int(dt.datetime(2026, 10, 12, 18, 55, tzinfo=dt.timezone.utc).timestamp())
    sweep_start_time = int(dt.datetime(2026, 10, 12, 19, 20, tzinfo=dt.timezone.utc).timestamp())
    sweep_end_time = int(dt.datetime(2026, 10, 12, 19, 24, tzinfo=dt.timezone.utc).timestamp())
    sweep = sorted(
        [
            case for case in lite
            if int(case["source_seconds"]) == 15
            and int(case["START_unix"]) == sweep_start
            and sweep_start_time <= int(case["END_unix"]) <= sweep_end_time
        ],
        key=lambda case: int(case["END_unix"]),
    )
    assert len(sweep) == 17, f"Expected 17 sweep rows, got {len(sweep)}"
    sweep_values = [float(case["C_Lite"]) for case in sweep]
    assert all(is_integer_output(value) for value in sweep_values)
    sweep_ints = [int(round(value)) for value in sweep_values]
    sweep_deltas = [b - a for a, b in zip(sweep_ints, sweep_ints[1:])]
    sweep_mod9_changes = [a % 9 != b % 9 for a, b in zip(sweep_ints, sweep_ints[1:])]
    sweep_summary = {
        "case_ids": [case["id"] for case in sweep],
        "END_UTC": [case["END"] for case in sweep],
        "C_integer_levels": sweep_ints,
        "C_mod_3": [value % 3 for value in sweep_ints],
        "C_mod_9": [value % 9 for value in sweep_ints],
        "delta_C": sweep_deltas,
        "transitions": len(sweep_deltas),
        "nonzero_transitions": sum(delta != 0 for delta in sweep_deltas),
        "nonzero_delta_divisible_by_3": sum(delta != 0 and delta % 3 == 0 for delta in sweep_deltas),
        "nonzero_delta_divisible_by_9": sum(delta != 0 and delta % 9 == 0 for delta in sweep_deltas),
        "phase_changes_mod_9": sum(sweep_mod9_changes),
        "phase_preserving_mod_9": sum(not changed for changed in sweep_mod9_changes),
        "phase_preserving_nonzero_delta_mod_9": sum(
            not changed and delta != 0 for changed, delta in zip(sweep_mod9_changes, sweep_deltas)
        ),
    }

    case_rows: list[dict[str, Any]] = []
    for case in lite:
        value = float(case["C_Lite"])
        integer = is_integer_output(value)
        integer_value = int(round(value)) if integer else None
        case_rows.append({
            "case_id": case["id"],
            "source_seconds": int(case["source_seconds"]),
            "bars": int(case["bars"]),
            "regime": "short_n_lt_21" if int(case["bars"]) < 21 else "long_n_ge_21",
            "C_Lite_exact": repr(value),
            "integer_within_tolerance": integer,
            "rounded_integer_used_only_if_integer": integer_value,
            "C_mod_3": integer_value % 3 if integer else None,
            "C_mod_9": integer_value % 9 if integer else None,
            "C_mod_27": integer_value % 27 if integer else None,
        })
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(case_rows[0]))
        writer.writeheader()
        writer.writerows(case_rows)

    output = {
        "status": "descriptive_level_residue_audit_no_generator_identified",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "scope": "Measured C_Lite only; integer residues use tolerance 1e-7; fractional short values are not rounded. Counts are dependent because windows overlap.",
        "integer_tolerance": INTEGER_TOLERANCE,
        "moduli": list(MODULI),
        "groups_by_source_and_n_regime": groups,
        "barrido_1855_1920_1924_15s": sweep_summary,
        "case_level_csv": str(RESIDUAL),
        "interpretation": (
            "The 15-second long windows concentrate on C mod 9 = 7, including the sweep's stable level basin, "
            "but the 60-second long windows occupy all nine residues. The 15-second cases are from one overlapping "
            "episode, so this is not evidence for a universal base-9 phase or a causal entry-candle rule."
        ),
    }
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "groups": [
            {
                "source_seconds": group["source_seconds"],
                "regime": group["regime"],
                "cases": group["cases"],
                "integer_cases": group["integer_cases"],
                "fractional_cases": group["fractional_cases"],
                "unique_integer_C_values": group["unique_integer_C_values"],
                "mod_3": group["integer_output_residues"]["3"]["case_counts"],
                "mod_9": group["integer_output_residues"]["9"]["case_counts"],
                "unique_mod_9": group["integer_output_residues"]["9"]["unique_output_value_counts"],
            }
            for group in groups
        ],
        "sweep": sweep_summary,
        "result_json": str(RESULT),
        "case_level_csv": str(RESIDUAL),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
