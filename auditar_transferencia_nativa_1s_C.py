"""Aplica sin reentrenar candidatas congeladas del maestro a la serie nativa de 1 s."""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

import analizar_modelo_C_independiente as long_model
import analizar_C_frontera_1s as one_second
import analizar_C_frontera_1s_replicas as replicas
import probar_ley_dimensionless_C as dimensionless


ROOT = Path(__file__).resolve().parent
MANUAL = ROOT / "manual"
MASTER = ROOT / "master_all_C_cases.json"
LONG_RESULTS = ROOT / "resultado_C_modelo_independiente.json"
Q_RESULTS = ROOT / "resultado_C_ley_dimensionless.json"
ONE_SECOND_AUDIT = ROOT / "resultado_C_meseta_1s_conteos.json"
RESULT = ROOT / "resultado_C_transferencia_1s.json"
RESIDUAL = ROOT / "residuos_C_transferencia_1s.csv"
PREDICTION_NAMES = ("constant_q", "linear_n", "log_n", "normalized_ohlcv")


def metrics(predicted: list[float], observed: list[float]) -> dict[str, Any]:
    residuals = [p - o for p, o in zip(predicted, observed)]
    absolute = [abs(r) for r in residuals]
    return {
        "n": len(residuals),
        "MAE": sum(absolute) / len(absolute) if absolute else None,
        "RMSE": math.sqrt(sum(r * r for r in residuals) / len(residuals)) if residuals else None,
        "max_abs_residual": max(absolute) if absolute else None,
        "within_1e-6": sum(r <= 1e-6 for r in absolute),
        "within_1": sum(r <= 1.0 + 1e-9 for r in absolute),
    }


def read_pair(n: int) -> tuple[dict[int, dict[str, str]], dict[int, dict[str, str]]]:
    if n in (20, 21):
        paths = [MANUAL / f"C_1s_r1404_n{n}_{suffix}.csv" for suffix in ("a", "b")]
        reader = replicas.read
    else:
        paths = [MANUAL / f"C_1s_plateau_n{n}_{suffix}.csv" for suffix in ("a", "b")]
        reader = one_second.read
    first, second = [reader(path) for path in paths]
    common = set(first) & set(second)
    assert common
    check_keys = ("open", "high", "low", "close", "Volume", *one_second.LANES)
    assert all(first[t][key] == second[t][key] for t in common for key in check_keys)
    return first, second


