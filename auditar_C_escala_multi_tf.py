"""Auditor prospectivo de invariancia de C bajo duplicación de precio por TF."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from analizar_C_fuente_vs_grafico import LANES, fit_lite, read
from auditar_C_escala_50_completa import compare_double, compare_exact, reconstruct

ROOT = Path(__file__).parent
MANUAL = ROOT / "manual"
FIELDS = ["open", "high", "low", "close", "Volume"] + LANES


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit_summary(rows, step):
    fits = fit_lite(rows, step, step)
    values = [fits[key]["C"] for key in LANES]
    return {
        "C_mean": sum(values) / len(values),
        "C_by_lane": fits,
        "C_spread": max(values) - min(values),
        "max_EMA_RMSE": max(fits[key]["rmse"] for key in LANES),
    }


def main():
    prereg_path = ROOT / "C_ESCALA_TF_REPLICACION_PREREGISTRO.json"
    master_path = ROOT / "master_all_C_cases.json"
    ref_path = ROOT / "C_test_timeframes_1900_1920.json"
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    master = json.loads(master_path.read_text(encoding="utf-8"))
    reference = json.loads(ref_path.read_text(encoding="utf-8"))
    cases_by_id = {x["id"]: x for x in master["cases"]}
    ref_by_id = {x["id"]: x for x in reference["cases"]}
    results = []
    residual_rows = []

    for spec in prereg["cases"]:
        start = int(datetime.fromisoformat(spec["START_UTC"].replace("Z", "+00:00")).timestamp())
        end = int(datetime.fromisoformat(spec["END_UTC"].replace("Z", "+00:00")).timestamp())
        step = spec["source_seconds"]
        expected_times = list(range(start, end + 1, step))
        assert len(expected_times) == spec["bars_inclusive"]

        master_case = cases_by_id[spec["master_case_id"]]
        ref_case = ref_by_id["C_pack_tf" + str(step)]
        assert master_case["bars"] == spec["bars_inclusive"]
        assert abs(master_case["C_Lite"] - spec["C_base_locked"]) < 1e-6
        assert abs(ref_case["C_Lite"] - spec["C_base_locked"]) < 1e-6

        base_names = spec["base_exports"]
        base_a, base_b = [read(name) for name in base_names]
        base_repeat = compare_exact(base_a, base_b)
        assert base_repeat["common_rows"] > 0 and base_repeat["mismatches"] == 0
        assert base_repeat["visibility_mismatches"] == 0
        base_coverage = sum(t in base_a for t in expected_times)
        assert base_coverage == len(expected_times)
        master_ohlcv = {r["time"]: r for r in master_case["OHLCV"]}
        baseline_data_mismatches = []
        for t in expected_times:
            if t not in master_ohlcv:
                baseline_data_mismatches.append((t, "missing_master"))
                continue
            csv_row, master_row = base_a[t], master_ohlcv[t]
            for key, master_key in [("open", "open"), ("high", "high"), ("low", "low"), ("close", "close"), ("Volume", "volume")]:
                if float(csv_row[key]) != float(master_row[master_key]):
                    baseline_data_mismatches.append((t, key, csv_row[key], master_row[master_key]))
        assert not baseline_data_mismatches, baseline_data_mismatches[:3]

        base_fit = fit_summary(base_a, step)
        assert base_fit["C_spread"] < 1e-6 and base_fit["max_EMA_RMSE"] < 1e-8
        base_reconstruction = reconstruct(base_a, start, end, step, base_fit["C_mean"])
        double_names = spec["double_exports"]
        double_paths = [MANUAL / name for name in double_names]
        present = [path.is_file() for path in double_paths]
        double_result = {"status": "pending_missing_double_exports", "exports_present": present}
        screenshot_path = MANUAL / spec["double_screenshot"]
        if all(present):
            double_a, double_b = [read(name) for name in double_names]
            double_repeat = compare_exact(double_a, double_b)
            double_coverage = sum(t in double_a for t in expected_times)
            transform = compare_double(base_a, double_a)
            double_fit = fit_summary(double_a, step)
            data_compatible = (
                double_coverage == len(expected_times)
                and double_repeat["mismatches"] == 0
                and double_repeat["visibility_mismatches"] == 0
                and transform["price_mismatches"] == 0
                and transform["volume_mismatches"] == 0
                and transform["curve_mismatches"] == 0
                and transform["visibility_mismatches"] == 0
                and double_fit["C_spread"] < 1e-6
                and double_fit["max_EMA_RMSE"] < 1e-8
            )
            double_reconstruction = reconstruct(double_a, start, end, step, double_fit["C_mean"])
            recurrence_ok = (
                double_reconstruction["max_reconstruction_error"] < 1e-8
                and double_reconstruction["visibility_mismatches"] == 0
            )
            double_result = {
                "status": "measured_compatible" if data_compatible and recurrence_ok else "measured_incompatible_or_failed",
                "exports_present": present,
                "target_rows_present": double_coverage,
                "repeat_stability": double_repeat,
                "transformation": transform,
                "C_fit": double_fit,
                "residual_C_minus_locked_prediction": double_fit["C_mean"] - spec["C_double_prediction"],
                "delta_C_double_minus_base": double_fit["C_mean"] - base_fit["C_mean"],
                "reconstruction": double_reconstruction,
                "data_compatible": data_compatible,
                "recurrence_ok": recurrence_ok,
                "screenshot_exists_for_manual_symbol_review": screenshot_path.is_file(),
            }

        baseline_row = {
            "case": spec["id"], "measurement": "base", "prediction": spec["C_base_locked"],
            "C_observed": base_fit["C_mean"],
            "residual_observed_minus_prediction": base_fit["C_mean"] - spec["C_base_locked"],
        }
        residual_rows.append(baseline_row)
        double_row = {
            "case": spec["id"], "measurement": "double_price", "prediction": spec["C_double_prediction"],
            "C_observed": double_result.get("C_fit", {}).get("C_mean"),
            "residual_observed_minus_prediction": double_result.get("residual_C_minus_locked_prediction"),
        }
        residual_rows.append(double_row)

        results.append({
            "case": spec["id"],
            "master_case_id": master_case["id"],
            "START_UTC": spec["START_UTC"], "END_UTC": spec["END_UTC"],
            "source_seconds": step, "bars": len(expected_times), "regime": spec["regime"],
            "base_exports": base_names,
            "base_repeat_stability": base_repeat,
            "base_master_OHLCV_mismatches": len(baseline_data_mismatches),
            "base_target_rows_present": base_coverage,
            "base_C_fit": base_fit,
            "base_reconstruction": base_reconstruction,
            "double_exports": double_names,
            "double_screenshot": str(screenshot_path),
            "double": double_result,
            "sha256": {
                "base_exports": {name: sha256(MANUAL / name) for name in base_names},
                "double_exports": {name: sha256(path) for name, path in zip(double_names, double_paths) if path.is_file()},
            },
        })

    result = {
        "preregistration": prereg,
        "cases": results,
        "status": "pending_double_measurements" if any(c["double"]["status"].startswith("pending") for c in results) else "all_double_measurements_present",
        "sha256": {
            "prereg": sha256(prereg_path),
            "master": sha256(master_path),
            "reference": sha256(ref_path),
        },
    }
    (ROOT / "resultado_C_escala_multi_tf.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (ROOT / "residuos_C_escala_multi_tf.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(residual_rows[0]))
        writer.writeheader()
        writer.writerows(residual_rows)
    print(json.dumps({
        "status": result["status"],
        "cases": [{"case": x["case"], "C_base": x["base_C_fit"]["C_mean"], "base_rmse": x["base_C_fit"]["max_EMA_RMSE"], "double_status": x["double"]["status"]} for x in results],
    }, indent=2))


if __name__ == "__main__":
    main()
