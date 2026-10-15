"""Exporta las colisiones exactas (C previo, vela entrante, Δ) del análisis principal."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MASTER_PATH = ROOT / "master_all_C_cases.json"
ANALYSIS_PATH = ROOT / "resultado_C_modelo_independiente.json"
CSV_PATH = ROOT / "residuos_C_estado_escalar.csv"
JSON_PATH = ROOT / "resultado_C_estado_escalar.json"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    master_hash = sha256(MASTER_PATH)
    analysis = json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))
    if analysis["master_sha256"] != master_hash:
        raise RuntimeError("resultado_C_modelo_independiente.json is stale for this master")
    groups = analysis["context_transition_audit"]["same_scalar_state_conflicts"]
    rows = []
    for group_number, group in enumerate(groups, 1):
        for context in group["contexts"]:
            c_after = float(context["C_after"])
            delta = float(context["delta_C"])
            if abs((c_after - float(group["C_before"])) - delta) > 1e-8:
                raise AssertionError("stored delta_C does not match C_after - C_before")
            rows.append({
                "group": group_number,
                "entry_utc": datetime.fromtimestamp(group["entering_time"], timezone.utc).isoformat(),
                "source_seconds": group["dt_seconds"],
                "open": group["entering_OHLCV"]["open"],
                "high": group["entering_OHLCV"]["high"],
                "low": group["entering_OHLCV"]["low"],
                "close": group["entering_OHLCV"]["close"],
                "volume": group["entering_OHLCV"]["volume"],
                "C_previous": group["C_before"],
                "n_previous": context["n_before"],
                "C_next": c_after,
                "delta_C": delta,
                "START_UTC": context["start"],
            })
    fields = ["group", "entry_utc", "source_seconds", "open", "high", "low", "close", "volume",
              "C_previous", "n_previous", "C_next", "delta_C", "START_UTC"]
    with CSV_PATH.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    output = {
        "status": "reproduced_from_current_master_analysis",
        "master_sha256": master_hash,
        "analysis_sha256": sha256(ANALYSIS_PATH),
        "group_count": len(groups),
        "transition_rows": len(rows),
        "same_scalar_state_conflicts": analysis["context_transition_audit"]["same_C_previous_and_same_entering_candle_with_different_delta"],
        "csv_sha256": sha256(CSV_PATH),
        "csv": str(CSV_PATH),
    }
    JSON_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
