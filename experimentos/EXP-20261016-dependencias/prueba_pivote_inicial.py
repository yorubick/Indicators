"""H_pivote (17-oct), definida antes de ejecutar, a partir del barrido M7:
C depende solo de las velas desde el primer pivote confirmado de la ventana
(fuerza k a ambos lados, dentro de la ventana) hasta END.

Prueba de colisión sin ajuste: casos con el mismo END, la misma fuente y el mismo
primer pivote deben tener el mismo C. Se cuentan grupos coherentes e incoherentes
para varias definiciones de pivote, y se compara con agrupar por START (control
trivial: cada grupo tiene un solo caso).
"""
import sys, collections, json, datetime as dt
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "tools"))
from evaluador_C import cargar_maestro, cargar_nuevos, Caso, Vela, Registro

M7 = {30: 108, 31: 108, 32: 108, 33: 108, 34: 108, 35: 88, 36: 93, 37: 82, 38: 88, 39: 88, 40: 88}


def casos_m7():
    b = json.loads((RAIZ / "experimentos/EXP-20261016-dependencias/NQ1_1m_2026-10-15_16.json").read_text())["bars"]
    fin = int(dt.datetime(2026, 10, 16, 17, 0, tzinfo=dt.timezone.utc).timestamp())
    out = []
    for m, C in M7.items():
        ini = int(dt.datetime(2026, 10, 16, 16, m, tzinfo=dt.timezone.utc).timestamp())
        v = tuple(Vela(o, h, l, c, x) for t, o, h, l, c, x in zip(b["t"], b["o"], b["h"], b["l"], b["c"], b["v"]) if ini <= t <= fin)
        out.append(Registro(Caso(60, len(v), fin - ini, v), float(C), f"M7_16{m}", f"{fin}|60"))
    return out


def primer_pivote(v, k, tipo):
    for i in range(k, len(v) - k):
        if tipo in ("alto", "cualquiera") and all(v[i].h > v[j].h for j in range(i - k, i + k + 1) if j != i):
            return i
        if tipo in ("bajo", "cualquiera") and all(v[i].l < v[j].l for j in range(i - k, i + k + 1) if j != i):
            return i
    return None


def main():
    # END e identidad del tramo final: se identifica por las velas desde el pivote (tuplas OHLC)
    regs = [r for r in cargar_maestro() + cargar_nuevos() + casos_m7() if r.largo]
    for k in (1, 2, 3):
        for tipo in ("cualquiera", "alto", "bajo"):
            grupos = collections.defaultdict(list)
            for r in regs:
                v = r.caso.velas
                p = primer_pivote(v, k, tipo)
                if p is None:
                    continue
                clave = (r.caso.dt, tuple((x.o, x.h, x.l, x.c) for x in v[p:]))
                grupos[clave].append(round(r.C))
            multi = [g for g in grupos.values() if len(g) > 1]
            ok = sum(1 for g in multi if len(set(g)) == 1)
            print(f"k={k} pivote {tipo:<10}: grupos con >1 caso: {len(multi):>2}; coherentes {ok}; incoherentes {len(multi) - ok}  {[g for g in multi if len(set(g)) > 1][:4]}")


if __name__ == "__main__":
    main()
