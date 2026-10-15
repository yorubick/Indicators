"""Procesa exportaciones CSV oficiales de TradingView para un barrido START/END.

No automatiza ni inspecciona internals del sitio. Cada CSV debe provenir de:
TradingView > Manage layouts > Download chart data. Para la inversión directa,
la resolución del gráfico y la fuente del indicador deben coincidir.

Ejemplos:
  python tools/barrido_start_1933.py --init
  python tools/barrido_start_1933.py --analyze
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "barrido_start_1933.json"
LANE_BASES = {
    "Lane 3 A": 24.0,
    "Lane 3 B": 89.0 / 3.0,
    "Lane 2 A": 8.0,
    "Lane 2 B": 89.0 / 9.0,
    "Lane 1 A": 72.0 / 27.0,
    "Lane 1 B": 89.0 / 27.0,
}


def utc_timestamp(value: str) -> int:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return int(parsed.timestamp())


def make_manifest(date: str, first_start: str, last_start: str,
                  end: str, source_seconds: int, symbol: str) -> dict[str, Any]:
    day = dt.date.fromisoformat(date)
    starts = []
    current = dt.datetime.combine(day, dt.time.fromisoformat(first_start), tzinfo=dt.timezone.utc)
    final = dt.datetime.combine(day, dt.time.fromisoformat(last_start), tzinfo=dt.timezone.utc)
    end_dt = dt.datetime.combine(day, dt.time.fromisoformat(end), tzinfo=dt.timezone.utc)
    while current <= final:
        starts.append(current)
        current += dt.timedelta(minutes=1)
    cases = []
    for start in starts:
        tag = f"{start:%Y%m%d}_start_{start:%H%M%S}_end_{end_dt:%H%M%S}_{source_seconds}s"
        cases.append({
            "case_id": f"start_{start:%H%M}",
            "START": start.isoformat().replace("+00:00", "Z"),
            "END": end_dt.isoformat().replace("+00:00", "Z"),
            "T_seg": int((end_dt - start).total_seconds()),
            "symbol": symbol,
            "chart_interval_seconds": source_seconds,
            "source_interval_seconds": source_seconds,
            "official_csv": f"exports/{tag}.csv",
            "status": "pending",
            "C_resuelto": None,
            "N_3A": None,
            "N_2A": None,
        })
    return {
        "schema_version": 1,
        "title": "Barrido de START con END fijo en 2026-10-12 19:33 UTC",
        "data_origin": "CSV exportado desde la interfaz oficial de TradingView",
        "calculation_scope": "C recuperado de plots visibles; no inferido solo de OHLC",
        "symbol": symbol,
        "date_utc": date,
        "END": end_dt.isoformat().replace("+00:00", "Z"),
        "chart_interval_seconds": source_seconds,
        "source_interval_seconds": source_seconds,
        "same_resolution_required": True,
        "cases": cases,
        "notes": [
            "15 puntos: START 19:00 a 19:14 UTC inclusive; END fijo 19:33 UTC.",
            "T_seg es el tiempo transcurrido END-START; no es conteo inclusivo de barras.",
            "La lectura directa requiere que la resolución exportada coincida con Source data resolution.",
            "Los CSV y los C no medidos permanecen pendientes; no se rellenan con predicciones."
        ],
    }


def parse_time(value: str) -> int:
    text = (value or "").strip()
    if not text:
        raise ValueError("timestamp vacío")
    try:
        number = float(text)
        if not math.isfinite(number):
            raise ValueError("timestamp no finito")
        if abs(number) >= 1e12:
            number /= 1000.0
        return int(number)
    except ValueError:
        pass
    parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return int(parsed.timestamp())


def numeric(value: str | None) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() in {"na", "nan", "none", "null", "∅"}:
        return None
    text = text.replace(",", "")
    try:
        result = float(text)
    except ValueError:
        return None
    return result if math.isfinite(result) else None


def read_export(path: Path) -> tuple[list[dict[str, Any]], int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path.name}: CSV sin encabezados")
        normalized = [str(h).strip() for h in reader.fieldnames]
        counts = Counter(normalized)
        required = ("time", "close", *LANE_BASES)
        ambiguous = [name for name in required if counts[name] > 1]
        if ambiguous:
            raise ValueError(
                f"{path.name}: columnas ambiguas repetidas: {', '.join(ambiguous)}. "
                "No se puede distinguir con seguridad qué estudio las generó; "
                "exporta con una sola copia del indicador que publique esas Lane o "
                "verifica manualmente los encabezados antes de mapearlos."
            )
        headers = {name: raw for name, raw in zip(normalized, reader.fieldnames)}
        missing = [name for name in required if name not in headers]
        if missing:
            raise ValueError(f"{path.name}: faltan columnas requeridas: {', '.join(missing)}")
        rows = []
        for raw in reader:
            if not raw.get(headers["time"]):
                continue
            row: dict[str, Any] = {"time": parse_time(raw[headers["time"]])}
            row["close"] = numeric(raw.get(headers["close"]))
            for lane in LANE_BASES:
                row[lane] = numeric(raw.get(headers[lane]))
            rows.append(row)
    rows.sort(key=lambda row: row["time"])
    times = [row["time"] for row in rows]
    diffs = [b - a for a, b in zip(times, times[1:]) if b > a]
    if not diffs:
        raise ValueError(f"{path.name}: faltan timestamps distintos")
    counts: dict[int, int] = {}
    for delta in diffs:
        counts[delta] = counts.get(delta, 0) + 1
    inferred = max(counts, key=counts.get)
    return rows, inferred


def closed_form_c(rows: list[dict[str, Any]], step: int) -> dict[str, Any]:
    by_time = {row["time"]: row for row in rows}
    estimates: list[float] = []
    for t, current in by_time.items():
        previous = by_time.get(t - step)
        if previous is None:
            continue
        s3p, s3c = previous["Lane 3 A"], current["Lane 3 A"]
        s2p, s2c = previous["Lane 2 A"], current["Lane 2 A"]
        if None in (s3p, s3c, s2p, s2c):
            continue
        d3, d2 = s3c - s3p, s2c - s2p
        denominator = 24.0 * d3 - 8.0 * d2
        numerator = (s2p + s2c) - (s3p + s3c)
        scale = max(1.0, abs(24.0 * d3), abs(8.0 * d2))
        if abs(denominator) <= 1e-12 * scale:
            continue
        value = (numerator / denominator) * step
        if math.isfinite(value) and value > 0:
            estimates.append(value)
    if not estimates:
        raise ValueError("no hay pares Lane 3 A/Lane 2 A contiguos y estables para invertir C")
    return {
        "median_seconds": statistics.median(estimates),
        "mean_seconds": statistics.fmean(estimates),
        "min_seconds": min(estimates),
        "max_seconds": max(estimates),
        "pair_count": len(estimates),
        "estimates": estimates,
    }


def lane_fit(rows: list[dict[str, Any]], step: int) -> dict[str, Any]:
    by_time = {row["time"]: row for row in rows}
    result = {}
    for lane, base in LANE_BASES.items():
        pairs = []
        for t, current in by_time.items():
            previous = by_time.get(t - step)
            if previous is None or current[lane] is None or previous[lane] is None or current["close"] is None:
                continue
            dx = current["close"] - previous[lane]
            dy = current[lane] - previous[lane]
            pairs.append((dx, dy))
        denom = sum(x * x for x, _ in pairs)
        if len(pairs) < 3 or denom <= 1e-18:
            result[lane] = {"status": "insufficient_data", "pairs": len(pairs)}
            continue
        alpha = sum(x * y for x, y in pairs) / denom
        if not 0 < alpha <= 1:
            result[lane] = {"status": "not_ema_like", "alpha": alpha, "pairs": len(pairs)}
            continue
        period = 2.0 / alpha - 1.0
        c = period * step / base
        rmse = math.sqrt(sum((y - alpha * x) ** 2 for x, y in pairs) / len(pairs))
        result[lane] = {
            "status": "fit",
            "alpha": alpha,
            "period": period,
            "C_seconds": c,
            "pairs": len(pairs),
            "step_rmse": rmse,
        }
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def analyze_case(case: dict[str, Any], manifest_dir: Path) -> dict[str, Any]:
    csv_value = case.get("official_csv")
    if not csv_value:
        return {**case, "status": "pending", "reason": "official_csv no asignado"}
    path = Path(csv_value)
    if not path.is_absolute():
        path = (manifest_dir / path).resolve()
    if not path.exists():
        return {**case, "status": "pending", "reason": f"falta CSV: {path}"}
    rows, inferred_step = read_export(path)
    chart_step = int(case.get("chart_interval_seconds") or inferred_step)
    source_step = int(case.get("source_interval_seconds") or chart_step)
    if inferred_step != chart_step:
        raise ValueError(f"{case['case_id']}: CSV indica paso {inferred_step}s, pero el manifiesto dice {chart_step}s")
    if chart_step != source_step:
        raise ValueError(
            f"{case['case_id']}: gráfico {chart_step}s y fuente {source_step}s no coinciden; "
            "exporta en la misma resolución o usa el ajuste multipaso con CSV nativo"
        )
    inversion = closed_form_c(rows, chart_step)
    fits = lane_fit(rows, chart_step)
    usable_lane_c = [v["C_seconds"] for v in fits.values() if v.get("status") == "fit"]
    resolved = inversion["median_seconds"]
    start_ts, end_ts = utc_timestamp(case["START"]), utc_timestamp(case["END"])
    output = {
        **case,
        "T_seg": end_ts - start_ts,
        "C_resuelto": resolved,
        "N_3A": 24.0 * resolved / source_step,
        "N_2A": 8.0 * resolved / source_step,
        "status": "measured",
        "measurement": {
            "csv_path": str(path),
            "csv_sha256": sha256(path),
            "rows": len(rows),
            "inferred_interval_seconds": inferred_step,
            "closed_form_pair_estimates": {
                key: value for key, value in inversion.items() if key != "estimates"
            },
            "lane_fits": fits,
            "lane_fit_C_median_seconds": statistics.median(usable_lane_c) if usable_lane_c else None,
            "delta_closed_form_vs_lane_fit_seconds": (
                resolved - statistics.median(usable_lane_c) if usable_lane_c else None
            ),
            "method": "O(1) inversion on consecutive visible Lane 3 A / Lane 2 A plots",
        },
    }
    return output


def write_json(path: Path, content: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera y procesa la matriz de CSV visible de TradingView.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--init", action="store_true", help="crea el barrido START 19:00–19:14, END 19:33")
    parser.add_argument("--analyze", action="store_true", help="procesa los CSV asignados en el manifiesto")
    parser.add_argument("--date", default="2026-10-12")
    parser.add_argument("--first-start", default="19:00:00")
    parser.add_argument("--last-start", default="19:14:00")
    parser.add_argument("--end", default="19:33:00")
    parser.add_argument("--interval", type=int, default=15, help="resolución de gráfico y fuente, segundos")
    parser.add_argument("--symbol", default="CME_MINI:NQ1!")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.init:
        manifest = make_manifest(args.date, args.first_start, args.last_start, args.end, args.interval, args.symbol)
        write_json(output, manifest)
        print(f"Manifiesto creado: {output} ({len(manifest['cases'])} casos pendientes)")
        return
    if args.analyze:
        manifest = json.loads(output.read_text(encoding="utf-8"))
        manifest["cases"] = [analyze_case(c, output.parent) for c in manifest.get("cases", [])]
        manifest["status"] = (
            "complete" if manifest["cases"] and all(c.get("status") == "measured" for c in manifest["cases"])
            else "partial"
        )
        write_json(output, manifest)
        done = sum(c.get("status") == "measured" for c in manifest["cases"])
        print(f"Matriz actualizada: {output} — {done}/{len(manifest['cases'])} mediciones válidas")
        for case in manifest["cases"]:
            if case.get("status") == "measured":
                print(f"{case['START']}  C={case['C_resuelto']:.9f}s  N3A={case['N_3A']:.9f}  N2A={case['N_2A']:.9f}")
            else:
                print(f"{case['START']}  {case.get('status')}: {case.get('reason', '')}")
        return
    parser.error("elige --init o --analyze")


if __name__ == "__main__":
    main()
