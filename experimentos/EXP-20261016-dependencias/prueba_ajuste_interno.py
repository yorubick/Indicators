"""Hipótesis H_interno (16-oct), definida antes de ejecutar:

En Manual y régimen largo, el Character del rango es el C con el que la nube
(semilla en el extremo de la vela START: máximo si bajista, mínimo si alcista;
dirección según la ayuda: cierre de END en la mitad superior de la caja = bajista)
toca la mecha de END (máximo si bajista, mínimo si alcista) en la vela END.
Variantes: nube media o lenta; línea rápida, centro o lenta; C continuo
redondeado al entero más cercano, hacia abajo o hacia arriba.
"""
import json, math, sys, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from evaluador_C import cargar_maestro, cargar_2m, Caso, Vela

NUBES = {"media": (8.0, 89 / 9), "lenta": (24.0, 89 / 3)}


def linea(caso, seed, C, bs, var):
    a = [2 / (b * C / caso.dt + 1) for b in bs]
    l1 = l2 = seed
    for v in caso.velas[1:]:
        l1 += a[0] * (v.c - l1)
        l2 += a[1] * (v.c - l2)
    return {"rapida": l1, "centro": (l1 + l2) / 2, "lenta": l2}[var]


def ajuste(caso, bs, var):
    hi = max(v.h for v in caso.velas); lo = min(v.l for v in caso.velas)
    fin = caso.velas[-1]
    bajista = fin.c >= (hi + lo) / 2
    seed = caso.velas[0].h if bajista else caso.velas[0].l
    objetivo = fin.h if bajista else fin.l
    f = lambda C: linea(caso, seed, C, bs, var) - objetivo
    a, b = 0.5, 5000.0
    if f(a) * f(b) > 0:
        return None
    for _ in range(80):
        m = (a + b) / 2
        if f(m) * f(a) > 0: a = m
        else: b = m
    return (a + b) / 2


def nuevos():
    base = Path(__file__).parent
    out = []
    for f, s, e, C in [("NQ1_1m_2026-10-15_16.json", "2026-10-16T16:40", "2026-10-16T17:00", 88),
                       ("NQ1_1m_2026-10-12_13.json", "2026-10-12T13:31", "2026-10-12T13:53", 89)]:
        b = json.loads((base / f).read_text())["bars"]
        ts = int(dt.datetime.fromisoformat(s + ":00+00:00").timestamp()); te = int(dt.datetime.fromisoformat(e + ":00+00:00").timestamp())
        v = tuple(Vela(b["o"][i], b["h"][i], b["l"][i], b["c"][i], b["v"][i]) for i, t in enumerate(b["t"]) if ts <= t <= te)
        out.append((Caso(60, len(v), te - ts, v), C))
    return out


def main():
    casos = [(r.caso, r.C) for r in cargar_maestro() + cargar_2m() if r.largo] + nuevos()
    print("casos largos:", len(casos))
    for nube, bs in NUBES.items():
        for var in ("rapida", "centro", "lenta"):
            fits = [(ajuste(c, bs, var), C) for c, C in casos]
            for nombre, q in (("round", round), ("floor", math.floor), ("ceil", math.ceil)):
                ok = sum(1 for x, C in fits if x is not None and q(x) == round(C))
                near = sum(1 for x, C in fits if x is not None and abs(x - C) <= 2)
                print(f"  nube {nube:<5} línea {var:<6} {nombre:<5}: exactos {ok}/{len(casos)}   a ±2 s: {near}")


if __name__ == "__main__":
    main()
