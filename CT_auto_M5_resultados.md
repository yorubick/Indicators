# Prueba Character Tree M5 — Auto Balanced

Fecha probada: 2026-10-12. Gráfico NQ1!, 1m, UTC, ETH; B-ADJ desactivado. Character Tree en Auto Balanced; Setup direction Auto; Capping cloud Middle; Show range y Show extra EMA clouds activados. Lite quedó en Manual 14:00–14:22.

## Rangos Auto observados

| Caso | Mecha (UTC, precio) | Inicio elegido por Auto | Rango hasta END 14:22 | CT en la vela de la mecha | Primer CT no vacío |
|---|---:|---:|---:|---|---|
| CT_auto_1422_w1429H | 14:29, 30906.00 | 14:02 | 20 min | vacío en las 10 columnas CT | 14:45 (Middle=30902.45948832715) |
| CT_auto_1422_w1443H | 14:43, 30911.25 | 13:56 | 26 min | vacío en las 10 columnas CT | 14:59 (Middle=30906.660798022098) |
| CT_auto_1422_w1448H | 14:48, 30921.25 | 13:49 | 33 min | vacío en las 10 columnas CT | 15:04 (Middle=30908.259567679692) |
| CT_auto_1422_w1426L | 14:26, 30859.00 | 14:02 | 20 min | vacío en las 10 columnas CT | 14:42 (Middle=30896.456976280628) |

El inicio de cada rectángulo Auto se obtuvo separando su borde vertical variable del rectángulo fijo Lite 14:00–14:22 y convirtiendo la coordenada horizontal mediante las marcas horarias visibles en la captura. Los inicios son distintos entre mechas; Auto no reutiliza un inicio fijo.

## Lectura de la mecha en CSV

En las cuatro velas Point 2 las diez series CT (Slow/Middle/Fast y Extra 1/2, con boundaries) están vacías. Por eso estos CSV no permiten comprobar numéricamente qué nube tocó la mecha ni identificar con certeza la nube de capping a partir de su valor en esa vela. Las barras OHLC sí confirman que cada fila corresponde al precio/hora solicitados.

## Referencia Lite

Las seis columnas Lane del Lite coinciden entre las cuatro exportaciones en 514 timestamps con datos de Lite; discrepancias: 0.

## Primera comparación Manual disponible

El CSV Manual exportado fue 14:00–14:22. Al inspeccionar las capturas, Auto para el caso w1429H eligió 14:02, así que ese CSV no es el rango manual equivalente y no puede cerrar la predicción (a). Sirve como comparación preliminar: en 495 muestras numéricas comunes por columna posteriores a 14:45, ninguna de las 10 series completas es idéntica. Solo hubo coincidencias aisladas en una muestra de Fast cloud y una de Fast cloud boundary. Los errores medios y máximos están en `CT_auto_M5_manual_1400_comparacion.csv`. Esta diferencia también puede reflejar el inicio 14:00 frente a 14:02 y la distinta activación temporal de las series.

La prueba concluyente de (a) requiere poner Character Tree en Manual con Point 1 = 14:02 y Point 2 = 14:22 para el caso w1429H, exportar de nuevo y comparar. Los PNG con sufijo `_cruceta` son capturas de TradingView anotadas con la cruceta sobre el cierre de la primera vela del rango Auto; las capturas originales quedan preservadas. La automatización del navegador quedó bloqueada al intentar continuar: Work indicó que el uso del navegador local está desactivado en Settings. El último estado confirmado en TradingView fue Manual 14:00–14:22; para continuar hace falta reactivar el acceso al navegador y repetir el cambio/exportación.

## Archivos

- CSV: `CT_auto_1422_w1429H.csv`; captura anotada con cruceta sobre la primera vela Auto: `CT_auto_1422_w1429H_cruceta.png`.
- CSV: `CT_auto_1422_w1443H.csv`; captura anotada con cruceta sobre la primera vela Auto: `CT_auto_1422_w1443H_cruceta.png`.
- CSV: `CT_auto_1422_w1448H.csv`; captura anotada con cruceta sobre la primera vela Auto: `CT_auto_1422_w1448H_cruceta.png`.
- CSV: `CT_auto_1422_w1426L.csv`; captura anotada con cruceta sobre la primera vela Auto: `CT_auto_1422_w1426L_cruceta.png`.
- Resumen por caso: `CT_auto_M5_resumen.csv`.
- CSV Manual preliminar (14:00–14:22): `CT_manual_1400_1422.csv`.
