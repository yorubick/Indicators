"""Audita identidad sintética, escala x2 y retorno para C=50 en 1m.

Lee exportaciones TV locales, descarta la última vela abierta mediante el lector
común y verifica OHLCV, seis canales Lite, C recuperado, visibilidad y recurrencia.
"""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from analizar_C_fuente_vs_grafico import LANES, fit_lite, read

ROOT = Path(__file__).parent
MANUAL = ROOT / "manual"
BASE_FIELDS = ["open", "high", "low", "close", "Volume"]
FIELDS = BASE_FIELDS + LANES
BASE_SECONDS = dict(zip(LANES, [24, 89 / 3, 8, 89 / 9, 72 / 27, 89 / 27]))
FILES = {
    "base_a": "C_escala50_base_a.csv",
    "base_b": "C_escala50_base_b.csv",
    "identity_a": "C_escala50_identidad_alternativa_a.csv",
    "identity_b": "C_escala50_identidad_alternativa_b.csv",
    "double_a": "C_escala50_doble_a.csv",
    "double_b": "C_escala50_doble_b.csv",
    "return": "C_escala50_regreso.csv",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_exact(a, b, fields=FIELDS):
    common = sorted(set(a) & set(b))
    mismatches = []
    visibility_mismatches = 0
    compared_values = 0
    for t in common:
        for key in fields:
            av, bv = a[t][key], b[t][key]
            if bool(av) != bool(bv):
                visibility_mismatches += 1
            if av and bv:
                compared_values += 1
                if float(av) != float(bv):
                    mismatches.append((t, key, av, bv))
            elif av != bv:
                mismatches.append((t, key, av, bv))
    return {
        "common_rows": len(common),
        "left_only_rows": len(set(a) - set(b)),
        "right_only_rows": len(set(b) - set(a)),
        "compared_nonempty_values": compared_values,
        "mismatches": len(mismatches),
        "visibility_mismatches": visibility_mismatches,
        "first_mismatch": mismatches[0] if mismatches else None,
    }


def compare_double(base, doubled):
    common = sorted(set(base) & set(doubled))
    price_mismatches = volume_mismatches = curve_mismatches = 0
    visibility_mismatches = 0
    visible_curve_values = 0
    max_price_error = max_volume_error = max_curve_error = 0.0
    first_mismatch = None
    for t in common:
        for key in ("open", "high", "low", "close"):
            expected = 2 * float(base[t][key])
            actual = float(doubled[t][key])
            error = abs(actual - expected)
            max_price_error = max(max_price_error, error)
            if actual != expected:
                price_mismatches += 1
                first_mismatch = first_mismatch or (t, key, expected, actual)
        vol_base, vol_double = float(base[t]["Volume"]), float(doubled[t]["Volume"])
        error = abs(vol_double - vol_base)
        max_volume_error = max(max_volume_error, error)
        if vol_double != vol_base:
            volume_mismatches += 1
            first_mismatch = first_mismatch or (t, "Volume", vol_base, vol_double)
        for key in LANES:
            bv, dv = base[t][key], doubled[t][key]
            if bool(bv) != bool(dv):
                visibility_mismatches += 1
            if bv and dv:
                visible_curve_values += 1
                expected = 2 * float(bv)
                actual = float(dv)
                error = abs(actual - expected)
                max_curve_error = max(max_curve_error, error)
                if actual != expected:
                    curve_mismatches += 1
                    first_mismatch = first_mismatch or (t, key, expected, actual)
            elif bv != dv:
                curve_mismatches += 1
                first_mismatch = first_mismatch or (t, key, bv, dv)
    return {
        "common_rows": len(common),
        "price_values_compared": 4 * len(common),
        "volume_values_compared": len(common),
        "visible_curve_values_compared": visible_curve_values,
        "price_mismatches": price_mismatches,
        "volume_mismatches": volume_mismatches,
        "curve_mismatches": curve_mismatches,
        "visibility_mismatches": visibility_mismatches,
        "max_abs_error": {
            "OHLC_x2": max_price_error,
            "volume_unchanged": max_volume_error,
            "Lite_curves_x2": max_curve_error,
        },
        "first_mismatch": first_mismatch,
    }


def reconstruct(rows, start, end, step, C, future_bars=540):
    window = [rows[t] for t in range(start, end + 1, step)]
    high = max(float(row["high"]) for row in window)
    low = min(float(row["low"]) for row in window)
    breakout = next(
        t for t in sorted(rows)
        if t > end and (float(rows[t]["close"]) > high or float(rows[t]["close"]) < low)
    )
    upward = float(rows[breakout]["close"]) > high
    seed = float(rows[end]["low" if upward else "high"])
    states = dict.fromkeys(LANES, seed)
    alphas = {key: 2 / (BASE_SECONDS[key] * C / step + 1) for key in LANES}
    errors = []
    visibility_mismatches = 0
    checked = 0
    future_timestamps = [t for t in sorted(rows) if t > end][:future_bars]
    if len(future_timestamps) != future_bars:
        raise AssertionError(f"only {len(future_timestamps)} future native bars; expected {future_bars}")
    for t in future_timestamps:
        checked += 1
        close = float(rows[t]["close"])
        for key in LANES:
            states[key] += alphas[key] * (close - states[key])
            present = bool(rows[t][key])
            visibility_mismatches += present != (t >= breakout)
            if present:
                errors.append(abs(states[key] - float(rows[t][key])))
    return {
        "window_high": high,
        "window_low": low,
        "first_breakout_unix": breakout,
        "first_breakout_utc": datetime.fromtimestamp(breakout, timezone.utc).isoformat(),
        "direction": "up" if upward else "down",
        "seed": seed,
        "future_bars_checked": checked,
        "reconstruction_values": len(errors),
        "max_reconstruction_error": max(errors),
        "visibility_mismatches": visibility_mismatches,
    }


def main():
    prereg_path = ROOT / "C_ESCALA_50_PREREGISTRO.json"
    alternate_path = ROOT / "C_ESCALA_50_IDENTIDAD_ALTERNATIVA.json"
    master_path = ROOT / "master_all_C_cases.json"
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    alternate = json.loads(alternate_path.read_text(encoding="utf-8"))
    master = json.loads(master_path.read_text(encoding="utf-8"))
    start = int(datetime.fromisoformat(prereg["START_UTC"].replace("Z", "+00:00")).timestamp())
    end = int(datetime.fromisoformat(prereg["END_UTC"].replace("Z", "+00:00")).timestamp())
    step = prereg["source_seconds"]
    times = list(range(start, end + 1, step))
    base_symbol = prereg["steps"][0]["symbol"]
    base_case = next(
        case for case in master["cases"]
        if case["symbol"] == base_symbol and case["START_unix"] == start
        and case["END_unix"] == end and case["source_seconds"] == step
    )
    chronology_files = {
        "base_prereg": prereg_path,
        "base_a": MANUAL / FILES["base_a"],
        "base_b": MANUAL / FILES["base_b"],
        "identity_alternative_prereg": alternate_path,
        "identity_a": MANUAL / FILES["identity_a"],
        "identity_b": MANUAL / FILES["identity_b"],
        "double_a": MANUAL / FILES["double_a"],
        "double_b": MANUAL / FILES["double_b"],
        "return": MANUAL / FILES["return"],
    }
    chronology = {
        key: datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
        for key, path in chronology_files.items()
    }
    assert prereg_path.stat().st_mtime < chronology_files["base_a"].stat().st_mtime
    assert alternate_path.stat().st_mtime < chronology_files["identity_a"].stat().st_mtime
    assert chronology_files["identity_b"].stat().st_mtime < chronology_files["double_a"].stat().st_mtime
    assert chronology_files["double_b"].stat().st_mtime < chronology_files["return"].stat().st_mtime
    data = {key: read(MANUAL / filename) for key, filename in FILES.items()}
    target_coverage = {
        key: {"rows_present": sum(t in rows for t in times), "rows_expected": len(times)}
        for key, rows in data.items()
    }
    full_window_exports = ("base_a", "base_b", "identity_b", "double_a", "double_b", "return")
    assert all(target_coverage[key]["rows_present"] == len(times) for key in full_window_exports), target_coverage

    repeats = {
        "base_a_vs_b": compare_exact(data["base_a"], data["base_b"]),
        "identity_a_vs_b": compare_exact(data["identity_a"], data["identity_b"]),
        "double_a_vs_b": compare_exact(data["double_a"], data["double_b"]),
        "base_a_vs_return": compare_exact(data["base_a"], data["return"]),
    }
    full_range_identity = compare_exact(data["base_a"], data["identity_b"])
    double_transform = compare_double(data["base_a"], data["double_a"])
    assert all(v["mismatches"] == 0 and v["visibility_mismatches"] == 0 for v in repeats.values()), repeats
    assert full_range_identity["mismatches"] == 0 and full_range_identity["visibility_mismatches"] == 0
    assert not any(double_transform[k] for k in ["price_mismatches", "volume_mismatches", "curve_mismatches", "visibility_mismatches"]), double_transform

    fits = {}
    for key in ("base_a", "identity_b", "double_a", "return"):
        per_lane = fit_lite(data[key], step, step)
        values = [per_lane[lane]["C"] for lane in LANES]
        fits[key] = {
            "C_mean": sum(values) / len(values),
            "C_by_lane": per_lane,
            "C_spread": max(values) - min(values),
            "max_EMA_RMSE": max(per_lane[lane]["rmse"] for lane in LANES),
        }

    base_prediction = prereg["steps"][0]["prediction_C"]
    identity_prediction = alternate["prediction_C"]
    double_step = next(x for x in prereg["steps"] if x["id"] == "double")
    return_prediction = prereg["steps"][-1]["prediction_C"]
    residuals = [
        {"measurement": "base", "prediction": base_prediction,
         "C_observed": fits["base_a"]["C_mean"],
         "residual_observed_minus_prediction": fits["base_a"]["C_mean"] - base_prediction},
        {"measurement": "identity_average", "prediction": identity_prediction,
         "C_observed": fits["identity_b"]["C_mean"],
         "residual_observed_minus_prediction": fits["identity_b"]["C_mean"] - identity_prediction},
        {"measurement": "double_price_invariance", "prediction": double_step["prediction_invariant_C"],
         "C_observed": fits["double_a"]["C_mean"],
         "residual_observed_minus_prediction": fits["double_a"]["C_mean"] - double_step["prediction_invariant_C"]},
        {"measurement": "double_price_Gemini_v4", "prediction": double_step["prediction_Gemini_v4_C"],
         "C_observed": fits["double_a"]["C_mean"],
         "residual_observed_minus_prediction": fits["double_a"]["C_mean"] - double_step["prediction_Gemini_v4_C"]},
        {"measurement": "return_native", "prediction": return_prediction,
         "C_observed": fits["return"]["C_mean"],
         "residual_observed_minus_prediction": fits["return"]["C_mean"] - return_prediction},
        {"measurement": "double_minus_base", "prediction": 0.0,
         "C_observed": fits["double_a"]["C_mean"] - fits["base_a"]["C_mean"],
         "residual_observed_minus_prediction": fits["double_a"]["C_mean"] - fits["base_a"]["C_mean"]},
    ]

    reconstructions = {
        key: reconstruct(data[key], start, end, step, fits[key]["C_mean"])
        for key in ("base_a", "identity_b", "double_a", "return")
    }
    curves_hidden_in_selection = {
        key: {lane: sum(bool(data[key][t][lane]) for t in times) for lane in LANES}
        for key in ("base_a", "identity_b", "double_a", "return")
    }

    result = {
        "preregistered_window_utc": [prereg["START_UTC"], prereg["END_UTC"]],
        "bars_expected": len(times),
        "target_coverage": target_coverage,
        "symbols": {
            "base": base_symbol,
            "identity_alternative": alternate["alternative_identity"],
            "double": double_step["symbol"],
            "return": prereg["steps"][-1]["symbol"],
        },
        "filesystem_chronology_utc": chronology,
        "baseline_master_case": {
            "id": base_case["id"], "C_Lite": base_case["C_Lite"],
            "residual_C_minus_50": base_case["C_Lite"] - base_prediction,
        },
        "repeat_stability": repeats,
        "base_vs_identity_full_overlap": full_range_identity,
        "double_transform_vs_base": double_transform,
        "C_fits": fits,
        "residuals": residuals,
        "reconstruction": reconstructions,
        "visible_curves_inside_selected_window": curves_hidden_in_selection,
        "scope": "A single preregistered 1m case supports price-scale invariance: OHLC and six Lite curves double, volume and C remain fixed. It does not identify the general f(OHLCV, delta).",
        "sha256": {
            "prereg": sha256(prereg_path),
            "alternate_identity_prereg": sha256(alternate_path),
            "master": sha256(master_path),
            "screenshots": {
                name: sha256(MANUAL / name)
                for name in ["C_escala50_identidad_alternativa.png", "C_escala50_doble.png", "C_escala50_final.png"]
            },
            "exports": {name: sha256(MANUAL / filename) for name, filename in FILES.items()},
        },
    }

    assert fits["base_a"]["C_spread"] < 1e-6
    assert fits["identity_b"]["C_spread"] < 1e-6
    assert fits["double_a"]["C_spread"] < 1e-6
    assert fits["return"]["C_spread"] < 1e-6
    assert all(x["max_reconstruction_error"] < 1e-8 and x["visibility_mismatches"] == 0
               for x in reconstructions.values()), reconstructions

    (ROOT / "resultado_C_escala_50_completa.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (ROOT / "residuos_C_escala_50.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(residuals[0]))
        writer.writeheader()
        writer.writerows(residuals)
    print(json.dumps({
        "target_coverage": target_coverage,
        "double_transform_vs_base": double_transform,
        "C_means": {key: fits[key]["C_mean"] for key in fits},
        "residuals": residuals,
        "reconstruction": {key: {k: v for k, v in value.items() if k in ["first_breakout_utc", "max_reconstruction_error", "visibility_mismatches"]} for key, value in reconstructions.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
