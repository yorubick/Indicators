"""Contrasta sin reentrenar q lineal con y sin cuantización en el maestro."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import probar_ley_dimensionless_C as q_audit


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
Q_RESULT = ROOT / "resultado_C_ley_dimensionless.json"
RESULT = ROOT / "resultado_C_q_redondeado_maestro.json"
RESIDUAL = ROOT / "residuos_C_q_redondeado_maestro.csv"
SHORT_DENOMINATOR = 183.0
TOL = 1e-6


def short_prediction(n: int, delta: float) -> float:
    return delta * max(1.0, 10.0 * n / SHORT_DENOMINATOR)


def metric(residuals: list[float]) -> dict[str, Any]:
    absolute = [abs(value) for value in residuals]
    if not absolute:
        return {"n": 0, "MAE": None, "RMSE": None, "max_abs_residual": None, "exact_1e-6": 0, "within_1": 0}
    return {
        "n": len(absolute),
        "MAE": sum(absolute) / len(absolute),
        "RMSE": math.sqrt(sum(value * value for value in absolute) / len(absolute)),
        "max_abs_residual": max(absolute),
        "exact_1e-6": sum(value <= TOL for value in absolute),
        "within_1": sum(value <= 1.0 + 1e-9 for value in absolute),
    }


def main() -> None:
    master_bytes = MASTER.read_bytes()
    cases = json.loads(master_bytes.decode("utf-8"))["cases"]
    q_results_bytes = Q_RESULT.read_bytes()
    q_results = json.loads(q_results_bytes.decode("utf-8"))
    assert q_results["master_sha256"] == hashlib.sha256(master_bytes).hexdigest()
    model = q_results["models"]["linear_n"]
    rows: list[dict[str, Any]] = []
    for case in cases:
        bars = int(case["bars"])
        delta = float(case["source_seconds"])
        q_hat = q_audit.predict_q(model, {"features": q_audit.features(case)})
        c_hat_raw = delta * q_hat
        c_hat_round = float(math.floor(c_hat_raw + 0.5))
        c_hat_short = short_prediction(bars, delta) if bars < 21 else None
        c_hat_hybrid = c_hat_short if bars < 21 else c_hat_round
        partition = "locked_holdout" if q_audit.is_holdout(case) else "development"
        interval = case["C_Character_interval"]
        row: dict[str, Any] = {
            "case_id": case["id"],
            "source_seconds": delta,
            "bars": bars,
            "partition": partition,
            "C_Lite_observed": case["C_Lite"],
            "C_hat_q_raw": c_hat_raw,
            "residual_q_raw": c_hat_raw - float(case["C_Lite"]) if case["C_Lite"] is not None else None,
            "C_hat_q_nearest_integer": c_hat_round,
            "residual_q_nearest_integer": c_hat_round - float(case["C_Lite"]) if case["C_Lite"] is not None else None,
            "C_hat_short_branch": c_hat_short,
            "C_hat_short_plus_rounded_q_diagnostic": c_hat_hybrid,
            "residual_short_plus_rounded_q": c_hat_hybrid - float(case["C_Lite"]) if case["C_Lite"] is not None else None,
            "Character_lower_inclusive": interval["lower_inclusive"] if interval else None,
            "Character_upper_exclusive": interval["upper_exclusive"] if interval else None,
            "q_raw_Character_compatible": interval["lower_inclusive"] <= c_hat_raw < interval["upper_exclusive"] if interval else None,
            "q_round_Character_compatible": interval["lower_inclusive"] <= c_hat_round < interval["upper_exclusive"] if interval else None,
            "hybrid_Character_compatible": interval["lower_inclusive"] <= c_hat_hybrid < interval["upper_exclusive"] if interval else None,
        }
        rows.append(row)

    def lite_subset(predicate) -> list[dict[str, Any]]:
        return [row for row in rows if row["C_Lite_observed"] is not None and predicate(row)]

    def summarize(subset: list[dict[str, Any]], residual_key: str) -> dict[str, Any]:
        return metric([float(row[residual_key]) for row in subset])

    lite = lite_subset(lambda row: True)
    groups = {
        "all_lite_hybrid": summarize(lite, "residual_short_plus_rounded_q"),
        "all_lite_q_raw": summarize(lite, "residual_q_raw"),
        "all_lite_q_rounded": summarize(lite, "residual_q_nearest_integer"),
    }
    for name, predicate in {
        "short_n_lt_21": lambda row: row["bars"] < 21,
        "long_n_ge_21": lambda row: row["bars"] >= 21,
        "holdout_all_n": lambda row: row["partition"] == "locked_holdout",
        "holdout_short": lambda row: row["partition"] == "locked_holdout" and row["bars"] < 21,
        "holdout_long": lambda row: row["partition"] == "locked_holdout" and row["bars"] >= 21,
        "development_long": lambda row: row["partition"] == "development" and row["bars"] >= 21,
    }.items():
        subset = lite_subset(predicate)
        groups[f"{name}_hybrid"] = summarize(subset, "residual_short_plus_rounded_q")
        if name in ("long_n_ge_21", "holdout_long", "development_long"):
            groups[f"{name}_q_raw"] = summarize(subset, "residual_q_raw")
            groups[f"{name}_q_rounded"] = summarize(subset, "residual_q_nearest_integer")

    character = [row for row in rows if row["C_Lite_observed"] is None]
    character_summary = {
        "n": len(character),
        "q_raw_compatible": sum(row["q_raw_Character_compatible"] for row in character),
        "q_nearest_integer_compatible": sum(row["q_round_Character_compatible"] for row in character),
        "hybrid_compatible": sum(row["hybrid_Character_compatible"] for row in character),
        "long_n_ge_21": {
            "n": sum(row["bars"] >= 21 for row in character),
            "q_raw_compatible": sum(row["q_raw_Character_compatible"] for row in character if row["bars"] >= 21),
            "q_nearest_integer_compatible": sum(row["q_round_Character_compatible"] for row in character if row["bars"] >= 21),
            "hybrid_compatible": sum(row["hybrid_Character_compatible"] for row in character if row["bars"] >= 21),
        },
    }
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    output = {
        "status": "fixed_linear_n_q_quantization_diagnostic_no_refit",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "q_model_sha256": hashlib.sha256(q_results_bytes).hexdigest(),
        "formula_raw": "C_hat = Delta * q_hat_linear_n(n), coefficients frozen in resultado_C_ley_dimensionless.json",
        "formula_round": "C_hat = floor(Delta*q_hat + 0.5), diagnostic quantizer motivated by integer long labels; no coefficients fitted",
        "formula_hybrid": "Use measured short empirical relation for n<21; use rounded q_linear_n for n>=21. Diagnostic only; the split is not a unified law.",
        "metrics": groups,
        "Character_interval_compatibility": character_summary,
        "residual_rows": len(rows),
        "residual_csv": str(RESIDUAL),
        "limitation": "This adds no blind data. The rounded q variant does not rescue the long branch across the reserved master cases or Character intervals; exact short fit remains empirical.",
    }
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({"status": output["status"], "metrics": groups, "Character_interval_compatibility": character_summary, "outputs": {"json": str(RESULT), "csv": str(RESIDUAL)}}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
