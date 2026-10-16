# Auditoría Seven Cloud — 16-oct-2026

## Objetivo

Comprobar si guardar el código con `lookahead_off` actualizó la instancia de la copia que ya estaba cargada, y medir la copia recién añadida contra el estudio oficial en el mismo gráfico.

## Resultado principal

En `seven_cloud_saved_script_added_2026-10-16_2035UTC.csv`, los tres bloques de 32 curvas están en este orden según el montaje observado en TradingView durante la prueba: **oficial**, **copia recién añadida desde el código guardado** y **copia que ya estaba en el gráfico**. Los nombres de encabezado se repiten en el CSV y por sí solos no codifican esta asignación; conservar este contexto al reutilizar el archivo.

Entre las barras de un minuto con timestamp UTC desde **14:00 hasta 20:31 inclusive**, el bloque oficial y la copia recién añadida son exactamente iguales en las **392 × 32 = 12.544 celdas** comparables. No hay diferencia textual ni numérica en esa ventana. En el mismo intervalo, el bloque de la copia preexistente difiere del oficial en **8.422 de 12.544 celdas**; la diferencia absoluta máxima entre celdas numéricas es **31,214629591846 puntos**.

La lectura **R8 E84** de la copia recién añadida coincide con el oficial en las barras cerradas, incluido el valor de **30.329,730986** a las 19:36 UTC. Esto respalda que la fuente guardada produce paridad histórica para esa ventana cuando se añade como una instancia nueva. El guardado, por sí solo, no actualizó la instancia que ya estaba cargada: su bloque siguió mostrando las discrepancias previas.

La captura también contiene filas del intervalo HTF en formación. A las 20:32 UTC el oficial marcó **30.329,730986** y la copia recién añadida **30.307,684375** (diferencia **−22,046611**); a las 20:33 la diferencia fue **−22,111317**. A las 20:34, los valores fueron **30.307,702022** y **30.307,737316**, respectivamente (diferencia **+0,035294**). Esta variación es una observación intrabar separada: la coincidencia histórica de las 392 barras cerradas no demuestra igualdad en vivo ni permite concluir una regla intrabar estable a partir de una sola captura.

## Protocolo reproducible

Desde la raíz del repositorio:

```powershell
python tools/audit_seven_cloud_exports.py
```

El script comprueba las tres secciones repetidas de 32 columnas, filtra la ventana UTC y compara valores decimales sin redondearlos. Para auditar otra exportación compatible:

```powershell
python tools/audit_seven_cloud_exports.py ruta\al\archivo.csv
```

Las columnas duplicadas no identifican cuál estudio es cuál; la asignación se deriva del orden en que se añadieron los estudios en la prueba del navegador. El resultado histórico queda condicionado a ese montaje y a los datos exportados.

## Evidencia primaria preservada

Se incluyen las exportaciones originales sin renombrar ni transformar:

- `seven_cloud_comparacion_16oct.csv`
- `seven_cloud_pre_recarga_16oct_2006UTC.csv`
- `seven_cloud_post_recarga_16oct_2006UTC.csv`
- `seven_cloud_intrabar_r8_pre_post_16oct_2006UTC.csv`
- `seven_cloud_code_update_pre_recarga_2026-10-16_2026UTC.csv`
- `seven_cloud_code_update_post_recarga_2026-10-16_2027UTC.csv`
- `seven_cloud_post_save_pre_reload_2026-10-16_2032UTC.csv`
- `seven_cloud_post_save_post_reload_2026-10-16_2032UTC.csv`
- `seven_cloud_saved_script_added_2026-10-16_2035UTC.csv`

El código Pine versionado está en [`../PoiSzn_Seven_Cloud_EMA_v1_2_OpenSource.pine`](../pine/PoiSzn_Seven_Cloud_EMA_v1_2_OpenSource.pine). En `calc_ema_pair()` declara `lookahead=barmerge.lookahead_off`.

## Siguiente comprobación

Para aislar el comportamiento intrabar, repetir una exportación mientras el siguiente intervalo HTF de 81 minutos sigue abierto y otra justo después de su cierre, anotando timestamp UTC, símbolo, timeframe, nombres/orden de estudios y si la copia se recompiló o se añadió como instancia nueva. Comparar el mismo R8 E84 en cada minuto y mantener separada esa prueba de la paridad de barras cerradas.
