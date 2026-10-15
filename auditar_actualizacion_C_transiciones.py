r"""Falsifiable transition models for adjacent Lite windows.

This is a diagnostic model family, not a claim about the indicator source.
It uses only exact-prefix adjacent cases from master_all_C_cases.json, trains
outside the fixed temporal lockbox, and writes both teacher-forced and recursive
holdout residuals.

Run with Python 3 and NumPy:
    python G:\trading\guias\analisis\auditar_actualizacion_C_transiciones.py
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "master_all_C_cases.json"
RESULT = ROOT / "resultado_C_transiciones_dinamicas.json"
RESIDUAL = ROOT / "residuos_C_transiciones_dinamicas.csv"
HOLDOUT_START = int(dt.datetime(2026, 10, 12, 18, 54, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_END = int(dt.datetime(2026, 10, 12, 19, 30, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_DAY = dt.date(2026, 10, 13)

FEATURES = {
    "state_scalar": ["C_previous", "ln_n", "ln_delta_seconds"],
    "prefix_state": [
        "C_previous", "ln_n", "ln_delta_seconds", "window_range_bp",
        "close_path_bp", "signed_efficiency", "volume_weighted_body_bp",
        "ln_1p_mean_volume", "volume_hhi",
    ],
    "prefix_plus_entering_bar": [
        "C_previous", "ln_n", "ln_delta_seconds", "window_range_bp",
        "close_path_bp", "signed_efficiency", "volume_weighted_body_bp",
        "ln_1p_mean_volume", "volume_hhi", "entry_range_over_prefix_range",
        "entry_body_bp", "entry_log_volume_relative_to_prefix_mean",
        "entry_close_gap_bp",
    ],
}


def is_holdout(case: dict[str, Any]) -> bool:
    bars = case["OHLCV"]
    start, end = int(bars[0]["time"]), int(bars[-1]["time"])
    start_day = dt.datetime.fromtimestamp(start, dt.timezone.utc).date()
    return start_day == HOLDOUT_DAY or (
        start_day == dt.date(2026, 10, 12)
        and start <= HOLDOUT_END
        and end >= HOLDOUT_START
    )


def prefix_features(previous: dict[str, Any], entering: dict[str, Any]) -> dict[str, float]:
    bars = previous["OHLCV"]
    opens = np.asarray([float(b["open"]) for b in bars])
    highs = np.asarray([float(b["high"]) for b in bars])
    lows = np.asarray([float(b["low"]) for b in bars])
    closes = np.asarray([float(b["close"]) for b in bars])
    volumes = np.asarray([float(b["volume"]) for b in bars])
    n = len(bars)
    delta = int(previous["source_seconds"])
    base = float(closes[0])
    path = float(np.abs(np.diff(closes)).sum())
    total_volume = float(volumes.sum())
    window_range = float(highs.max() - lows.min())
    mean_volume = float(volumes.mean())
    entry_range = float(entering["high"] - entering["low"])
    return {
        "C_previous": float(previous["C_Lite"]),
        "ln_n": math.log(n),
        "ln_delta_seconds": math.log(delta),
        "window_range_bp": window_range / base * 10_000,
        "close_path_bp": path / base * 10_000,
        "signed_efficiency": float((closes[-1] - closes[0]) / path) if path else 0.0,
        "volume_weighted_body_bp": (
            float(np.sum(volumes * (closes - opens)) / total_volume / base * 10_000)
            if total_volume else 0.0
        ),
        "ln_1p_mean_volume": math.log1p(mean_volume),
        "volume_hhi": float(np.sum((volumes / total_volume) ** 2)) if total_volume else 0.0,
        "entry_range_over_prefix_range": entry_range / window_range if window_range else 0.0,
        "entry_body_bp": float(entering["close"] - entering["open"]) / base * 10_000,
        "entry_log_volume_relative_to_prefix_mean": (
            math.log1p(float(entering["volume"])) - math.log1p(mean_volume)
        ),
        "entry_close_gap_bp": float(entering["close"] - closes[-1]) / base * 10_000,
    }


def metric(observed: list[float], predicted: list[float]) -> dict[str, Any]:
    if not observed:
        return {"n": 0, "MAE": None, "RMSE": None, "max_abs_residual": None, "within_1": 0}
    residual = np.asarray(predicted, dtype=float) - np.asarray(observed, dtype=float)
    return {
        "n": int(len(residual)),
        "MAE": float(np.mean(np.abs(residual))),
        "RMSE": float(np.sqrt(np.mean(residual**2))),
        "max_abs_residual": float(np.max(np.abs(residual))),
        "within_1": int(np.sum(np.abs(residual) <= 1.0 + 1e-9)),
    }


def fit_model(rows: list[dict[str, Any]], feature_names: list[str]) -> dict[str, Any]:
    x_raw = np.asarray([[r["x"][k] for k in feature_names] for r in rows], dtype=float)
    y = np.asarray([r["delta_C"] for r in rows], dtype=float)
    means = x_raw.mean(axis=0)
    scales = x_raw.std(axis=0)
    scales[scales == 0] = 1.0
    x = np.column_stack([np.ones(len(rows)), (x_raw - means) / scales])
    beta, _, rank, singular_values = np.linalg.lstsq(x, y, rcond=None)
    return {
        "features": feature_names,
        "mean": means.tolist(),
        "scale": scales.tolist(),
        "beta_intercept_then_standardized_features": beta.tolist(),
        "training_design_rank": int(rank),
        "training_rows": int(len(rows)),
        "training_columns_including_intercept": int(x.shape[1]),
        "training_singular_values": singular_values.tolist(),
    }


def predict_delta(model: dict[str, Any], row: dict[str, Any], c_previous: float | None = None) -> float:
    features = model["features"]
    means = np.asarray(model["mean"], dtype=float)
    scales = np.asarray(model["scale"], dtype=float)
    beta = np.asarray(model["beta_intercept_then_standardized_features"], dtype=float)
    x = np.asarray([
        (float(c_previous) if k == "C_previous" and c_previous is not None else row["x"][k])
        for k in features
    ])
    return float(beta[0] + np.dot(beta[1:], (x - means) / scales))


def recursive_predictions(rows: list[dict[str, Any]], model: dict[str, Any]) -> dict[str, float]:
    by_track: dict[tuple[int, int], list[dict[str, Any]]] = {}
    for row in rows:
        key = (int(row["current"]["source_seconds"]), int(row["current"]["START_unix"]))
        by_track.setdefault(key, []).append(row)
    predictions: dict[str, float] = {}
    for track in by_track.values():
        track.sort(key=lambda r: int(r["current"]["END_unix"]))
        predicted_previous: float | None = None
        last_current_end: int | None = None
        for row in track:
            previous_end = int(row["previous"]["END_unix"])
            current_end = int(row["current"]["END_unix"])
            # Start/restart a replay segment at a known measured C whenever a
            # missing pair breaks the exact adjacent chain.
            if predicted_previous is None or previous_end != last_current_end:
                predicted_previous = float(row["previous"]["C_Lite"])
            delta_hat = predict_delta(model, row, c_previous=predicted_previous)
            predicted_current = predicted_previous + delta_hat
            predictions[row["current"]["id"]] = predicted_current
            predicted_previous = predicted_current
            last_current_end = current_end
    return predictions


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
        x = prefix_features(previous, current["OHLCV"][-1])
        rows.append({
            "previous": previous,
            "current": current,
            "x": x,
            "delta_C": float(current["C_Lite"] - previous["C_Lite"]),
            "holdout": is_holdout(current),
            "train_eligible": not is_holdout(previous) and not is_holdout(current),
        })
    training = [r for r in rows if r["train_eligible"]]
    holdout = [r for r in rows if r["holdout"]]
    assert len(rows) == 87 and len(training) > 14 and len(holdout) > 0
    training_by_delta: dict[str, int] = {}
    holdout_by_delta: dict[str, int] = {}
    for row in training:
        key = str(row["current"]["source_seconds"])
        training_by_delta[key] = training_by_delta.get(key, 0) + 1
    for row in holdout:
        key = str(row["current"]["source_seconds"])
        holdout_by_delta[key] = holdout_by_delta.get(key, 0) + 1

    models: dict[str, Any] = {}
    residual_rows: list[dict[str, Any]] = []
    for model_name, feature_names in FEATURES.items():
        model = fit_model(training, feature_names)
        train_pred_delta = [predict_delta(model, r) for r in training]
        test_pred_delta = [predict_delta(model, r) for r in holdout]
        teacher_forced = [float(r["previous"]["C_Lite"]) + p for r, p in zip(holdout, test_pred_delta)]
        recursive = recursive_predictions(holdout, model)
        recursive_test = [recursive[r["current"]["id"]] for r in holdout]
        per_delta: dict[str, Any] = {}
        for d in sorted({int(r["current"]["source_seconds"]) for r in holdout}):
            inds = [i for i, row in enumerate(holdout) if int(row["current"]["source_seconds"]) == d]
            per_delta[str(d)] = {
                "teacher_forced": metric(
                    [float(holdout[i]["current"]["C_Lite"]) for i in inds],
                    [teacher_forced[i] for i in inds],
                ),
                "recursive": metric(
                    [float(holdout[i]["current"]["C_Lite"]) for i in inds],
                    [recursive_test[i] for i in inds],
                ),
            }
        models[model_name] = {
            **model,
            "training_teacher_forced_delta_fit": metric(
                [r["delta_C"] for r in training], train_pred_delta
            ),
            "holdout_teacher_forced_C": metric(
                [float(r["current"]["C_Lite"]) for r in holdout], teacher_forced
            ),
            "holdout_recursive_C": metric(
                [float(r["current"]["C_Lite"]) for r in holdout], recursive_test
            ),
            "holdout_by_source_seconds": per_delta,
        }
        for row, delta_hat, c_teacher, c_recursive in zip(holdout, test_pred_delta, teacher_forced, recursive_test):
            residual_rows.append({
                "model": model_name,
                "case_id": row["current"]["id"],
                "source_seconds": row["current"]["source_seconds"],
                "START": row["current"]["START"],
                "END": row["current"]["END"],
                "n_previous": row["previous"]["bars"],
                "C_previous_observed": row["previous"]["C_Lite"],
                "C_observed": row["current"]["C_Lite"],
                "delta_C_observed": row["delta_C"],
                "delta_C_predicted_teacher_forced": delta_hat,
                "C_predicted_teacher_forced": c_teacher,
                "residual_teacher_forced": c_teacher - float(row["current"]["C_Lite"]),
                "C_predicted_recursive": c_recursive,
                "residual_recursive": c_recursive - float(row["current"]["C_Lite"]),
            })

    results = {
        "status": "transition_candidates_rejected_for_unified_generation",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "pair_definition": "same requested START; END advances one source_seconds; prior OHLCV exactly equals current OHLCV prefix; both labels Lite measured",
        "partition": {
            "rule": "fixed temporal rule from the independent audit; exclude 2026-10-12 18:54-19:30 UTC intersections and all 2026-10-13 cases from fitting",
            "all_adjacent_pairs": len(rows),
            "training_pairs": len(training),
            "training_by_source_seconds": training_by_delta,
            "holdout_pairs": len(holdout),
            "holdout_by_source_seconds": holdout_by_delta,
            "blindness_note": "Labels were already collected. The partition is implemented before fitting, but this is not a genuinely blind or prospective study.",
        },
        "model_interpretation": "Each OLS model predicts delta_C from measured previous C and fixed physical window/entry features. Teacher-forced scoring uses observed C_previous for each step; recursive scoring carries the predicted C through contiguous holdout steps and seeds each disconnected segment with its measured initial C. Neither score establishes the indicator's source algorithm.",
        "models": models,
        "residual_csv": str(RESIDUAL),
    }
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(residual_rows[0]))
        writer.writeheader()
        writer.writerows(residual_rows)
    RESULT.write_text(json.dumps(results, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": results["status"],
        "partition": results["partition"],
        "models": {
            name: {
                "features": model["features"],
                "training_teacher_forced_delta_fit": model["training_teacher_forced_delta_fit"],
                "holdout_teacher_forced_C": model["holdout_teacher_forced_C"],
                "holdout_recursive_C": model["holdout_recursive_C"],
                "holdout_by_source_seconds": model["holdout_by_source_seconds"],
            }
            for name, model in models.items()
        },
        "residual_csv": str(RESIDUAL),
        "result_json": str(RESULT),
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
