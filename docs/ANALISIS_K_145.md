# Auditoría de C y k en los 145 casos Lite medidos

> **Nota de revisión (16-oct-2026).** La columna rotulada «Pine v1.3» usa $n = \lfloor T/\Delta t \rfloor$ **sin** el $+1$. El clon `pine/PoiSzn_EMA_Origin_Lite_v1_3_OpenSource.pine` (línea 104) usa `floor(T/dt) + 1`, es decir, la base que aquí se llama «heredada». La lectura compatible con el clon es por tanto la heredada, donde la fórmula corta acierta 35/35. El «14/57» muestra que el conteo no inclusivo es incorrecto, no que la ley corta falle. La conclusión sobre $k$ y la celosía de 9 s se mantiene: 7/110 frente a 12,2 esperados por azar.

Fuente: master_all_C_cases.json, que marca 145 casos Lite_decimal_verified dentro de 179 casos únicos. El propio maestro indica que no hay certificación de holdout ciego/prospectivo.

## Hallazgo de semántica temporal

En los 145 registros, bars es siempre una unidad mayor que (END − START) / source_seconds. Por ello hay dos análisis distintos:

| Base temporal | Régimen corto | Fórmula corta exacta | Régimen largo | C largo entero | dC múltiplo de 9 |
|---|---:|---:|---:|---:|---:|
| Análisis heredado: T = bars × dt, n = bars | 35 | 35/35; error máx. 7.62e−12 s | 110 | 110/110; residual máx. 4.75e−11 s | 7/110 |
| Pine v1.3: T = END − START, n = floor(T/dt) | 57 | 14/57; error máx. 21.426 s | 88 | 88/88; residual máx. 4.75e−11 s | 11/88 |

Para el régimen corto se comparó C contra max(dt, T × 10/183). En el régimen largo se usó base = round_half_up(T/18.3), dC = round(C) − base y k = dC/9.

La afirmación de que el C largo es entero sí se sostiene en ambas bases temporales. La afirmación más fuerte de que k siempre es un entero de una celosía de 9 s no se sostiene: en la lectura alineada con Pine v1.3, 77 de 88 casos largos no tienen dC divisible por 9. En la base heredada, 103 de 110 tampoco. C entero y k entero son propiedades diferentes.

## Desglose de la lectura Pine v1.3

| Fuente dt | Casos | Cortos | Fórmula corta exacta | Largos | C largo entero | dC múltiplo de 9 |
|---:|---:|---:|---:|---:|---:|---:|
| 15 s | 39 | 3 | 0/3 | 36 | 36/36 | 2/36 |
| 60 s | 102 | 50 | 13/50 | 52 | 52/52 | 9/52 |
| 120 s | 4 | 4 | 1/4 | 0 | — | — |

No hay casos Lite de 30 s en este maestro; los casos de esa resolución son Character-only y no se mezclaron con la inversión Lite.

## Lectura

El barrido oficial de data/barrido_start_1933.json también muestra que con START variable y END fijo C cambia por saltos no uniformes. La evidencia actual respalda cuantización entera del C largo, pero no un selector universal limitado a k ∈ {−1,0,+1} ni una ley cerrada determinada solo por duración.

Los resultados se pueden reproducir con tools/audit_k_145_semantics.py. El detalle por caso y por ambas semánticas queda en data/audit_k_145_semantics.json; el análisis heredado está en data/analisis_145_lite_casos.json.