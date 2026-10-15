"""Independent, reproducible audit of a short-regime rule and a long-regime candidate.

Run from any directory with Python 3 and NumPy:
    python G:\\trading\\guias\\analisis\\analizar_modelo_C_independiente.py

The regression is deliberately a falsifiable baseline, not a claim that its fitted
coefficients are the indicator's source algorithm. Character-only values are scored
against their intervals and are never treated as Lite decimal labels.
"""
from __future__ import annotations

import csv
import collections
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
MASTER_PATH = ROOT / "master_all_C_cases.json"
SWEEP_PATH = ROOT / "C_barrido_END_1855_1920_1924_15s.json"
TIMEFRAME_PATH = ROOT / "C_test_timeframes_1900_1920.json"
MATRIX_PATH = ROOT / "C_cruce_doble.json"
RESIDUAL_PATH = ROOT / "residuos_C_modelo_independiente.csv"
CONTROL_RESIDUAL_PATH = ROOT / "residuos_C_controles_modelo.csv"
TRANSITION_PATH = ROOT / "transiciones_C_barrido_independiente.csv"
RESULT_PATH = ROOT / "resultado_C_modelo_independiente.json"

SHORT_DENOMINATOR = 183.0
HOLDOUT_START = int(dt.datetime(2026, 10, 12, 18, 54, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_END = int(dt.datetime(2026, 10, 12, 19, 30, tzinfo=dt.timezone.utc).timestamp())
HOLDOUT_DAY = dt.date(2026, 10, 13)

FEATURE_NAMES = [
    "ln_n",
    "ln_delta_seconds",
    "window_range_bp",
    "close_path_bp",
    "signed_efficiency",
    "volume_weighted_body_bp",
    "ln_1p_mean_volume",
    "volume_hhi",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def case_key(case: dict[str, Any]) -> tuple[int, int, int]:
    bars = case["OHLCV"]
    delta = case.get("source_seconds", case.get("dt"))
    return int(delta), int(bars[0]["time"]), int(bars[-1]["time"])


def is_holdout(case: dict[str, Any]) -> bool:
    """Fixed by timestamp before fitting; no C label or price value is consulted."""
    bars = case["OHLCV"]
    start, end = int(bars[0]["time"]), int(bars[-1]["time"])
    start_day = dt.datetime.fromtimestamp(start, dt.timezone.utc).date()
    return start_day == HOLDOUT_DAY or (
        start_day == dt.date(2026, 10, 12) and start <= HOLDOUT_END and end >= HOLDOUT_START
    )


def validate_master(cases: list[dict[str, Any]]) -> dict[str, Any]:
    assert len(cases) == 179
    ids = [case["id"] for case in cases]
    assert len(set(ids)) == len(ids)
    assert sum(case["C_Lite"] is not None for case in cases) == 145
    assert sum(case["C_Lite"] is None for case in cases) == 34
    for case in cases:
        bars = case["OHLCV"]
        assert case["volume_complete"] and len(bars) == case["bars"]
        delta = int(case["source_seconds"])
        assert all(int(b["time"]) - int(a["time"]) == delta for a, b in zip(bars, bars[1:]))
        assert int(case["dt"]) == delta
        for bar in bars:
            assert bar["volume"] is not None and float(bar["volume"]) >= 0
            assert bar["low"] <= min(bar["open"], bar["close"])
            assert max(bar["open"], bar["close"]) <= bar["high"]
    categorical_fields = (
        "symbol", "mode", "profile", "session", "timezone", "contract_adjustment"
    )
    metadata_counts = {
        field: dict(sorted(collections.Counter(str(c.get(field)) for c in cases).items()))
        for field in categorical_fields
    }
    resolution_counts = {
        field: dict(sorted(collections.Counter(str(c.get(field)) for c in cases).items()))
        for field in ("source_seconds", "chart_seconds")
    }
    return {
        "cases": len(cases),
        "Lite_measured": sum(c["C_Lite"] is not None for c in cases),
        "Character_only": sum(c["C_Lite"] is None for c in cases),
        "all_OHLCV_complete": True,
        "categorical_metadata_counts": metadata_counts,
        "resolution_counts": resolution_counts,
        "all_source_intervals_match_chart_intervals": all(
            int(c["source_seconds"]) == int(c["chart_seconds"]) for c in cases
        ),
    }


def identical_input_audit(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Find cases with byte-equivalent candle content despite different requested anchors."""
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = collections.defaultdict(list)
    for case in cases:
        bars = case["OHLCV"]
        signature = (
            int(case["source_seconds"]),
            tuple(
                (
                    int(b["time"]),
                    float(b["open"]),
                    float(b["high"]),
                    float(b["low"]),
                    float(b["close"]),
                    float(b["volume"]),
                )
                for b in bars
            ),
        )
        groups[signature].append(case)

    duplicated = [group for group in groups.values() if len(group) > 1]
    reports = []
    for group in duplicated:
        lite_values = [float(c["C_Lite"]) for c in group if c["C_Lite"] is not None]
        all_intervals = [c["C_Character_interval"] for c in group if c["C_Character_interval"]]
        lite_consistent_with_intervals = all(
            interval["lower_inclusive"] <= value < interval["upper_exclusive"]
            for value in lite_values
            for interval in all_intervals
        )
        intervals_overlap = (
            max(x["lower_inclusive"] for x in all_intervals)
            < min(x["upper_exclusive"] for x in all_intervals)
            if all_intervals
            else None
        )
        reports.append(
            {
                "dt_seconds": int(group[0]["source_seconds"]),
                "n_bars": int(group[0]["bars"]),
                "case_ids": [c["id"] for c in group],
                "requested_STARTs": [c["START"] for c in group],
                "requested_ENDs": [c["END"] for c in group],
                "effective_START": group[0]["effective_START"],
                "effective_END": group[0]["effective_END"],
                "C_Lite_measurements": lite_values,
                "Character_intervals_overlap": intervals_overlap,
                "all_Lite_values_inside_all_Character_intervals": lite_consistent_with_intervals,
            }
        )
    return {
        "duplicate_groups": len(reports),
        "cases_in_duplicate_groups": sum(len(x) for x in duplicated),
        "groups": reports,
        "interpretation": "The repeated inputs differ only in requested anchors; the OHLCV arrays and their timestamps are identical. The compatible C labels support using the effective candle array as the input on these controls, but do not identify its generating function.",
    }


def context_transition_audit(cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare adjacent END updates that append the same physical OHLCV candle."""
    by_anchor = {
        (int(c["source_seconds"]), int(c["START_unix"]), int(c["END_unix"])): c
        for c in cases
    }
    transitions_by_entering_bar: dict[tuple[Any, ...], list[dict[str, Any]]] = collections.defaultdict(list)
    adjacent_pairs = 0
    for current in cases:
        delta = int(current["source_seconds"])
        previous = by_anchor.get((delta, int(current["START_unix"]), int(current["END_unix"]) - delta))
        if previous is None:
            continue
        if previous["OHLCV"] != current["OHLCV"][:-1]:
            continue
        if previous["C_Lite"] is None or current["C_Lite"] is None:
            continue
        adjacent_pairs += 1
        entering = current["OHLCV"][-1]
        candle_key = (
            delta,
            int(entering["time"]),
            float(entering["open"]),
            float(entering["high"]),
            float(entering["low"]),
            float(entering["close"]),
            float(entering["volume"]),
        )
        transitions_by_entering_bar[candle_key].append(
            {
                "dt_seconds": delta,
                "start": current["START"],
                "from_id": previous["id"],
                "to_id": current["id"],
                "n_before": int(previous["bars"]),
                "n_after": int(current["bars"]),
                "C_before": float(previous["C_Lite"]),
                "C_after": float(current["C_Lite"]),
                "delta_C": float(current["C_Lite"] - previous["C_Lite"]),
                "entering_time": int(entering["time"]),
                "entering_OHLCV": {k: entering[k] for k in ("open", "high", "low", "close", "volume")},
            }
        )

    repeated = [group for group in transitions_by_entering_bar.values() if len(group) > 1]
    conflicting_groups = []
    same_scalar_state_conflicts = []
    same_count_state_repeats = 0
    same_count_state_conflicts = 0
    for group in repeated:
        deltas = [float(t["delta_C"]) for t in group]
        conflict = max(deltas) - min(deltas) > 1e-7
        if conflict:
            conflict_record = {
                "dt_seconds": group[0]["dt_seconds"],
                "entering_time": group[0]["entering_time"],
                "entering_OHLCV": group[0]["entering_OHLCV"],
                "contexts": group,
                "delta_C_min": min(deltas),
                "delta_C_max": max(deltas),
            }
            conflicting_groups.append(conflict_record)
            by_previous: dict[int, list[dict[str, Any]]] = collections.defaultdict(list)
            for t in group:
                by_previous[round(float(t["C_before"]) * 1e7)].append(t)
            for previous_key, contexts in by_previous.items():
                context_deltas = [float(t["delta_C"]) for t in contexts]
                if len(contexts) > 1 and max(context_deltas) - min(context_deltas) > 1e-7:
                    same_scalar_state_conflicts.append(
                        {
                            "dt_seconds": group[0]["dt_seconds"],
                            "entering_time": group[0]["entering_time"],
                            "entering_OHLCV": group[0]["entering_OHLCV"],
                            "C_before": float(contexts[0]["C_before"]),
                            "contexts": contexts,
                            "delta_C_min": min(context_deltas),
                            "delta_C_max": max(context_deltas),
                        }
                    )
            by_count_and_previous: dict[tuple[int, int], list[dict[str, Any]]] = collections.defaultdict(list)
            for t in group:
                signature = (int(t["n_before"]), round(float(t["C_before"]) * 1e7))
                by_count_and_previous[signature].append(t)
            for contexts in by_count_and_previous.values():
                if len(contexts) > 1:
                    same_count_state_repeats += 1
                    context_deltas = [float(t["delta_C"]) for t in contexts]
                    if max(context_deltas) - min(context_deltas) > 1e-7:
                        same_count_state_conflicts += 1
    return {
        "adjacent_Lite_pairs_with_exact_OHLCV_prefix": adjacent_pairs,
        "distinct_entering_candles": len(transitions_by_entering_bar),
        "repeated_entering_candles": len(repeated),
        "repeated_candles_with_context_dependent_delta_C": len(conflicting_groups),
        "same_C_previous_and_same_entering_candle_with_different_delta": len(same_scalar_state_conflicts),
        "same_C_previous_same_n_and_same_entering_candle_repeated_keys": same_count_state_repeats,
        "same_C_previous_same_n_and_same_entering_candle_conflicts": same_count_state_conflicts,
        "same_scalar_state_conflicts": same_scalar_state_conflicts,
        "conflicting_candle_examples": conflicting_groups[:20],
        "interpretation": "At the captured C precision (previous C grouped to 1e-7), an update rule depending only on previous C and exact entering OHLCV is rejected where delta_C differs. The observed data require additional prefix state or another input; they do not distinguish bar count from richer path state because no exact (n, C_previous, entering OHLCV) key repeats.",
    }


def feature_vector(case: dict[str, Any]) -> np.ndarray:
    bars = case["OHLCV"]
    n = len(bars)
    delta = float(case["source_seconds"])
    base = float(bars[0]["close"])
    opens = np.asarray([float(b["open"]) for b in bars])
    highs = np.asarray([float(b["high"]) for b in bars])
    lows = np.asarray([float(b["low"]) for b in bars])
    closes = np.asarray([float(b["close"]) for b in bars])
    volumes = np.asarray([float(b["volume"]) for b in bars])
    path = float(np.abs(np.diff(closes)).sum())
    volume_sum = float(volumes.sum())
    volume_weighted_body = (
        float(np.sum(volumes * (closes - opens)) / volume_sum / base * 10_000)
        if volume_sum > 0
        else 0.0
    )
    volume_hhi = float(np.sum((volumes / volume_sum) ** 2)) if volume_sum > 0 else 0.0
    return np.asarray(
        [
            math.log(n),
            math.log(delta),
            float((highs.max() - lows.min()) / base * 10_000),
            float(path / base * 10_000),
            float((closes[-1] - closes[0]) / path) if path > 0 else 0.0,
            volume_weighted_body,
            math.log1p(float(volumes.mean())),
            volume_hhi,
        ],
        dtype=float,
    )


def fit_long_model(cases: list[dict[str, Any]]) -> dict[str, Any]:
    # Only measured Lite cases outside the fixed episode/day holdout can fit beta.
    train = [c for c in cases if c["C_Lite"] is not None and c["bars"] >= 21 and not is_holdout(c)]
    assert len(train) == 35, f"Unexpected development sample size: {len(train)}"
    return fit_ols(train)


def fit_ols(train: list[dict[str, Any]]) -> dict[str, Any]:
    x = np.vstack([feature_vector(c) for c in train])
    y = np.asarray([float(c["C_Lite"]) for c in train])
    mean = x.mean(axis=0)
    scale = x.std(axis=0)
    scale[scale == 0] = 1.0
    xz = (x - mean) / scale
    design = np.column_stack([np.ones(len(train)), xz])
    beta, _, rank, singular = np.linalg.lstsq(design, y, rcond=None)
    assert int(rank) == len(FEATURE_NAMES) + 1
    return {
        "train_cases": train,
        "mean": mean,
        "scale": scale,
        "beta": beta,
        "rank": int(rank),
        "singular_values": singular,
    }


def exact_input_signature(case: dict[str, Any]) -> tuple[Any, ...]:
    return (
        int(case.get("source_seconds", case.get("dt"))),
        tuple(
            (
                int(b["time"]),
                float(b["open"]),
                float(b["high"]),
                float(b["low"]),
                float(b["close"]),
                float(b["volume"]),
            )
            for b in case["OHLCV"]
        ),
    )


def control_signature_keys(cases: list[dict[str, Any]]) -> tuple[set[tuple[Any, ...]], dict[str, list[str]]]:
    """Resolve the named matrix, END sweep and timeframe controls back to master inputs."""
    by_anchor = {(int(c["dt"]), int(c["START_unix"]), int(c["END_unix"])): c for c in cases}
    matrix = read_json(MATRIX_PATH)["cases"]
    matrix_cases = []
    for row in matrix:
        def anchor_seconds(value: str) -> int:
            value = value if len(value) > 5 else value + ":00"
            stamp = dt.datetime.fromisoformat("2026-10-12T" + value + "+00:00")
            return int(stamp.timestamp())

        key = (int(row["dt"]), anchor_seconds(row["start"]), anchor_seconds(row["end"]))
        assert key in by_anchor, f"Could not resolve matrix row: {row}"
        matrix_cases.append(by_anchor[key])
    sweep_cases = read_json(SWEEP_PATH)["cases"]
    timeframe_cases = read_json(TIMEFRAME_PATH)["cases"]
    groups = {"matrix": matrix_cases, "sweep": sweep_cases, "timeframe": timeframe_cases}
    signatures: set[tuple[Any, ...]] = set()
    ids: dict[str, list[str]] = {}
    master_by_key = {case_key(c): c for c in cases}
    for name, rows in groups.items():
        matched = []
        for row in rows:
            key = case_key(row)
            assert key in master_by_key, f"Could not resolve {name} control: {row.get('id')}"
            case = master_by_key[key]
            signatures.add(exact_input_signature(case))
            matched.append(case["id"])
        ids[name] = matched
    return signatures, ids


def short_prediction(case: dict[str, Any]) -> float:
    n = len(case["OHLCV"])
    delta = float(case["source_seconds"])
    return delta * max(1.0, 10.0 * n / SHORT_DENOMINATOR)


def raw_prediction(case: dict[str, Any], fit: dict[str, Any]) -> float:
    if len(case["OHLCV"]) < 21:
        return short_prediction(case)
    z = (feature_vector(case) - fit["mean"]) / fit["scale"]
    return float(np.r_[1.0, z] @ fit["beta"])


def model_prediction(case: dict[str, Any], fit: dict[str, Any]) -> float:
    raw = raw_prediction(case, fit)
    if len(case["OHLCV"]) < 21:
        return raw
    # The long-regime measured values are integer to measurement precision.
    return float(math.floor(raw + 0.5))


def pearson(x: list[float], y: list[float]) -> float:
    xa, ya = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if xa.std() == 0 or ya.std() == 0:
        return float("nan")
    return float(np.corrcoef(xa, ya)[0, 1])


def average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[order[k]] = rank
        i = j
    return ranks


def spearman(x: list[float], y: list[float]) -> float:
    return pearson(average_ranks(x), average_ranks(y))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def metric_block(pred: list[float], observed: list[float]) -> dict[str, Any]:
    residuals = [float(p - y) for p, y in zip(pred, observed)]
    return {
        "n": len(residuals),
        "MAE": float(np.mean(np.abs(residuals))) if residuals else None,
        "RMSE": float(np.sqrt(np.mean(np.square(residuals)))) if residuals else None,
        "max_abs_residual": float(max(map(abs, residuals))) if residuals else None,
        "within_1": sum(abs(r) <= 1.0 + 1e-9 for r in residuals),
        "exact_within_1e-8": sum(abs(r) <= 1e-8 for r in residuals),
    }


def main() -> None:
    master_bytes = MASTER_PATH.read_bytes()
    master_hash = hashlib.sha256(master_bytes).hexdigest()
    master = json.loads(master_bytes)
    cases = master["cases"]
    validation = validate_master(cases)
    fit = fit_long_model(cases)
    train_cases = fit["train_cases"]

    prediction_rows: list[dict[str, Any]] = []
    by_key: dict[tuple[int, int, int], dict[str, Any]] = {}
    for case in cases:
        pred_raw = raw_prediction(case, fit)
        pred = model_prediction(case, fit)
        held = is_holdout(case)
        lite = case["C_Lite"]
        interval = case["C_Character_interval"]
        target_kind = "Lite_decimal" if lite is not None else "Character_interval_only"
        residual = float(pred - float(lite)) if lite is not None else None
        interval_ok = (
            bool(interval["lower_inclusive"] <= pred < interval["upper_exclusive"])
            if interval is not None
            else None
        )
        row = {
            "id": case["id"],
            "partition": "locked_holdout" if held else "development_pool",
            "model_branch": "short_n_lt_21" if case["bars"] < 21 else "long_OLS_then_integer_round",
            "dt_seconds": case["source_seconds"],
            "n_bars": case["bars"],
            "target_kind": target_kind,
            "C_hat_raw": pred_raw,
            "C_hat": pred,
            "C_Lite": lite,
            "residual_hat_minus_Lite": residual,
            "Character_lower": interval["lower_inclusive"] if interval else None,
            "Character_upper_exclusive": interval["upper_exclusive"] if interval else None,
            "Character_interval_compatible": interval_ok,
        }
        prediction_rows.append(row)
        by_key[case_key(case)] = {"case": case, "prediction": pred, "raw": pred_raw, "row": row}

    residual_fields = list(prediction_rows[0].keys())
    write_csv(RESIDUAL_PATH, prediction_rows, residual_fields)

    lite_cases = [c for c in cases if c["C_Lite"] is not None]
    short_lite = [c for c in lite_cases if c["bars"] < 21]
    long_lite = [c for c in lite_cases if c["bars"] >= 21]
    short_err = [model_prediction(c, fit) - float(c["C_Lite"]) for c in short_lite]
    long_train = [c for c in train_cases if c["bars"] >= 21]
    long_test = [c for c in long_lite if is_holdout(c)]

    residual_map: dict[str, float] = {}
    transition_rows: list[dict[str, Any]] = []
    sweep = read_json(SWEEP_PATH)["cases"]
    sweep_sorted = sorted(sweep, key=lambda c: c["OHLCV"][-1]["time"])
    for idx, case in enumerate(sweep_sorted):
        measured = by_key[case_key(case)]
        assert measured["case"]["C_Lite"] is not None
        residual_map[case["id"]] = float(measured["prediction"] - float(case["C_Lite"]))
        if idx == 0:
            continue
        previous = sweep_sorted[idx - 1]
        bars = case["OHLCV"]
        entering = bars[-1]
        window_hi = max(float(b["high"]) for b in bars)
        window_lo = min(float(b["low"]) for b in bars)
        window_range = window_hi - window_lo
        volumes = [float(b["volume"]) for b in bars]
        volume_sum = sum(volumes)
        vwap = (
            sum(float(b["close"]) * float(b["volume"]) for b in bars) / volume_sum
            if volume_sum > 0
            else float(bars[0]["close"])
        )
        entry_range = float(entering["high"] - entering["low"])
        body = float(entering["close"] - entering["open"])
        prev_close = float(bars[-2]["close"])
        anchor_close = float(bars[0]["close"])
        previous_bars = previous["OHLCV"]
        prior_high = max(float(b["high"]) for b in previous_bars)
        prior_low = min(float(b["low"]) for b in previous_bars)
        new_global_high = float(entering["high"]) > prior_high
        new_global_low = float(entering["low"]) < prior_low
        confirmed_local_high = (
            float(bars[-2]["high"]) > float(bars[-3]["high"])
            and float(bars[-2]["high"]) >= float(entering["high"])
        )
        confirmed_local_low = (
            float(bars[-2]["low"]) < float(bars[-3]["low"])
            and float(bars[-2]["low"]) <= float(entering["low"])
        )
        prior_c = float(previous["C_Lite"])
        c_now = float(case["C_Lite"])
        entry_vol = float(entering["volume"])
        transition_rows.append(
            {
                "step": idx,
                "END_UTC": case["END"],
                "C_previous": prior_c,
                "C_observed": c_now,
                "delta_C": c_now - prior_c,
                "C_hat": measured["prediction"],
                "residual_hat_minus_C": measured["prediction"] - c_now,
                "entering_time_unix": int(entering["time"]),
                "entry_open": float(entering["open"]),
                "entry_high": float(entering["high"]),
                "entry_low": float(entering["low"]),
                "entry_close": float(entering["close"]),
                "entry_volume": entry_vol,
                "new_global_high": new_global_high,
                "new_global_low": new_global_low,
                "confirmed_local_high_radius1": confirmed_local_high,
                "confirmed_local_low_radius1": confirmed_local_low,
                "any_predeclared_event": bool(new_global_high or new_global_low or confirmed_local_high or confirmed_local_low),
                "entry_range": entry_range,
                "entry_body_signed": body,
                "entry_close_gap_from_prior_close": float(entering["close"] - prev_close),
                "entry_range_over_window_range": entry_range / window_range if window_range else 0.0,
                "entry_close_from_START_close_over_window_range": (float(entering["close"]) - anchor_close) / window_range if window_range else 0.0,
                "entry_close_from_midrange_over_window_range": (float(entering["close"]) - (window_hi + window_lo) / 2.0) / window_range if window_range else 0.0,
                "entry_close_from_VWAP_over_window_range": (float(entering["close"]) - vwap) / window_range if window_range else 0.0,
                "entry_volume_rank_fraction": sum(v <= entry_vol for v in volumes) / len(volumes),
            }
        )
    transition_fields = list(transition_rows[0].keys())
    write_csv(TRANSITION_PATH, transition_rows, transition_fields)

    event_rows = [r for r in transition_rows if r["any_predeclared_event"]]
    changed_rows = [r for r in transition_rows if abs(float(r["delta_C"])) > 1e-8]
    changed_without_event = [r for r in changed_rows if not r["any_predeclared_event"]]
    unchanged_with_event = [r for r in transition_rows if abs(float(r["delta_C"])) <= 1e-8 and r["any_predeclared_event"]]

    correlation_columns = {
        "entry_range": "entry_range",
        "entry_range_over_window_range": "entry_range_over_window_range",
        "entry_body_signed": "entry_body_signed",
        "entry_volume": "entry_volume",
        "entry_volume_rank_fraction": "entry_volume_rank_fraction",
        "entry_close_gap_from_prior_close": "entry_close_gap_from_prior_close",
        "entry_close_from_START_close_over_window_range": "entry_close_from_START_close_over_window_range",
        "entry_close_from_midrange_over_window_range": "entry_close_from_midrange_over_window_range",
        "entry_close_from_VWAP_over_window_range": "entry_close_from_VWAP_over_window_range",
        "C_previous": "C_previous",
    }
    delta_c = [float(row["delta_C"]) for row in transition_rows]
    sweep_correlations = {}
    for name, col in correlation_columns.items():
        values = [float(row[col]) for row in transition_rows]
        sweep_correlations[name] = {"pearson": pearson(values, delta_c), "spearman": spearman(values, delta_c)}

    timeframe_json = read_json(TIMEFRAME_PATH)
    timeframe_results = []
    for case in timeframe_json["cases"]:
        found = by_key[case_key(case)]
        timeframe_results.append(
            {
                "id": case["id"],
                "dt_seconds": case.get("source_seconds", case.get("dt")),
                "n_bars": case["bars"],
                "C_hat": found["prediction"],
                "C_Lite_observed": found["case"]["C_Lite"],
                "residual_hat_minus_Lite": found["row"]["residual_hat_minus_Lite"],
                "Character_interval": found["case"]["C_Character_interval"],
                "partition": found["row"]["partition"],
            }
        )

    # Separate named-control lockbox: no exact control OHLCV input is allowed into
    # this refit. It is stricter by case than the primary temporal split, but related
    # windows may still overlap in time and therefore are not an independent episode.
    control_signatures, control_ids_by_group = control_signature_keys(cases)
    control_train = [
        c
        for c in lite_cases
        if c["bars"] >= 21 and exact_input_signature(c) not in control_signatures
    ]
    assert all(exact_input_signature(c) not in control_signatures for c in control_train)
    assert len(control_train) >= 9, f"Too few cases for named-control fit: {len(control_train)}"
    control_fit = fit_ols(control_train)
    id_to_case = {c["id"]: c for c in cases}
    control_rows: list[dict[str, Any]] = []
    control_group_metrics: dict[str, Any] = {}
    control_union_ids = set()
    for group_name, group_ids in control_ids_by_group.items():
        group_cases = [id_to_case[case_id] for case_id in group_ids]
        control_union_ids.update(group_ids)
        group_lite_long = [c for c in group_cases if c["C_Lite"] is not None and c["bars"] >= 21]
        group_lite_short = [c for c in group_cases if c["C_Lite"] is not None and c["bars"] < 21]
        group_chars = [c for c in group_cases if c["C_Lite"] is None]
        group_pred_long = [model_prediction(c, control_fit) for c in group_lite_long]
        group_pred_short = [model_prediction(c, control_fit) for c in group_lite_short]
        compat = []
        for c in group_cases:
            pred = model_prediction(c, control_fit)
            interval = c["C_Character_interval"]
            ok = bool(interval["lower_inclusive"] <= pred < interval["upper_exclusive"]) if interval else None
            if c["C_Lite"] is None and ok is not None:
                compat.append(ok)
            control_rows.append(
                {
                    "control_group": group_name,
                    "id": c["id"],
                    "partition": "named_control_excluded_from_fit",
                    "dt_seconds": c["source_seconds"],
                    "n_bars": c["bars"],
                    "C_hat_raw": raw_prediction(c, control_fit),
                    "C_hat": pred,
                    "C_Lite": c["C_Lite"],
                    "residual_hat_minus_Lite": pred - float(c["C_Lite"]) if c["C_Lite"] is not None else None,
                    "Character_lower": interval["lower_inclusive"] if interval else None,
                    "Character_upper_exclusive": interval["upper_exclusive"] if interval else None,
                    "Character_interval_compatible": ok,
                }
            )
        control_group_metrics[group_name] = {
            "rows": len(group_cases),
            "distinct_input_signatures": len({exact_input_signature(c) for c in group_cases}),
            "Lite_long": metric_block(group_pred_long, [float(c["C_Lite"]) for c in group_lite_long]),
            "Lite_short": metric_block(group_pred_short, [float(c["C_Lite"]) for c in group_lite_short]),
            "Character_only_cases": len(group_chars),
            "Character_only_compatible": sum(compat),
        }
    assert len(control_rows) == 45
    write_csv(CONTROL_RESIDUAL_PATH, control_rows, list(control_rows[0].keys()))
    control_union_cases = [id_to_case[case_id] for case_id in sorted(control_union_ids)]
    control_union_long = [c for c in control_union_cases if c["C_Lite"] is not None and c["bars"] >= 21]
    control_fit_summary = {
        "rule": "exclude exact OHLCV inputs named by C_cruce_doble.json, the 17-step END sweep, and the 15s/1m/2m timeframe file; fit the same fixed OLS feature model on remaining Lite long cases",
        "training_cases": len(control_train),
        "training_by_delta": {str(delta): sum(int(c["source_seconds"]) == delta for c in control_train) for delta in sorted({int(c["source_seconds"]) for c in control_train})},
        "named_control_rows": {name: len(ids) for name, ids in control_ids_by_group.items()},
        "union_rows": len(control_union_cases),
        "union_distinct_inputs": len({exact_input_signature(c) for c in control_union_cases}),
        "union_Lite_long_metrics": metric_block(
            [model_prediction(c, control_fit) for c in control_union_long],
            [float(c["C_Lite"]) for c in control_union_long],
        ),
        "groups": control_group_metrics,
        "sweep_predictions": [r for r in control_rows if r["control_group"] == "sweep"],
        "timeframe_predictions": [r for r in control_rows if r["control_group"] == "timeframe"],
        "blindness_note": "Exact named control inputs were excluded from fitting. Labels were previously collected and the windows overlap other cases, so this is a label lockbox check, not a human-blind or independent-episode validation.",
        "coefficients": [float(x) for x in control_fit["beta"]],
        "means": [float(x) for x in control_fit["mean"]],
        "scales": [float(x) for x in control_fit["scale"]],
    }

    train_pred = [model_prediction(c, fit) for c in long_train]
    test_pred = [model_prediction(c, fit) for c in long_test]
    heldout_long_by_dt = {}
    for delta in sorted({int(c["source_seconds"]) for c in long_test}):
        subset = [c for c in long_test if int(c["source_seconds"]) == delta]
        heldout_long_by_dt[str(delta)] = metric_block(
            [model_prediction(c, fit) for c in subset], [float(c["C_Lite"]) for c in subset]
        )

    character_cases = [c for c in cases if c["C_Lite"] is None]
    character_compatible = [
        by_key[case_key(c)]["row"]["Character_interval_compatible"] for c in character_cases
    ]
    n21_by_dt: dict[str, dict[str, Any]] = {}
    for delta in sorted({int(c["source_seconds"]) for c in lite_cases if c["bars"] == 21}):
        vals = [float(c["C_Lite"]) for c in lite_cases if c["bars"] == 21 and int(c["source_seconds"]) == delta]
        n21_by_dt[str(delta)] = {"count": len(vals), "min_C": min(vals), "max_C": max(vals), "distinct_C_rounded": len(set(round(v) for v in vals))}
    integer_deviation = [abs(float(c["C_Lite"]) - round(float(c["C_Lite"]))) for c in long_lite]

    sweep_rows_out = []
    for c in sweep_sorted:
        item = by_key[case_key(c)]
        sweep_rows_out.append(
            {
                "END": c["END"],
                "C_observed": float(c["C_Lite"]),
                "C_hat": item["prediction"],
                "residual_hat_minus_C": float(item["prediction"] - float(c["C_Lite"])),
            }
        )

    dev_holdout_count = sum(is_holdout(c) for c in lite_cases)
    results = {
        "status": "candidate_rejected_for_unified_generation",
        "master_sha256": master_hash,
        "input_validation": validation,
        "identical_effective_input_audit": identical_input_audit(cases),
        "context_transition_audit": context_transition_audit(cases),
        "partition": {
            "rule": "hold out the 2026-10-12 UTC episode intersecting 18:54-19:30 and all 2026-10-13 cases; time-only, independent of C and absolute price",
            "Lite_holdout_count": dev_holdout_count,
            "long_Lite_training_count": len(long_train),
            "long_Lite_holdout_count": len(long_test),
            "long_training_timeframes": {str(k): v for k, v in sorted({d: sum(int(c['source_seconds']) == d for c in long_train) for d in {int(c['source_seconds']) for c in long_train}}.items())},
            "long_holdout_timeframes": {str(k): v for k, v in sorted({d: sum(int(c['source_seconds']) == d for c in long_test) for d in {int(c['source_seconds']) for c in long_test}}.items())},
            "blindness_note": "Locked from target labels in the script, but not a genuinely blind study: the sweep labels are stated in the user request and all labels were previously collected in the package.",
        },
        "short_branch": {
            "formula": "C_hat = Delta * max(1, 10*n/183), for n<21",
            "Lite_cases": len(short_lite),
            "max_abs_residual": max(abs(e) for e in short_err),
            "exact_within_1e-8": sum(abs(e) <= 1e-8 for e in short_err),
            "coefficient_status": "10/183 reproduces the observed n=19,20 ratios but has no independent physical derivation; descriptive candidate only",
        },
        "boundary": {
            "long_Lite_cases": len(long_lite),
            "max_distance_to_integer": max(integer_deviation),
            "n21_by_delta": n21_by_dt,
        },
        "long_branch_candidate": {
            "formula": "C_hat = floor(beta0 + sum_j beta_j*(phi_j-mu_j)/scale_j + 0.5), n>=21",
            "features": FEATURE_NAMES,
            "beta": [float(x) for x in fit["beta"]],
            "mean": [float(x) for x in fit["mean"]],
            "scale": [float(x) for x in fit["scale"]],
            "training_rank": fit["rank"],
            "training_singular_values": [float(x) for x in fit["singular_values"]],
            "training_metrics": metric_block(train_pred, [float(c["C_Lite"]) for c in long_train]),
            "holdout_metrics": metric_block(test_pred, [float(c["C_Lite"]) for c in long_test]),
            "holdout_by_delta": heldout_long_by_dt,
            "interpretation": "Dimensionless path/volume regression; fixed predictors, OLS fit, no price-specific rules. It is an intentionally simple candidate and fails holdout; its coefficients are not promoted to a discovered law.",
        },
        "named_control_lockbox": control_fit_summary,
        "Character_only_interval_compatibility": {
            "cases": len(character_cases),
            "compatible": sum(bool(v) for v in character_compatible),
            "incompatible": sum(not bool(v) for v in character_compatible),
            "note": "No numeric Lite residual is assigned to these cases.",
        },
        "sweep": {
            "positions": len(sweep_sorted),
            "transitions": len(transition_rows),
            "MAE": float(np.mean([abs(r["residual_hat_minus_C"]) for r in sweep_rows_out])),
            "sequence_C_observed": [round(float(c["C_Lite"])) for c in sweep_sorted],
            "sequence_C_hat": [float(by_key[case_key(c)]["prediction"]) for c in sweep_sorted],
            "rows": sweep_rows_out,
            "delta_C_correlations": sweep_correlations,
            "predeclared_events": {
                "definition": "strict new global high/low or radius-1 local high/low confirmed by the entering bar",
                "transitions_with_event": len(event_rows),
                "C_changed_without_event": len(changed_without_event),
                "C_unchanged_with_event": len(unchanged_with_event),
                "changed_without_event_ENDs": [r["END_UTC"] for r in changed_without_event],
            },
            "deltas_divisible_by_3": sum(int(round(x)) % 3 == 0 for x in delta_c),
            "deltas_not_divisible_by_3": sum(int(round(x)) % 3 != 0 for x in delta_c),
        },
        "timeframe_controls": timeframe_results,
        "outputs": {
            "residual_csv": str(RESIDUAL_PATH),
            "named_control_residual_csv": str(CONTROL_RESIDUAL_PATH),
            "transition_csv": str(TRANSITION_PATH),
            "result_json": str(RESULT_PATH),
        },
    }
    RESULT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False, allow_nan=False), encoding="utf-8")
    print(json.dumps({
        "status": results["status"],
        "master_sha256": master_hash,
        "input_validation": results["input_validation"],
        "short_branch": results["short_branch"],
        "long_training_metrics": results["long_branch_candidate"]["training_metrics"],
        "long_holdout_metrics": results["long_branch_candidate"]["holdout_metrics"],
        "long_holdout_by_delta": heldout_long_by_dt,
        "named_control_lockbox": {
            "training_cases": control_fit_summary["training_cases"],
            "named_control_rows": control_fit_summary["named_control_rows"],
            "union_rows": control_fit_summary["union_rows"],
            "union_distinct_inputs": control_fit_summary["union_distinct_inputs"],
            "union_Lite_long_metrics": control_fit_summary["union_Lite_long_metrics"],
            "groups": control_group_metrics,
        },
        "character_compatibility": results["Character_only_interval_compatibility"],
        "timeframe_controls": timeframe_results,
        "sweep_MAE": results["sweep"]["MAE"],
        "sweep_delta_C_correlations": sweep_correlations,
        "sweep_predeclared_events": results["sweep"]["predeclared_events"],
        "context_transition_audit": {
            "adjacent_Lite_pairs_with_exact_OHLCV_prefix": results["context_transition_audit"]["adjacent_Lite_pairs_with_exact_OHLCV_prefix"],
            "distinct_entering_candles": results["context_transition_audit"]["distinct_entering_candles"],
            "repeated_entering_candles": results["context_transition_audit"]["repeated_entering_candles"],
            "repeated_candles_with_context_dependent_delta_C": results["context_transition_audit"]["repeated_candles_with_context_dependent_delta_C"],
            "same_C_previous_and_same_entering_candle_with_different_delta": results["context_transition_audit"]["same_C_previous_and_same_entering_candle_with_different_delta"],
            "same_C_previous_same_n_and_same_entering_candle_repeated_keys": results["context_transition_audit"]["same_C_previous_same_n_and_same_entering_candle_repeated_keys"],
            "same_C_previous_same_n_and_same_entering_candle_conflicts": results["context_transition_audit"]["same_C_previous_same_n_and_same_entering_candle_conflicts"],
        },
        "files": results["outputs"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
