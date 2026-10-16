# C: END15:51 fijo y controles de la vela15:52

13 octubre2026. Seis selecciones nuevas, dos anteriores reutilizadas y repetición independiente del pico93. NQ1!,12oct, ETH, UTC, BADJ apagado, Replay apagado. Lite v1.2 fuente1m, Character Tree v6.5.36 perfilB Manual fuenteChart, gráfico1m.

## END fijo

| START UTC | END UTC | Velas inclusivas | C |
|---|---|---:|---:|
|15:26|15:51|26|82|
|15:27|15:51|25|93|
|15:28|15:51|24|75|
|15:29,control anterior|15:51|23|75|
|15:30,control anterior|15:51|22|68|
|15:31|15:51|21|68|

Todos conservan high30965.50 ylow30877.75. La hipótesis predeclarada de que el prefijo anterior a15:29 fuera irrelevante predijo75 en las tres extensiones; coincide en15:28 y falla en15:26/15:27. No debe generalizarse esa irrelevancia a partir de la pareja75/75.

Al eliminar primeras velas aparecen tanto cambios como mesetas. El mayor cambio de este barrido es93→75 al eliminar15:27:END y extremos permanecen iguales y la ventana restante conserva exactamente su OHLC. Esto no identifica si el cálculo usa conteo, la primera vela, un segmento elegido o estado recursivo; esas entradas cambian junto con START.

## Predicciones de continuidad al añadir15:52

Como añadir15:52 había conservado C en START15:29/15:30, se predijo antes de medir que conservaría93 y75 en START15:27/15:28. **Ambas predicciones fallaron.**

| START | C END15:51 | Predicción END15:52 | C medido END15:52 |
|---|---:|---:|---:|
|15:27|93|93|82|
|15:28|75|75|81|
|15:29,controles anteriores|75|—|75|
|15:30,controles anteriores|68|—|68|

La misma vela15:52 conserva C en algunos rangos y lo cambia en otros; los extremos globales siguen iguales. No inferir que una vela es irrelevante para el generador sin especificar el rango. El fallo de esta extrapolación se conserva como resultado, sin modificar la predicción después de observarlo.

La pareja15:27–15:51 C93 y15:28–15:52 C81 tiene25velas y los mismos extremos globales, pero distinto C. La pareja de26velas15:26–15:51/15:27–15:52 da82 en ambas; esa coincidencia aislada no demuestra una función del conteo.

## Repetición y auditoría

Después de las dos pruebas END15:52 se volvió a15:27–15:51. Pareja e/f recupera93 y coincide exactamente con la primera exportación d en40,176celdas de16plots comunes cerrados. El pico se reproduce desde otra selección y no se acepta basándose solo en la primera captura.

Las seis parejas nuevas comparan241,232celdas estables. Las ocho selecciones del analizador (seis nuevas y dos reutilizadas) pasan coberturaOHLC, seis estimaciones Lite concordantes, residuos de EMA de cierre y C Lite compatible con las diez curvas Character. Última fila de CSV excluida; tolerancias numéricas1e-7segundos para C y1e-8 para límites de intervalos. No hay fallas pendientes.

Script `analizar_C_END1551.py`; datos `C_END1551.json`. CSV/capturas en `manual/C_END1551_START_1526/1527/1528/1531_*`, `manual/C_END1552_START_1527/1528_*`. Los controlesSTART29/30 están en archivos de la tanda anterior. Para pico93 se acepta e/f y se preserva c/d. Predicciones registradas en `C_DECIMALES_PREDICCIONES.md`.

Layout restaurado y guardado en12oct18:55–19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado. Captura `manual/C_END1551_restaurado.png`.

## Alcance y siguiente trabajo

No se obtuvo la fórmula de C. El resultado fortalece la necesidad de una regla conjunta del rango: un mismo sufijo, extremos iguales o una vela de END por separado no bastan.

Antes de seguir extendiendo esta matriz, consolidar todos los controles en un conjunto de validación y exigir a un candidato explícito explicar los picos81/93, las mesetas75/68 y los fallos de continuidad. La hipótesis debe definir selección de segmento y cálculo numérico, y predecir otra fecha o rango reservado. Más mediciones de esta zona por sí solas no identificarán una fórmula única.
