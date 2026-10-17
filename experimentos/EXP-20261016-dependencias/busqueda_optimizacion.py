"""Búsqueda sistemática (17-oct): C = entero que satisface o optimiza un criterio
sobre las velas de la caja, con EMA de las curvas corriendo dentro de la caja.

Solo entrenamiento: maestro + 2 m (casos largos). Los casos `nuevos` quedan
reservados para la prueba ciega de cualquier familia que destaque aquí.
Criterio de éxito fijado antes de ejecutar: >= 50 % de aciertos exactos.
Por azar, la mejor de varios cientos de variantes rondaría el 5-8 %.
"""
import sys, itertools
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from evaluador_C import cargar_maestro, cargar_2m

CS = np.arange(1, 401, dtype=float)                       # C candidatos (s)
B0 = {"1A": 8/3, "1B": 89/27, "2A": 8.0, "2B": 89/9, "3A": 24.0, "3B": 89/3, "X1A": 72.0, "X1B": 89.0}


def ema_tray(closes, seed, b0, dt):
    a = 2.0 / (b0 * CS / dt + 1.0)                          # (C,)
    L = np.full(CS.shape, seed, dtype=float)
    out = np.empty((len(closes), len(CS)))
    for i, x in enumerate(closes):
        L = L + a * (x - L)
        out[i] = L
    return out                                              # (n, C)


def main():
    regs = [r for r in cargar_maestro() + cargar_2m() if r.largo]
    objetivo = np.array([round(r.C) for r in regs])
    resultados = {}
    for k, r in enumerate(regs):
        v = r.caso.velas; dt = r.caso.dt
        o = np.array([x.o for x in v]); h = np.array([x.h for x in v]); l = np.array([x.l for x in v]); c = np.array([x.c for x in v])
        H, L_ = h.max(), l.min(); mid = (H + L_) / 2
        bajista = c[-1] >= mid
        semillas = {"S_close": c[0], "S_open": o[0], "S_ext": h[0] if bajista else l[0], "S_extop": l[0] if bajista else h[0],
                    "box_ext": H if bajista else L_}
        objetivos_end = {"E_close": c[-1], "E_ext": h[-1] if bajista else l[-1], "E_extop": l[-1] if bajista else h[-1], "mid": mid,
                         "E_open": o[-1]}
        for (sn, sv), (bn, b0) in itertools.product(semillas.items(), B0.items()):
            tr = ema_tray(c[1:], sv, b0, dt)                 # desde la segunda vela de la caja
            fin = tr[-1]
            # 1) valor de la línea en END igual a un objetivo: C más cercano al cruce
            for en, ev in objetivos_end.items():
                d = fin - ev
                s = np.sign(d); idx = np.where(s[:-1] * s[1:] <= 0)[0]
                pred = CS[idx[0]] if len(idx) else -1
                resultados.setdefault(("linea_en_END", sn, bn, en), []).append(pred)
            # 2) equilibrio: nº de cierres por encima = por debajo (primer C donde cambia el signo)
            dif = (c[1:, None] > tr).sum(0) - (c[1:, None] < tr).sum(0)
            s = np.sign(dif); idx = np.where(s[:-1] * s[1:] <= 0)[0]
            resultados.setdefault(("equilibrio", sn, bn, "-"), []).append(CS[idx[0]] if len(idx) else -1)
            # 3) menor C sin cierres que atraviesen la línea (techo si bajista, suelo si alcista)
            atraviesa = (c[1:, None] > tr).any(0) if bajista else (c[1:, None] < tr).any(0)
            idx = np.where(~atraviesa)[0]
            resultados.setdefault(("sin_cierres_atraviesan", sn, bn, "-"), []).append(CS[idx[0]] if len(idx) else -1)
            # 4) menor C sin mechas que atraviesen
            atr = (h[1:, None] > tr).any(0) if bajista else (l[1:, None] < tr).any(0)
            idx = np.where(~atr)[0]
            resultados.setdefault(("sin_mechas_atraviesan", sn, bn, "-"), []).append(CS[idx[0]] if len(idx) else -1)
            # 5) mínimo error cuadrático entre línea y cierres (excluyendo C<dt)
            sse = ((c[1:, None] - tr) ** 2).sum(0); sse[CS < dt] = np.inf
            resultados.setdefault(("min_sse", sn, bn, "-"), []).append(CS[int(np.argmin(sse))])
            # 6) máximo nº de toques (vela cuyo rango contiene la línea)
            toques = ((l[1:, None] <= tr) & (h[1:, None] >= tr)).sum(0)
            resultados.setdefault(("max_toques", sn, bn, "-"), []).append(CS[int(np.argmax(toques))])
    filas = []
    for clave, preds in resultados.items():
        p = np.array(preds)
        filas.append(((p == objetivo).sum(), (np.abs(p - objetivo) <= 2).sum(), clave))
    filas.sort(reverse=True)
    print(f"casos de entrenamiento: {len(regs)}; variantes: {len(filas)}")
    for f in filas[:15]:
        print(f"  exactos {f[0]:>3}  ±2 {f[1]:>3}  {f[2]}")


if __name__ == "__main__":
    main()
