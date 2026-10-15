"""Verifica solo la identidad OHLCV del preregistro de escala C=50.

El endpoint OHLCV no devuelve los plots Lite. Por diseño este auditor no puntúa
C para el símbolo sintético y no habilita el paso de escala x2.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(rows, fields):
    return [tuple(row[key] for key in fields) for row in rows]


def main():
    prereg_path = ROOT / "C_ESCALA_50_PREREGISTRO.json"
    master_path = ROOT / "master_all_C_cases.json"
    snapshot_path = ROOT / "C_ESCALA_50_OHLCV_TV_API.json"
    prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
    master = json.loads(master_path.read_text(encoding="utf-8"))
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))

    base_step = next(x for x in prereg["steps"] if x["id"] == "base")
    identity_step = next(x for x in prereg["steps"] if x["id"] == "identity")
    case = next(
        x for x in master["cases"]
        if x["symbol"] == base_step["symbol"]
        and x["START_unix"] == int(__import__("datetime").datetime.fromisoformat(
            prereg["START_UTC"].replace("Z", "+00:00")).timestamp())
        and x["END_unix"] == int(__import__("datetime").datetime.fromisoformat(
            prereg["END_UTC"].replace("Z", "+00:00")).timestamp())
        and x["source_seconds"] == prereg["source_seconds"]
    )

    api_fields = ("t", "o", "h", "l", "c", "v")
    master_fields = ("time", "open", "high", "low", "close", "volume")
    base = normalize(snapshot["baseBars"], api_fields)
    identity = normalize(snapshot["identityBars"], api_fields)
    original = normalize(case["OHLCV"], master_fields)
    same_identity = base == identity
    same_master = base == original
    timestamps = [row[0] for row in base]
    expected_start = case["START_unix"]
    expected_end = case["END_unix"]
    complete = (
        len(base) == case["bars"]
        and timestamps == list(range(expected_start, expected_end + 1, prereg["source_seconds"]))
    )

    result = {
        "prereg_id": "C_ESCALA_50",
        "requested_window_utc": [prereg["START_UTC"], prereg["END_UTC"]],
        "interval_seconds": prereg["source_seconds"],
        "base_symbol": base_step["symbol"],
        "identity_symbol": identity_step["symbol"],
        "bars_base": len(base),
        "bars_identity": len(identity),
        "timestamp_coverage_complete": complete,
        "OHLCV_base_equals_identity": same_identity,
        "OHLCV_base_equals_master_baseline": same_master,
        "baseline_C_observed": case["C_Lite"],
        "baseline_prediction": base_step["prediction_C"],
        "baseline_residual_observed_minus_predicted": case["C_Lite"] - base_step["prediction_C"],
        "identity_C_observed": None,
        "identity_prediction": identity_step["prediction_C"],
        "identity_gate_complete": False,
        "identity_gate_missing": "six Lite curves and C fit for the synthetic identity symbol",
        "scale_x2_evaluated": False,
        "scope": "Auxiliary audit of the original +0 API route only. It does not assess the later (NQ1!+NQ1!)/2 identity capture or the completed x2 test; matching OHLCV alone does not verify C.",
        "complete_scale_audit": "resultado_C_escala_50_completa.json",
        "sha256": {
            "prereg": sha256(prereg_path),
            "master": sha256(master_path),
            "api_snapshot": sha256(snapshot_path),
        },
    }

    assert complete, "API snapshot does not cover the preregistered timestamps"
    assert same_identity, "Base and +0 OHLCV differ"
    assert same_master, "Base endpoint OHLCV differs from the consolidated master"
    out_path = ROOT / "resultado_C_escala_50_ohlcv.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
