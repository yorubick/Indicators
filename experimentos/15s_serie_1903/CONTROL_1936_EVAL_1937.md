# Control oficial: END 19:36, lectura 19:37

**Estado:** realizado en TradingView; `C` no es observable en esta vela porque el indicador aún no proyecta las curvas.

## Configuración y lectura observada

- Símbolo: `NQ1!`; gráfico de 1 minuto; timezone del gráfico: UTC.
- Indicador oficial visible: `PoiSzn EMA Origin Lite v1.3`; fuente configurada: 15 segundos.
- START: `2026-10-12 19:03`; END (incluida la vela): `2026-10-12 19:36`.
- Vela seleccionada: `2026-10-12 19:37 UTC`.
- OHLC en TradingView: O `30,908.00`, H `30,908.25`, L `30,902.25`, C `30,906.25`.
- Las seis salidas Lite en la Ventana de Datos son `∅`. El indicador de laboratorio también no produce líneas visibles en ese punto.
- La vela END tuvo high `30,911.00`; el cierre de 19:37 (`30,906.25`) no rompió ese extremo. La predicción de curvas a 19:37 supone una salida activa y no se puede contrastar aquí.

Captura: [`evidencia/C_Lite_1936_eval_1937.png`](evidencia/C_Lite_1936_eval_1937.png).

## Reproducción de la predicción

Ejecuté `imports/gemini/c_discovery/predict_1936_eval_1937.py` tras inspeccionar su contenido. Reproduce la tabla compartida para `C=87` y `C=123`, con semilla `30,902.25` y cierres de las cuatro subbarras de 19:37 `[30,903.75, 30,903.75, 30,905.25, 30,906.25]`. El script calcula la recurrencia EMA para candidatos de C, pero no comprueba la condición de activación del indicador oficial.

En el CSV fuente `C_barrido_15s_start1902.csv` hay 4,142 barras de 15 s después del END, hasta `2026-10-13 13:55:30 UTC`; ninguna alcanza un high mayor que `30,911`. Por eso este END no ofrece una vela posterior con curvas oficiales visibles dentro del CSV examinado. La predicción aritmética queda **sin medición oficial**, no confirmada ni refutada.

## Revisión de `verify_operator_full_audit.py`

La ejecución produce `E_cand=True` en `19:26`, `19:29`, `19:33` y `19:34`, no solo en `19:29` y `19:34`. Al cruzarlo con `observed_15s` hardcodeado por el propio script:

| END | E del script | C 15 s codificado |
|---|---:|---:|
| 19:26 | 1 | 88 |
| 19:29 | 1 | 123 |
| 19:33 | 1 | 87 |
| 19:34 | 1 | 123 |

Así, `E` no separa exactamente las expansiones de las mesetas en los 13 casos tal como está implementado. Los dos contraejemplos indicados no desaparecen al incluir el high previo de START–19:22:30, que fue `30,870.75`.

La afirmación de que 19:33 “se congela a mitad de minuto” tampoco coincide con las subbarras del CSV: el high de `19:33:45` es `30,886.25` y su cierre `30,885.75`. La secuencia de cierres incluye dos valores `30,881.00` en :15 y :30, pero la subbarra :45 continúa el movimiento.

El script empieza `win_high` en `-1e9` al iniciar el bucle en 19:23, por lo que no incluye por construcción todo el high previo desde START para marcar nuevos máximos. En este caso concreto los máximos de 19:26 y 19:33 sí superan el high previo `30,870.75`, así que los contraejemplos anteriores se mantienen. `np.argmax` también resuelve empates eligiendo la primera subbarra; el protocolo debe fijar si “subbarra máxima :45” significa primer máximo, último máximo o máximo único.

## Corrección aritmética de la fórmula declarada

Con los valores publicados para `N_C` y `Δt`, la ecuación escrita con `round` no da todos los C indicados:

- 1 min: `5 × 22.5 = 112.5`, `6 × 22.5 = 135`.
- 15 s: `12 × 5.625 = 67.5`, `15.5 × 5.625 = 87.1875`, `22 × 5.625 = 123.75`.

El redondeo al entero más cercano da `68`, `87` y `124` para esos tres casos de 15 s (`round` de Python usa empate al par y daría `112` en `112.5`). `floor` da `67`, `87` y `123`, y reproduce los enteros de la tabla. Para los valores informados, la forma aritméticamente compatible es `C=floor(N_C·3·Δt/8)`, salvo que los `N_C` reales antes de redondear sean distintos de los publicados. Esto no determina todavía cómo se selecciona `N_C`.

## Siguiente medición válida

Para comprobar una salida oficial hay que seleccionar una vela posterior a END donde las curvas estén activas. END `19:36` no cruza `30,911` en el CSV disponible. Puede usarse END `19:35` / lectura `19:36` como control de calibración (el cierre de 19:36 supera el high de 19:35), pero ese caso no sería una predicción ciega nueva.
