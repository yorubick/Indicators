"""Resume saltos de C y contrasta formulas predefinidas; no entrena un operador."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from statistics import fmean, median

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "barrido_start_1933.json"
DEFAULT_REPORT = ROOT / "data" / "analisis_barrido_start_1933.json"


def round_half_up(x: float) -> int:
    return math.floor(x + 0.5)


def evaluate(data: dict) -> dict:
    measured = [c for c in data.get("cases", []) if c.get("status") == "measured" and c.get("C_resuelto") is not None]
    measured.sort(key=lambda c: c["START"])
    comparisons = []
    for candidate in ("continuous_T_over_18_3", "max_source_step_and_continuous", "nearest_integer_T_over_18_3", "floor_T_over_18_3"):
        errors = []
        rows = []
        for case in measured:
            T = float(case["T_seg"])
            source_dt = float(case["source_interval_seconds"])
            observed = float(case["C_resuelto"])
            raw = T / 18.3
            if candidate == "continuous_T_over_18_3":
                predicted = raw
            elif candidate == "max_source_step_and_continuous":
                predicted = max(source_dt, raw)
            elif candidate == "nearest_integer_T_over_18_3":
                predicted = float(round_half_up(raw))
            else:
                predicted = float(math.floor(raw))
            error = predicted - observed
            errors.append(abs(error))
            rows.append({"case_id": case["case_id"], "C_observed": observed, "C_predicted": predicted, "error_pred_minus_obs": error})
        comparisons.append({
            "candidate": candidate,
            "n": len(rows),
            "mae_seconds": fmean(errors) if errors else None,
            "max_abs_error_seconds": max(errors) if errors else None,
            "exact_within_1e_6_count": sum(e <= 1e-6 for e in errors),
            "per_case": rows,
        })
    jumps = []
    for prev, cur in zip(measured, measured[1:]):
        delta = float(cur["C_resuelto"]) - float(prev["C_resuelto"])
        jumps.append({
            "from_case": prev["case_id"], "to_case": cur["case_id"],
            "C_from": prev["C_resuelto"], "C_to": cur["C_resuelto"], "delta_C": delta,
        })
    return {
        "schema_version": 1,
        "input_status": data.get("status"),
        "measured_cases": len(measured),
        "scope": "one END, one date/symbol and adjacent STARTs; descriptive calibration only",
        "conclusion": (
            "No se declara una ley universal. Los candidatos solo se comparan con C medido; "
            "se necesita validación en fechas, END y resoluciones independientes."
        ),
        "comparisons": comparisons,
        "jumps_by_start": jumps,
        "C_summary": {
            "min": min((float(c["C_resuelto"]) for c in measured), default=None),
            "median": median(float(c["C_resuelto"]) for c in measured) if measured else None,
            "max": max((float(c["C_resuelto"]) for c in measured), default=None),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evalúa candidatos simples contra C ya medido.")
    parser.add_argument("--input", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    report = evaluate(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Reporte: {args.output.resolve()}")
    print(f"Casos medidos: {report['measured_cases']}")
    for item in report["comparisons"]:
        print(f"{item['candidate']}: MAE={item['mae_seconds']}, máximo={item['max_abs_error_seconds']}, exactos={item['exact_within_1e_6_count']}/{item['n']}")


if __name__ == "__main__":
    main()