def main() -> None:
    master_hash = hashlib.sha256(MASTER.read_bytes()).hexdigest()
    long_data = json.loads(LONG_RESULTS.read_text(encoding="utf-8"))
    q_data = json.loads(Q_RESULTS.read_text(encoding="utf-8"))
    audit = json.loads(ONE_SECOND_AUDIT.read_text(encoding="utf-8"))
    assert long_data["master_sha256"] == q_data["master_sha256"] == master_hash
    assert audit["counts"] == list(range(20, 41))

    branch = long_data["long_branch_candidate"]
    long_fit = {
        "mean": np.asarray(branch["mean"], dtype=float),
        "scale": np.asarray(branch["scale"], dtype=float),
        "beta": np.asarray(branch["beta"], dtype=float),
    }
    q_models = q_data["models"]
    observations = {int(row["n"]): float(row["C_Lite_reconstructed"]) for row in audit["rows"]}
    start = int(replicas.stamp("2026-10-14T14:04:00Z"))

    rows: list[dict[str, Any]] = []
    cases: dict[int, dict[str, Any]] = {}
    for n in range(20, 41):
        first, second = read_pair(n)
        end = start + n - 1
        assert all(t in second for t in range(start, end + 1))
        bars = [
            {
                "time": int(second[t]["time"]),
                "open": float(second[t]["open"]),
                "high": float(second[t]["high"]),
                "low": float(second[t]["low"]),
                "close": float(second[t]["close"]),
                "volume": float(second[t]["Volume"]),
            }
            for t in range(start, end + 1)
        ]
        assert len(bars) == n
        case = {"bars": n, "source_seconds": 1, "OHLCV": bars, "C_Lite": observations[n]}
        cases[n] = case
        fit_lanes = one_second.fit_lite(second, step=1, period_seconds=1)
        actual_from_lanes = sum(fit["C"] for fit in fit_lanes.values()) / len(fit_lanes)
        assert abs(actual_from_lanes - observations[n]) <= 1e-12

        row: dict[str, Any] = {
            "n": n,
            "C_Lite": observations[n],
            "C_hat_short_rule": long_model.short_prediction(case) if n < 21 else None,
            "short_rule_residual": long_model.short_prediction(case) - observations[n] if n < 21 else None,
            "C_hat_long_OLS_raw": long_model.raw_prediction(case, long_fit) if n >= 21 else None,
            "C_hat_long_OLS_rounded": long_model.model_prediction(case, long_fit) if n >= 21 else None,
        }
        q_feature_row = {"features": dimensionless.features(case)}
        for name in PREDICTION_NAMES:
            q_hat = dimensionless.predict_q(q_models[name], q_feature_row)
            c_hat = float(case["source_seconds"]) * q_hat
            row[f"C_hat_{name}"] = c_hat
            row[f"residual_{name}"] = c_hat - observations[n]
            rounded_hat = float(math.floor(c_hat + 0.5))
            row[f"C_hat_{name}_nearest_integer"] = rounded_hat
            row[f"residual_{name}_nearest_integer"] = rounded_hat - observations[n]
        for key in ("C_hat_long_OLS_raw", "C_hat_long_OLS_rounded"):
            row[f"residual_{key.removeprefix('C_hat_')}"] = row[key] - observations[n] if row[key] is not None else None
        rows.append(row)

    long_rows = [row for row in rows if row["n"] >= 21]
    actual = [float(row["C_Lite"]) for row in long_rows]
    summaries = {
        name: metrics([float(row[f"C_hat_{name}"]) for row in long_rows], actual)
        for name in PREDICTION_NAMES
    }
    summaries.update({
        f"{name}_nearest_integer": metrics(
            [float(row[f"C_hat_{name}_nearest_integer"]) for row in long_rows], actual
        )
        for name in PREDICTION_NAMES
    })
    summaries["long_branch_OLS_raw"] = metrics([float(row["C_hat_long_OLS_raw"]) for row in long_rows], actual)
    summaries["long_branch_OLS_rounded"] = metrics([float(row["C_hat_long_OLS_rounded"]) for row in long_rows], actual)
    one_case = rows[0]

    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    output = {
        "status": "frozen_master_models_scored_on_supplementary_native_1s_sequence",
        "master_sha256": master_hash,
        "training_models_frozen_before_this_audit": {
            "long_branch_candidate_sha256": hashlib.sha256(LONG_RESULTS.read_bytes()).hexdigest(),
            "dimensionless_models_sha256": hashlib.sha256(Q_RESULTS.read_bytes()).hexdigest(),
            "long_branch_formula": branch["formula"],
            "dimensionless_formulas": {name: q_models[name]["formula"] for name in PREDICTION_NAMES},
        },
        "test_scope": "21 nested 1s OHLCV windows n=20..40 from one NQ1! ETH episode; not part of the 179-case master. No coefficients were refit. This is an out-of-resolution diagnostic, not a blind or independent-session validation.",
        "evaluated_long_counts": len(long_rows),
        "metrics_n21_to_40": summaries,
        "short_n20_check": {
            "C_hat_short_rule": one_case["C_hat_short_rule"],
            "C_Lite": one_case["C_Lite"],
            "residual": one_case["short_rule_residual"],
        },
        "residual_rows": len(rows),
        "residual_csv": str(RESIDUAL),
        "integer_quantization_note": "Nearest-integer q variants are scored as fixed post-quantization diagnostics because all long master labels are integer to measurement precision. They were not part of the original q equations and are not presented as discovered laws.",
        "limitations": [
            "The test series has one start/session and includes many nested prefixes.",
            "The fitted long models were previously selected on the master; applying them here does not establish a new prospective holdout.",
            "A failure rejects these frozen candidates at 1s, not all deterministic OHLCV laws.",
        ],
    }
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({"status": output["status"], "metrics_n21_to_40": summaries, "short_n20_check": output["short_n20_check"], "outputs": {"json": str(RESULT), "csv": str(RESIDUAL)}}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
