# Evaluador de reglas de C

`tools/evaluador_C.py` es el criterio único para decidir si una regla de selección de C funciona. Una regla nueva no se considera un avance hasta que mejora a las líneas base en este evaluador **y** acierta controles registrados antes de medirlos.

## Uso

```bash
# Marcador de todas las reglas sobre el maestro y los casos 2 m
python tools/evaluador_C.py evaluar

# Antes de mirar TradingView: registrar la predicción para una ventana nueva
python tools/evaluador_C.py registrar --ohlcv velas.json \
    --start 2026-10-16T14:30:00Z --end 2026-10-16T15:10:00Z --dt 60
git add experimentos/predicciones && git commit -m "Predicción registrada ..."

# Después de leer el C oficial
python tools/evaluador_C.py verificar --archivo experimentos/predicciones/<id>.json --C 87
```

`--ohlcv` acepta la salida del conector de TradingView (`get_ohlcv`, en filas o columnas) o una lista de velas `{time, open, high, low, close, volume}`. Las velas deben estar en la **resolución de la fuente** del indicador y cubrir de START a END sin huecos. Si falta alguna, el registro se rechaza.

## Qué garantiza

1. **Las reglas no ven identificadores, fechas ni horas.** Reciben solo `dt`, `n` (barras inclusivas), `T = END − START` y las velas de la caja, así que no pueden codificar casos a mano como hacía `operador_completo_C.py`.
2. **Validación cruzada por grupo.** Las reglas con parámetros se ajustan dejando fuera cada vez todos los casos con el mismo START y la misma `dt`; esos casos comparten casi todas sus velas.
3. **Comparación con el azar.** La columna `azar` da los aciertos exactos que se obtendrían barajando los C medidos dentro de cada `dt`, y `p` la probabilidad de igualar o superar el resultado así.
4. **Predicciones inmutables.** `registrar` no sobrescribe un archivo existente y guarda el SHA-256 de las velas y el commit base.

## Criterio de acierto

- Régimen corto ($n<21$): $|C_{pred} - C| < 10^{-6}$ s.
- Régimen largo ($n \ge 21$): `round(pred) == C`, porque C es entero.

## Marcador al 16-oct-2026

Régimen largo, aciertos exactos (todas las reglas aciertan el régimen corto, 35/35):

| Regla | Maestro (110) | Azar | p | Mediana del error | 2 m (11) |
|---|---:|---:|---:|---:|---:|
| `base_T_transcurrido`: `round(T/18.3)` | 8 | 3,3 | 0,007 | 9 s | 1 |
| `base_T_inclusivo`: `round(n·dt/18.3)` | 3 | 3,9 | 0,77 | 7 s | 0 |
| `pine_v1_3_auto`: modo Auto del clon | 1 | 1,2 | 0,73 | 13,5 s | 0 |
| `kappa_por_dt`: κ ajustada por dt (validación cruzada) | 2 | 4,0 | 0,93 | 8 s | 0 |
| `mediana_por_n`: mediana de C por (dt, n) (validación cruzada) | 14 | 10,6 | 0,14 | 6,5 s | 2 |

Cómo leerlo:

- **Ninguna regla predice el régimen largo.** La mejor acierta el 13 % de los casos y no se distingue del azar.
- **El modo Auto del clon Pine es la peor regla:** queda por debajo de la línea base trivial. En los 11 casos de 2 m, con los que se ajustó su κ, no acierta ninguno. Salvedad: la regla está traducida a Python a mano desde `pine/PoiSzn_EMA_Origin_Lite_v1_3_OpenSource.pine` y no se ha contrastado ejecutando el Pine.
- `round(T/18.3)` es la única regla por encima del azar ($p<0{,}01$), pero solo con 8/110. C crece con T, pero T no basta para fijarlo.

## Datos

- `maestro`: los 145 casos Lite de `master_all_C_cases.json`.
- `2m`: 11 casos de 2 m leídos en vivo el 14/15-oct (ver `tools/tabla_maestra_12_casos_2m.py`). Son evidencia secundaria: no tienen CSV de curvas en `manual/`.

La pista más clara de estos datos: **C no es monótono al añadir velas**. Con START 14:00 del 14-oct, C vale 191 con END 14:46, 128 con 14:48 y 191 con 14:50. Moviendo START de 14:00 a 14:02 con END 14:50, C cae de 191 a 128. Algo discreto dentro de la caja hace cambiar C en saltos de unos 60 s.

## Añadir una regla

Escribe una función `def mi_regla(caso: Caso) -> float` y regístrala en `REGLAS_FIJAS`. Si tiene parámetros, escribe en cambio `def ajustar(entrenamiento: list[Registro]) -> Regla` y regístrala en `REGLAS_AJUSTABLES`. Añade una línea en `DESCRIPCION`.
