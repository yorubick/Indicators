r"""Leave-one-temporally-disjoint-block-out audit of existing C candidates.

Blocks are connected components of physical time coverage across all source
resolutions. No OHLCV interval may overlap between a fold's fit and test.
The candidate families and features are fixed in the existing independent
analysis scripts; this audit changes only the split strategy.

Run from any directory with Python 3 and NumPy:
    python G:\trading\guias\analisis\auditar_validacion_bloques_disjuntos_C.py
"""
from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

import analizar_modelo_C_independiente as raw_model
import probar_ley_dimensionless_C as dim_model


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
RESULT = ROOT / "resultado_C_bloques_disjuntos.json"
RESIDUAL = ROOT / "residuos_C_bloques_disjuntos.csv"
DIMENSIONLESS_FEATURES = {
    "linear_n": ["n"],
    "log_n": ["ln_n"],
    "normalized_ohlcv": [
        "ln_n", "window_range_bp", "close_path_bp", "signed_efficiency",
        "volume_weighted_body_bp", "ln_1p_mean_volume", "volume_hhi",
    ],
}


def context(case: dict[str, Any]) -> tuple[Any, ...]:
    return (
        case["symbol"], case["session"], case["timezone"],
        case["contract_adjustment"], case["mode"], case["profile"],
    )


def interval(case: dict[str, Any]) -> tuple[int, int]:
    delta = int(case["source_seconds"])
    times = [int(bar["time"]) for bar in case["OHLCV"]]
    assert times and all(b - a == delta for a, b in zip(times, times[1:])), case["id"]
    return times[0], times[-1] + delta


def temporal_components(cases: list[dict[str, Any]]) -> tuple[dict[str, int], list[dict[str, Any]]]:
    parent = list(range(len(cases)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a: int, b: int) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    spans = [interval(case) for case in cases]
    for i, current in enumerate(cases):
        for j in range(i):
            if context(current) == context(cases[j]):
                a0, a1 = spans[i]
                b0, b1 = spans[j]
                if a0 < b1 and b0 < a1:
                    union(i, j)

    raw_groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(cases)):
        raw_groups[find(i)].append(i)
    ordered = sorted(
        raw_groups.values(),
        key=lambda inds: min(spans[i][0] for i in inds),
    )
    case_component: dict[str, int] = {}
    summary: list[dict[str, Any]] = []
    for component_id, inds in enumerate(ordered, start=1):
        group = [cases[i] for i in inds]
        group_spans = [spans[i] for i in inds]
        summary.append({
            "component": component_id,
            "cases": len(group),
            "Lite_cases": sum(case["C_Lite"] is not None for case in group),
            "Character_only_cases": sum(case["C_Lite"] is None for case in group),
            "by_source_seconds": {
                str(delta): sum(int(case["source_seconds"]) == delta for case in group)
                for delta in sorted({int(case["source_seconds"]) for case in group})
            },
            "coverage_start_unix": min(start for start, _ in group_spans),
            "coverage_end_exclusive_unix": max(end for _, end in group_spans),
            "case_ids": [case["id"] for case in group],
        })
        for case in group:
            case_component[case["id"]] = component_id

    # Establish that the partition really separates all physical coverage.
    for i in range(len(cases)):
        for j in range(i):
            overlap = (
                context(cases[i]) == context(cases[j])
                and spans[i][0] < spans[j][1]
                and spans[j][0] < spans[i][1]
            )
            assert not overlap or case_component[cases[i]["id"]] == case_component[cases[j]["id"]]
    return case_component, summary


def fit_raw(cases: list[dict[str, Any]]) -> dict[str, Any]:
    x = np.vstack([raw_model.feature_vector(case) for case in cases])
    y = np.asarray([float(case["C_Lite"]) for case in cases], dtype=float)
    mean, scale = x.mean(axis=0), x.std(axis=0)
    numeric_constant = scale <= 32 * np.finfo(float).eps * np.maximum(1.0, np.abs(mean))
    scale[numeric_constant] = 1.0
    design = np.column_stack([np.ones(len(cases)), (x - mean) / scale])
    beta, _, rank, singular = np.linalg.lstsq(design, y, rcond=None)
    return {
        "mean": mean, "scale": scale, "beta": beta,
        "numerically_constant_features": [
            name for name, constant in zip(raw_model.FEATURE_NAMES, numeric_constant) if bool(constant)
        ],
        "rank": int(rank), "columns": int(design.shape[1]),
        "singular_values": singular,
        "training_rows": len(cases),
    }


