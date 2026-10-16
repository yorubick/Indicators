"""Predicciones para Auto Balanced de Character Tree (M5b), registradas antes de medir.

Hipótesis (de los textos de ayuda del autor): las nubes arrancan en END con semilla
en el extremo de la vela END (máximo si bajista, mínimo si alcista; confirmado en M5).
El Character (C) se ajusta para que la nube que hace de tope (media por defecto)
toque la mecha de retroceso (Point 2) sin que ningún cierre de 1 m entre END y la
mecha la atraviese. Se calculan tres variantes de «tocar»: la línea rápida de la
nube (EMA 72·C/9), la lenta (EMA 89·C/9) y el centro.

Uso: python experimentos/EXP-20261016-dependencias/predecir_auto_balanced.py
"""
import json
import datetime as dt
from pathlib import Path

DATOS = Path(__file__).with_name("NQ1_1m_2026-10-15_16.json")
B_MIDDLE = (8.0, 89 / 9)   # b0 de la nube media: EMA 72 y 89 en temporalidad C/9
DT = 60


def lineas(closes, seed, C):
    a = [2 / (b * C / DT + 1) for b in B_MIDDLE]
    l1 = l2 = seed
    out = []
    for x in closes:
        l1 += a[0] * (x - l1)
        l2 += a[1] * (x - l2)
        out.append((l1, l2))
    return out


def ajustar(closes, seed, objetivo, variante, bajista):
    """C continuo para que la línea elegida valga `objetivo` en la última vela."""
    def valor(C):
        l1, l2 = lineas(closes, seed, C)[-1]
        return {"rapida": l1, "lenta": l2, "centro": (l1 + l2) / 2}[variante]
    lo, hi = 0.5, 5000.0
    f_lo, f_hi = valor(lo) - objetivo, valor(hi) - objetivo
    if f_lo * f_hi > 0:
        return None
    for _ in range(100):
        mid = (lo + hi) / 2
        f = valor(mid) - objetivo
        if f * f_lo > 0:
            lo, f_lo = mid, f
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    b = json.loads(DATOS.read_text())["bars"]
    t, o, h, l, c = b["t"], b["o"], b["h"], b["l"], b["c"]
    U = lambda i: dt.datetime.fromtimestamp(t[i], dt.timezone.utc).strftime("%m-%d %H:%M")
    n = len(t)
    piv_h = lambda i, k=3: all(h[i] >= h[j] for j in range(i - k, i + k + 1) if 0 <= j < n)
    piv_l = lambda i, k=3: all(l[i] <= l[j] for j in range(i - k, i + k + 1) if 0 <= j < n)
    casos = []
    for e in range(3, n - 20):
        if t[e] < 1792157400:          # solo 16-oct desde la apertura RTH
            continue
        for bajista in (True, False):
            if not (piv_h(e) if bajista else piv_l(e)):
                continue
            seed = h[e] if bajista else l[e]
            for w in range(e + 6, min(e + 45, n - 17)):
                if any(t[k + 1] - t[k] != 60 for k in range(e, w)):
                    break
                if bajista:
                    if not (piv_h(w) and h[w] < h[e] and min(l[e + 1:w]) < h[w] - 10):
                        continue
                else:
                    if not (piv_l(w) and l[w] > h[e] and max(h[e + 1:w]) > l[w] + 10):
                        continue
                objetivo = h[w] if bajista else l[w]
                res = {}
                for var in ("rapida", "centro", "lenta"):
                    C = ajustar(c[e + 1:w + 1], seed, objetivo, var, bajista)
                    if C is None:
                        continue
                    ls = lineas(c[e + 1:w + 1], seed, C)
                    # ningún cierre entre END y la mecha atraviesa la nube (ni su borde lejano)
                    malo = any((x > max(p) if bajista else x < min(p)) for x, p in zip(c[e + 1:w], ls[:-1]))
                    if not malo:
                        res[var] = round(C, 2)
                if len(res) == 3:
                    casos.append((U(e), "bajista" if bajista else "alcista", U(w), objetivo, w - e, res))
                    break   # primera mecha válida por END
    for caso in casos:
        print(caso)


if __name__ == "__main__":
    main()
