r"""Test one-scale-time laws C = Delta * g(n, normalized OHLCV).

Fits low-complexity dimensionless candidates only on the fixed non-holdout
Lite cases, then scores the same temporal holdout used by the independent audit.
No absolute prices or case-specific rules enter the feature vector.

Run with Python 3 and NumPy:
    python G:\trading\guias\analisis\probar_ley_dimensionless_C.py
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
RESULT = ROOT / "resultado_C_ley_dimensionless.json"
RESIDUAL = ROOT / "residuos_C_ley_dimensionless.csv"
HOLDOUT_START = int(dt.datetime(2026, 10, 12, 18, 54, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_END = int(dt.datetime(2026, 10, 12, 19, 30, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_DAY = dt.date(2026, 10, 13)

MODEL_FEATURES = {
    "constant_q": [],
    "linear_n": ["n"],
    "log_n": ["ln_n"],
    "normalized_ohlcv": [
        "ln_n", "window_range_bp", "close_path_bp", "signed_efficiency",
        "volume_weighted_body_bp", "ln_1p_mean_volume", "volume_hhi",
    ],
}


def is_holdout(case: dict[str, Any]) -> bool:
    bars = case["OHLCV"]
    start, end = int(bars[0]["time"]), int(bars[-1]["time"])
    day = dt.datetime.fromtimestamp(start, dt.timezone.utc).date()
    return day == HOLDOUT_DAY or (
        day == dt.date(2026, 10, 12) and start <= HOLDOUT_END and end >= HOLDOUT_START
    )


def features(case: dict[str, Any]) -> dict[str, float]:
    bars = case["OHLCV"]
    n = len(bars)
    opens = np.asarray([float(b["open"]) for b in bars])
    highs = np.asarray([float(b["high"]) for b in bars])
    lows = np.asarray([float(b["low"]) for b in bars])
    closes = np.asarray([float(b["close"]) for b in bars])
    volumes = np.asarray([float(b["volume"]) for b in bars])
    base = float(closes[0])
    path = float(np.abs(np.diff(closes)).sum())
    total_volume = float(volumes.sum())
    return {
        "n": float(n),
        "ln_n": math.log(n),
        "window_range_bp": float((highs.max() - lows.min()) / base * 10_000),
        "close_path_bp": float(path / base * 10_000),
        "signed_efficiency": float((closes[-1] - closes[0]) / path) if path else 0.0,
        "volume_weighted_body_bp": (
            float(np.sum(volumes * (closes - opens)) / total_volume / base * 10_000)
            if total_volume else 0.0
        ),
        "ln_1p_mean_volume": math.log1p(float(volumes.mean())),
        "volume_hhi": float(np.sum((volumes / total_volume) ** 2)) if total_volume else 0.0,
    }


def metric(observed: list[float], predicted: list[float]) -> dict[str, Any]:
    if not observed:
        return {"n": 0, "MAE": None, "RMSE": None, "max_abs_residual": None, "within_1": 0}
    residual = np.asarray(predicted, dtype=float) - np.asarray(observed, dtype=float)
    return {
        "n": len(residual),
        "MAE": float(np.mean(np.abs(residual))),
        "RMSE": float(np.sqrt(np.mean(residual**2))),
        "max_abs_residual": float(np.max(np.abs(residual))),
        "within_1": int(np.sum(np.abs(residual) <= 1.0 + 1e-9)),
    }


def fit(rows: list[dict[str, Any]], feature_names: list[str]) -> dict[str, Any]:
    y = np.asarray([r["q_observed"] for r in rows], dtype=float)
    if not feature_names:
        return {
            "features": [], "mean": [], "scale": [],
            "beta_intercept_then_standardized_features": [float(y.mean())],
            "training_rank": 1, "training_rows": len(rows),
        }
    raw = np.asarray([[r["features"][k] for k in feature_names] for r in rows], dtype=float)
    mean = raw.mean(axis=0)
    scale = raw.std(axis=0)
    scale[scale == 0] = 1.0
    design = np.column_stack([np.ones(len(rows)), (raw - mean) / scale])
    beta, _, rank, singular = np.linalg.lstsq(design, y, rcond=None)
    return {
        "features": feature_names,
        "mean": mean.tolist(),
        "scale": scale.tolist(),
        "beta_intercept_then_standardized_features": beta.tolist(),
        "training_rank": int(rank),
        "training_rows": len(rows),
        "training_columns": int(design.shape[1]),
        "training_singular_values": singular.tolist(),
    }


def predict_q(model: dict[str, Any], row: dict[str, Any]) -> float:
    beta = np.asarray(model["beta_intercept_then_standardized_features"], dtype=float)
    if not model["features"]:
        return float(beta[0])
    raw = np.asarray([row["features"][k] for k in model["features"]], dtype=float)
    normalized = (raw - np.asarray(model["mean"])) / np.asarray(model["scale"])
    return float(beta[0] + np.dot(beta[1:], normalized))


def main() -> None:
    master_bytes = MASTER.read_bytes()
    cases = json.loads(master_bytes.decode("utf-8"))["cases"]
    rows = []
    for case in cases:
        row = {
            "case": case,
            "features": features(case),
            "partition": "locked_holdout" if is_holdout(case) else "development",
        }
        if case["C_Lite"] is not None:
            row["q_observed"] = float(case["C_Lite"]) / int(case["source_seconds"])
            rows.append(row)
        else:
            rows.append(row)
    train = [r for r in rows if r["case"]["C_Lite"] is not None and r["partition"] == "development"]
    holdout = [r for r in rows if r["case"]["C_Lite"] is not None and r["partition"] == "locked_holdout"]
    assert (len(rows), len(train), len(holdout)) == (179, 51, 94)
    models: dict[str, Any] = {}
    residual_rows: list[dict[str, Any]] = []
    for model_name, feature_names in MODEL_FEATURES.items():
        model = fit(train, feature_names)
        pred_q = {r["case"]["id"]: predict_q(model, r) for r in rows if r["case"]["C_Lite"] is not None}
        metrics: dict[str, Any] = {}
        for split_name, split_rows in (("development", train), ("locked_holdout", holdout)):
            hats = [int(r["case"]["source_seconds"]) * pred_q[r["case"]["id"]] for r in split_rows]
            observed = [float(r["case"]["C_Lite"]) for r in split_rows]
            metrics[split_name] = metric(observed, hats)
            for label, predicate in (
                ("short_n_lt_21", lambda c: int(c["bars"]) < 21),
                ("long_n_ge_21", lambda c: int(c["bars"]) >= 21),
            ):
                group = [r for r in split_rows if predicate(r["case"])]
                group_hats = [int(r["case"]["source_seconds"]) * pred_q[r["case"]["id"]] for r in group]
                metrics[f"{split_name}_{label}"] = metric(
                    [float(r["case"]["C_Lite"]) for r in group], group_hats
                )
            metrics[f"{split_name}_by_source_seconds"] = {
                str(delta): metric(
                    [float(r["case"]["C_Lite"]) for r in split_rows if int(r["case"]["source_seconds"]) == delta],
                    [int(r["case"]["source_seconds"]) * pred_q[r["case"]["id"]]
                     for r in split_rows if int(r["case"]["source_seconds"]) == delta],
                )
                for delta in sorted({int(r["case"]["source_seconds"]) for r in split_rows})
            }
        character_compatible = 0
        for row in rows:
            case = row["case"]
            if case["C_Lite"] is None:
                c_hat = int(case["source_seconds"]) * predict_q(model, row)
                interval = case["C_Character_interval"]
                character_compatible += int(interval["lower_inclusive"] <= c_hat < interval["upper_exclusive"])
        models[model_name] = {
            **model,
            "formula": "C_hat = Delta * (beta0 + sum_j beta_j * standardized(feature_j))",
            "metrics": metrics,
            "Character_only_compatible": character_compatible,
            "Character_only_cases": 34,
        }
        for row in rows:
            case = row["case"]
            c_hat = int(case["source_seconds"]) * predict_q(model, row)
            if case["C_Lite"] is not None:
                c_obs = float(case["C_Lite"])
                residual = c_hat - c_obs
                compatible = None
                c_interval = None
            else:
                c_obs = None
                residual = None
                c_interval = case["C_Character_interval"]
                compatible = bool(c_interval["lower_inclusive"] <= c_hat < c_interval["upper_exclusive"])
            residual_rows.append({
                "model": model_name,
                "case_id": case["id"],
                "source_seconds": case["source_seconds"],
                "bars": case["bars"],
                "partition": row["partition"],
                "C_Lite_observed": c_obs,
                "C_hat": c_hat,
                "residual_hat_minus_Lite": residual,
                "Character_interval": json.dumps(c_interval, ensure_ascii=False) if c_interval else None,
                "Character_compatible": compatible,
            })

    output = {
        "status": "dimensionless_candidates_rejected_for_unified_generation",
        "master_sha256": hashlib.sha256(master_bytes).hexdigest(),
        "equation_family": "C = Delta * g(n, normalized OHLCV); no absolute price, no piecewise n threshold",
        "partition": {
            "rule": "same fixed temporal rule as independent audit; split determined from timestamps before fitting",
            "training_Lite": len(train),
            "training_by_source_seconds": {
                str(d): sum(int(r["case"]["source_seconds"]) == d for r in train)
                for d in sorted({int(r["case"]["source_seconds"]) for r in train})
            },
            "holdout_Lite": len(holdout),
            "holdout_by_source_seconds": {
                str(d): sum(int(r["case"]["source_seconds"]) == d for r in holdout)
                for d in sorted({int(r["case"]["source_seconds"]) for r in holdout})
            },
            "blindness_note": "All labels were already collected; the fit excludes the temporal holdout, but this is not prospective or genuinely human-blind.",
        },
        "models": models,
        "residual_csv": str(RESIDUAL),
    }
    with RESIDUAL.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(residual_rows[0]))
        writer.writeheader()
        writer.writerows(residual_rows)
    RESULT.write_text(json.dumps(output, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "partition": output["partition"],
        "models": {
            name: {
                "training": value["metrics"]["development"],
                "holdout": value["metrics"]["locked_holdout"],
                "holdout_short": value["metrics"]["locked_holdout_short_n_lt_21"],
                "holdout_long": value["metrics"]["locked_holdout_long_n_ge_21"],
                "Character_only_compatible": value["Character_only_compatible"],
            }
            for name, value in models.items()
        },
        "files": {"result_json": str(RESULT), "residual_csv": str(RESIDUAL)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