def predict_raw(case: dict[str, Any], fitted: dict[str, Any]) -> float:
    z = (raw_model.feature_vector(case) - fitted["mean"]) / fitted["scale"]
    return float(np.r_[1.0, z] @ fitted["beta"])


def summarize_metric(observed: list[float], predicted: list[float]) -> dict[str, Any]:
    return dim_model.metric(observed, predicted)


def main() -> None:
    master_bytes = MASTER.read_bytes()
    master = json.loads(master_bytes.decode("utf-8"))
    cases = master["cases"]
    assert (len(cases), sum(c["C_Lite"] is not None for c in cases)) == (179, 145)
    component_of, components = temporal_components(cases)
    assert len(components) == 11

    cached_features = {case["id"]: dim_model.features(case) for case in cases}
    predictions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    fit_parameters: dict[str, dict[str, Any]] = defaultdict(dict)
    fold_summaries: list[dict[str, Any]] = []

    for component in components:
        fold = int(component["component"])
        test_cases = [case for case in cases if component_of[case["id"]] == fold]
        train_lite = [case for case in cases if case["C_Lite"] is not None and component_of[case["id"]] != fold]
        test_lite = [case for case in test_cases if case["C_Lite"] is not None]
        assert train_lite and test_lite
        fold_predictions: dict[str, dict[str, float]] = defaultdict(dict)

        # Existing univariate dimensionless candidates: C = Delta * q(x).
        dim_rows = [
            {
                "case": case,
                "features": cached_features[case["id"]],
                "q_observed": float(case["C_Lite"]) / int(case["source_seconds"]),
            }
            for case in train_lite
        ]
        for name, feature_names in DIMENSIONLESS_FEATURES.items():
            fitted = dim_model.fit(dim_rows, feature_names)
            fit_parameters[name][str(fold)] = fitted
            for case in test_cases:
                row = {"features": cached_features[case["id"]]}
                q_hat = dim_model.predict_q(fitted, row)
                fold_predictions[name][case["id"]] = int(case["source_seconds"]) * q_hat

        # Existing raw-C OLS feature family, now fitted across all n without a branch.
        fitted_raw_all = fit_raw(train_lite)
        fit_parameters["raw_ohlcv_ols_all"][str(fold)] = {
            "mean": fitted_raw_all["mean"].tolist(),
            "scale": fitted_raw_all["scale"].tolist(),
            "beta": fitted_raw_all["beta"].tolist(),
            "numerically_constant_features": fitted_raw_all["numerically_constant_features"],
            "rank": fitted_raw_all["rank"], "columns": fitted_raw_all["columns"],
            "singular_values": fitted_raw_all["singular_values"].tolist(),
            "training_rows": fitted_raw_all["training_rows"],
        }
        for case in test_cases:
            fold_predictions["raw_ohlcv_ols_all"][case["id"]] = predict_raw(case, fitted_raw_all)

        # Existing long-only candidate. Integer output quantization is part of this candidate.
        train_long = [case for case in train_lite if int(case["bars"]) >= 21]
        if len(train_long) >= len(raw_model.FEATURE_NAMES) + 1:
            fitted_long = fit_raw(train_long)
            fit_parameters["raw_ohlcv_ols_long_rounded"][str(fold)] = {
                "mean": fitted_long["mean"].tolist(),
                "scale": fitted_long["scale"].tolist(),
                "beta": fitted_long["beta"].tolist(),
                "numerically_constant_features": fitted_long["numerically_constant_features"],
                "rank": fitted_long["rank"], "columns": fitted_long["columns"],
                "singular_values": fitted_long["singular_values"].tolist(),
                "training_rows": fitted_long["training_rows"],
            }
            for case in test_cases:
                if int(case["bars"]) >= 21:
                    raw_hat = predict_raw(case, fitted_long)
                    fold_predictions["raw_ohlcv_ols_long_rounded"][case["id"]] = float(math.floor(raw_hat + 0.5))

        for model_name, preds in fold_predictions.items():
            for case in test_cases:
                if case["id"] not in preds:
                    continue
                c_hat = preds[case["id"]]
                if case["C_Lite"] is None:
                    lo = float(case["C_Character_interval"]["lower_inclusive"])
                    hi = float(case["C_Character_interval"]["upper_exclusive"])
                    compatible: bool | None = bool(lo <= c_hat < hi)
                    residual = None
                    observed = None
                else:
                    observed = float(case["C_Lite"])
                    residual = c_hat - observed
                    compatible = None
                record = {
                    "model": model_name,
                    "fold_component": fold,
                    "case_id": case["id"],
                    "source_seconds": int(case["source_seconds"]),
                    "bars": int(case["bars"]),
                    "measurement_kind": case["C_measurement_kind"],
                    "C_Lite_observed": observed,
                    "C_hat": c_hat,
                    "residual_hat_minus_Lite": residual,
                    "Character_lower": case["C_Character_interval"]["lower_inclusive"] if compatible is not None else None,
                    "Character_upper_exclusive": case["C_Character_interval"]["upper_exclusive"] if compatible is not None else None,
                    "Character_compatible": compatible,
                }
                predictions[model_name].append(record)

        fold_summaries.append({
            "component": fold,
            "train_Lite": len(train_lite),
            "test_Lite": len(test_lite),
            "test_by_source_seconds": {
                str(delta): sum(int(c["source_seconds"]) == delta for c in test_lite)
                for delta in sorted({int(c["source_seconds"]) for c in test_lite})
            },
            "models": {
                name: summarize_metric(
                    [float(c["C_Lite"]) for c in test_lite if c["id"] in fold_predictions[name]],
                    [fold_predictions[name][c["id"]] for c in test_lite if c["id"] in fold_predictions[name]],
                )
                for name in fold_predictions
            },
        })

    model_metrics: dict[str, Any] = {}
    for model_name, rows in predictions.items():
        lite_rows = [row for row in rows if row["C_Lite_observed"] is not None]
        char_rows = [row for row in rows if row["Character_compatible"] is not None]
        model_metrics[model_name] = {
            "all_Lite": summarize_metric(
                [row["C_Lite_observed"] for row in lite_rows],
                [row["C_hat"] for row in lite_rows],
            ),
            "Lite_by_source_seconds": {
                str(delta): summarize_metric(
                    [row["C_Lite_observed"] for row in lite_rows if row["source_seconds"] == delta],
                    [row["C_hat"] for row in lite_rows if row["source_seconds"] == delta],
                )
                for delta in sorted({row["source_seconds"] for row in lite_rows})
            },
            "Lite_short_n_lt_21": summarize_metric(
                [row["C_Lite_observed"] for row in lite_rows if row["bars"] < 21],
                [row["C_hat"] for row in lite_rows if row["bars"] < 21],
            ),
            "Lite_long_n_ge_21": summarize_metric(
                [row["C_Lite_observed"] for row in lite_rows if row["bars"] >= 21],
                [row["C_hat"] for row in lite_rows if row["bars"] >= 21],
            ),
            "Character_only_compatible": sum(bool(row["Character_compatible"]) for row in char_rows),
            "Character_only_scored": len(char_rows),
        }

    import csv

    residual_rows = [row for rows in predictions.values() for row in rows]
    fields = list(residual_rows[0])
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(residual_rows)

    output = {
        "status": "existing_candidates_reaudited_by_disjoint_temporal_components",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "scope": "Same-symbol case windows are joined when their physical OHLCV time coverage intersects, across source resolutions. Each fold excludes one entire connected component.",
        "blindness_limit": "All labels were already available; these are disjoint-window cross-validation folds, not a prospective or human-blind test, and all components remain from a small number of dates.",
        "candidate_definitions": {
            "linear_n": "C_hat = Delta * OLS(C_Lite/Delta ~ standardized n)",
            "log_n": "C_hat = Delta * OLS(C_Lite/Delta ~ standardized ln(n))",
            "normalized_ohlcv": "C_hat = Delta * OLS(C_Lite/Delta ~ standardized [ln(n), range_bp, close_path_bp, signed_efficiency, volume_weighted_body_bp, ln1p(mean_volume), volume_HHI])",
            "raw_ohlcv_ols_all": "C_hat = OLS(C_Lite ~ standardized [ln(n), ln(Delta), range_bp, close_path_bp, signed_efficiency, volume_weighted_body_bp, ln1p(mean_volume), volume_HHI])",
            "raw_ohlcv_ols_long_rounded": "For n>=21 only: round-nearest-second OLS(C_Lite ~ same eight standardized features); training uses only n>=21 cases outside the held-out component.",
        },
        "components": components,
        "folds": fold_summaries,
        "aggregate_leave_component_out_metrics": model_metrics,
        "fold_fit_parameters": fit_parameters,
        "residual_rows": len(residual_rows),
        "residual_csv": str(RESIDUAL),
    }
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "components": [{k: c[k] for k in ("component", "cases", "Lite_cases", "Character_only_cases", "by_source_seconds")} for c in components],
        "folds": fold_summaries,
        "aggregate": model_metrics,
        "residual_rows": len(residual_rows),
        "files": {"result_json": str(RESULT), "residual_csv": str(RESIDUAL)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
