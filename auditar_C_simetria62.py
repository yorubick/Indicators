"""Auditor preregistrado de escala, traslación y reflexión para el caso C=62."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from analizar_C_frontera_1s import read
from analizar_C_fuente_vs_grafico import LANES, fit_lite
from auditar_C_escala_50_completa import reconstruct

ROOT = Path(__file__).parent
MANUAL = ROOT / "manual"
SPEC_PATH = ROOT / "C_SIMETRIA_62_PREREGISTRO.json"
AMENDMENT_PATH = ROOT / "C_SIMETRIA_62_ENMIENDA_VALIDACION.json"
EVIDENCE_PATH = ROOT / "C_SIMETRIA_62_ENMIENDA_EVIDENCIA.json"
OUTPUT = ROOT / "resultado_C_simetria62.json"
RESIDUES = ROOT / "residuos_C_simetria62.csv"
OHLC = ("open", "high", "low", "close")
FIELDS = (*OHLC, "Volume", *LANES)
STEP = 60
C_LOCKED = 61.99999999999884
BASE_FILES = {"base_a": "C_simetria62_base_a.csv", "base_b": "C_simetria62_base_b.csv"}
TRANSFORMS = {
    "double": {"a": 2.0, "b": 0.0, "files": ["C_simetria62_doble_a.csv", "C_simetria62_doble_b.csv"]},
    "translation": {"a": 1.0, "b": 10000.0, "files": ["C_simetria62_traslacion_a.csv", "C_simetria62_traslacion_b.csv"]},
    "reflection": {"a": -1.0, "b": 70000.0, "files": ["C_simetria62_reflejo_a.csv", "C_simetria62_reflejo_b.csv"]},
}
RETURN_FILE = "C_simetria62_regreso.csv"
SCREENSHOTS = {
    "base": "C_simetria62_base.png",
    "double": "C_simetria62_doble.png",
    "translation": "C_simetria62_traslacion.png",
    "reflection": "C_simetria62_reflejo.png",
    "return_native": "C_simetria62_regreso.png",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_repeat(left, right):
    common = sorted(set(left) & set(right))
    if not common:
        return {"common_rows": 0, "mismatches": None, "visibility_mismatches": None,
                "max_abs_error": None, "error": "no common timestamps"}
    mismatches, visibility = 0, 0
    max_error = {key: 0.0 for key in FIELDS}
    for t in common:
        for key in FIELDS:
            x, y = left[t][key], right[t][key]
            visibility += bool(x) != bool(y) if key in LANES else 0
            if bool(x) != bool(y):
                mismatches += 1
            elif x and y:
                error = abs(float(x) - float(y))
                max_error[key] = max(max_error[key], error)
                mismatches += error != 0
    return {"common_rows": len(common), "mismatches": int(mismatches),
            "visibility_mismatches": int(visibility), "max_abs_error": max_error}


def affine_check(base, transformed, a, b):
    common = sorted(set(base) & set(transformed))
    errors = {key: 0.0 for key in FIELDS}
    visibility = {key: 0 for key in LANES}
    value_mismatches = {key: 0 for key in FIELDS}
    compared = {key: 0 for key in FIELDS}
    for t in common:
        for key in OHLC:
            base_key = {"high": "low", "low": "high"}.get(key, key) if a < 0 else key
            expected = a * float(base[t][base_key]) + b
            actual = float(transformed[t][key])
            error = abs(actual - expected)
            compared[key] += 1
            errors[key] = max(errors[key], error)
            value_mismatches[key] += actual != expected
        bv, tv = float(base[t]["Volume"]), float(transformed[t]["Volume"])
        compared["Volume"] += 1
        errors["Volume"] = max(errors["Volume"], abs(tv - bv))
        value_mismatches["Volume"] += tv != bv
        for key in LANES:
            x, y = base[t][key], transformed[t][key]
            visibility[key] += bool(x) != bool(y)
            if x and y:
                expected = a * float(x) + b
                error = abs(float(y) - expected)
                errors[key] = max(errors[key], error)
                compared[key] += 1
                value_mismatches[key] += float(y) != expected
    return {"common_rows": len(common), "max_abs_error": errors,
            "exact_value_mismatches": value_mismatches,
            "visibility_mismatches": visibility, "compared_values": compared}


def measurement(rows, start, end):
    times = list(range(start, end + 1, STEP))
    missing = [t for t in times if t not in rows]
    if missing:
        raise ValueError(f"missing range timestamps: {missing[:5]}")
    fits = fit_lite(rows, STEP, STEP)
    cs = [fit["C"] for fit in fits.values()]
    if len(fits) != 6:
        raise ValueError("expected six Lite lane fits")
    return {"C": sum(cs) / len(cs), "residual_vs_locked_C": sum(cs) / len(cs) - C_LOCKED,
            "lane_C_spread": max(cs) - min(cs), "max_lane_RMSE": max(x["rmse"] for x in fits.values()),
            "range_bars": len(times), "six_curve_fits": fits}


def master_range_check(base_rows, master_case):
    expected = {int(row["time"]): row for row in master_case["OHLCV"]}
    fields = {"open": "open", "high": "high", "low": "low", "close": "close", "Volume": "volume"}
    missing = [t for t in expected if t not in base_rows]
    mismatches = []
    for t, source in expected.items():
        if t not in base_rows:
            continue
        for field, source_field in fields.items():
            if float(base_rows[t][field]) != float(source[source_field]):
                mismatches.append((t, field, base_rows[t][field], source[source_field]))
    return {"rows_expected": len(expected), "rows_missing": len(missing),
            "value_mismatches": len(mismatches), "first_mismatch": mismatches[0] if mismatches else None}


def transformed_range_check(base_rows, transformed_rows, a, b, start, end):
    common = [t for t in range(start, end + 1, STEP) if t in base_rows and t in transformed_rows]
    mismatches = []
    for t in common:
        for field in OHLC:
            source_field = {"high": "low", "low": "high"}.get(field, field) if a < 0 else field
            expected = a * float(base_rows[t][source_field]) + b
            if float(transformed_rows[t][field]) != expected:
                mismatches.append((t, field, expected, transformed_rows[t][field]))
        if float(transformed_rows[t]["Volume"]) != float(base_rows[t]["Volume"]):
            mismatches.append((t, "Volume", base_rows[t]["Volume"], transformed_rows[t]["Volume"]))
    return {"rows_compared": len(common), "expected_rows": (end - start) // STEP + 1,
            "exact_OHLCV_mismatches": len(mismatches), "first_mismatch": mismatches[0] if mismatches else None}


def main():
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    amendment = json.loads(AMENDMENT_PATH.read_text(encoding="utf-8"))
    evidence_spec = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    master = json.loads((ROOT / spec["source_master"]).read_text(encoding="utf-8"))
    master_case = next(case for case in master["cases"] if case["id"] == spec["master_case_id"])
    assert float(spec["locked_prediction_all_transforms"]) == C_LOCKED
    assert float(master_case["C_Lite"]) == C_LOCKED
    start = int(datetime.fromisoformat(spec["START_UTC"].replace("Z", "+00:00")).timestamp())
    end = int(datetime.fromisoformat(spec["END_UTC"].replace("Z", "+00:00")).timestamp())
    names = {**BASE_FILES, "return": RETURN_FILE}
    for key, meta in TRANSFORMS.items():
        names[f"{key}_a"], names[f"{key}_b"] = meta["files"]
    paths = {key: MANUAL / name for key, name in names.items()}
    screenshot_paths = {key: MANUAL / name for key, name in SCREENSHOTS.items()}
    missing = [str(p.relative_to(ROOT)) for p in paths.values() if not p.exists()]
    missing_screenshots = [str(p.relative_to(ROOT)) for p in screenshot_paths.values() if not p.exists()]
    result = {"preregistered": SPEC_PATH.name, "validation_amendment": AMENDMENT_PATH.name,
              "evidence_amendment": EVIDENCE_PATH.name,
              "registered_at_UTC": spec["registered_at_UTC"], "validation_amendment_at_UTC": amendment["issued_at_UTC"],
              "evidence_amendment_at_UTC": evidence_spec["issued_at_UTC"],
              "preregistration_sha256": sha256(SPEC_PATH), "amendment_sha256": sha256(AMENDMENT_PATH),
              "evidence_amendment_sha256": sha256(EVIDENCE_PATH),
              "master_sha256": sha256(ROOT / spec["source_master"]),
              "status": "pending_measurements" if missing else "pending_symbol_evidence" if missing_screenshots else "audited",
              "missing_exports": missing, "missing_screenshots": missing_screenshots,
              "locked_prediction_C": C_LOCKED}
    if missing or missing_screenshots:
        OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
        return

    data = {key: read(path) for key, path in paths.items()}
    # Verify time coverage and keep the registered range and 540 future bars explicit.
    expected = list(range(start, end + 1, STEP))
    expected_future = list(range(end + STEP, end + 541 * STEP, STEP))
    coverage = {}
    for key, rows in data.items():
        range_count = sum(t in rows for t in expected)
        missing_future = [t for t in expected_future if t not in rows]
        future_count = len(expected_future) - len(missing_future)
        coverage[key] = {"range_rows": range_count, "expected_range_rows": len(expected),
                         "post_END_rows": future_count, "required_post_END_rows": 540,
                         "missing_post_END_timestamps": len(missing_future),
                         "first_missing_post_END": missing_future[0] if missing_future else None}
        assert range_count == len(expected) and not missing_future, (key, coverage[key])

    measurements = {key: measurement(rows, start, end) for key, rows in data.items()}
    recurrence = {key: reconstruct(rows, start, end, STEP, measurements[key]["C"])
                  for key, rows in data.items()}
    checks = {"base_repeat": exact_repeat(data["base_a"], data["base_b"]),
              "return_to_base": exact_repeat(data["base_b"], data["return"]),
              "base_a_vs_master_OHLCV": master_range_check(data["base_a"], master_case),
              "base_b_vs_master_OHLCV": master_range_check(data["base_b"], master_case)}
    for key, meta in TRANSFORMS.items():
        checks[f"{key}_repeat"] = exact_repeat(data[f"{key}_a"], data[f"{key}_b"])
        checks[f"{key}_affine"] = affine_check(data["base_b"], data[f"{key}_b"], meta["a"], meta["b"])
        checks[f"{key}_range_OHLCV"] = transformed_range_check(
            data["base_b"], data[f"{key}_b"], meta["a"], meta["b"], start, end)

    failures = []
    for key, fit in measurements.items():
        if abs(fit["C"] - C_LOCKED) > 1e-6 or fit["lane_C_spread"] > 1e-6 or fit["max_lane_RMSE"] >= 1e-8:
            failures.append(f"{key}: C-fit acceptance")
        if recurrence[key]["max_reconstruction_error"] >= 1e-8 or recurrence[key]["visibility_mismatches"]:
            failures.append(f"{key}: recurrence acceptance")
    for key, check in checks.items():
        if key in ("base_repeat", "return_to_base") or key.endswith("_repeat"):
            if check["common_rows"] < len(expected) + 540 or check["mismatches"] or check["visibility_mismatches"]:
                failures.append(f"{key}: repeat acceptance")
        elif key.endswith("_affine"):
            if check["common_rows"] < len(expected) + 540 or max(check["max_abs_error"].values()) >= 1e-8 or any(check["visibility_mismatches"].values()):
                failures.append(f"{key}: affine acceptance")
        elif key.endswith("_vs_master_OHLCV"):
            if check["rows_missing"] or check["value_mismatches"]:
                failures.append(f"{key}: master OHLCV acceptance")
        elif key.endswith("_range_OHLCV"):
            if check["exact_OHLCV_mismatches"] or check["rows_compared"] != check["expected_rows"]:
                failures.append(f"{key}: transformed OHLCV acceptance")

    result.update({"status": "failed_acceptance" if failures else "numerical_pass_visual_review_pending",
                   "coverage": coverage, "measurements": measurements, "recurrence_540_post_END": recurrence,
                   "checks": checks, "failures": failures,
                   "sha256": {key: sha256(path) for key, path in paths.items()},
                   "screenshot_sha256": {key: sha256(path) for key, path in screenshot_paths.items()},
                   "capture_mtime_utc": {key: datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()
                                         for key, path in paths.items()},
                   "interpretation": "This is a conditional affine-invariance test for one C=62 window; it does not identify the OHLCV-to-C operator."})
    OUTPUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with RESIDUES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["export", "C_estimated", "residual_vs_locked_C", "lane_C_spread", "max_lane_RMSE", "recurrence_max_error"])
        for key in names:
            fit = measurements[key]
            writer.writerow([key, fit["C"], fit["residual_vs_locked_C"], fit["lane_C_spread"],
                             fit["max_lane_RMSE"], recurrence[key]["max_reconstruction_error"]])
    print(json.dumps({"status": result["status"], "C": {k: v["C"] for k, v in measurements.items()},
                      "failures": failures}, indent=2))


if __name__ == "__main__":
    main()
