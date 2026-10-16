# C: ventanas18–24 y desplazamientos de21

13 octubre 2026. Dieciséis controles nuevos de NQ1!,12oct2026, ETH, UTC, BADJ apagado y Replay apagado. Fuente y gráfico de un minuto, Lite v1.2 fuente1m y Character Tree v6.5.36 perfilB Manual fuenteChart. Se eligieron START06:00 y14:00 antes de observar los valores. El conteo es inclusivo:18velas terminan17min después de START.

## Resultado de las predicciones

| Velas | Continuación de regla corta | C START06:00 | C START14:00 |
|---|---:|---:|---:|
|18|60|60|60|
|19|62.29508197|62.29508197|62.29508197|
|20|65.57377049|65.57377049|65.57377049|
|21|68.85245902|77|62|
|22|72.13114754|77|62|
|23|75.40983607|77|83|
|24|78.68852459|73|76|

En ambos tramos las tres predicciones cortas pasan y la primera divergencia aparece en21velas. Esto refuerza la frontera previamente observada en otros rangos y fuentes; no prueba que sea universal ni revela cómo se calcula la rama larga. El valor alternativo77/62 no fue predicho: esos resultados son diagnósticos.

Con21velas, mismo símbolo, fecha, resolución y conteo dan C77 yC62. Por tanto, el conteo y la resolución por sí solos no determinan C en estos casos de la rama larga. Los extremos globales permanecen constantes en cada barrido18..24:06:00 high31208.50/low31159.25;14:00 high30974.50/low30867.25. Dentro de cada tramo, C cambia sin cambiar los extremos globales, aunque sí cambian conteo y OHLC internos.

Ambos tramos tienen movimiento neto de cierre bajista. No se presentan como muestra balanceada de tendencia, lateral y reversión; ese contraste de estructuras sigue pendiente. Las ventanas de un mismo tramo se solapan; los dos tramos no se solapan, pero pertenecen a la misma jornada.

## Ventanas de21velas desplazadas una vela

| Ventana base -> desplazada | C base -> nueva | Cambio de extremos |
|---|---|---|
|06:00–06:20 ->06:01–06:21|77 ->80|High31208.50 ->31201.50; low igual|
|14:00–14:20 ->14:01–14:21|62 ->62|High ylow iguales|

Estos dos controles mantienen21velas y sustituyen la primera por una nueva al final. En06:00 se elimina la vela del máximo global: el cambio de C no puede atribuirse aisladamente al prefix o al high. En14:00 cambia la secuencia pero C permanece62: no toda sustitución de una vela exige cambiar C. Son controles diagnósticos, sin una predicción numérica de la fórmula general.

La vela eliminada06:00 tiene OHLC31203.50/31208.50/31201.50/31203.00; la añadida06:21,31164.75/31172.25/31163.25/31171.25. En14:00 la eliminada es30960.75/30971.00/30956.00/30966.50 y la añadida14:21,30914.00/30915.25/30890.75/30894.50. Los OHLC completos están preservados en JSON.

## Auditoría

Cada resultado aceptado pasa: cobertura completa del rango OHLC, coincidencia exacta de16curvas en exportaciones repetidas cerradas, seis estimaciones Lite concordantes dentro de1e-7segundos, residuos EMA de cierre menores1e-8, y C Lite dentro del intervalo compatible de las diez curvas Character (tolerancia1e-8segundos en límites numéricos). Los16controles pasan; ninguna falla pendiente.

Las primeras exportaciones06:00 de19,20y21velas mostraron curvas Character obsoletas o una pareja inestable. Se conservaron a/b y se repitieron c/d después de comprobar anclas y recálculo. La estabilidad de un par por sí sola no se aceptó como prueba suficiente. Control06:00/18 usa a/b; demás barridos y desplazamientos usan c/d. Las capturas de configuración se guardaron durante las mediciones, sin actualizar versiones.

Script `analizar_C_fronteras_nuevas.py`; salida `C_fronteras_nuevas.json`, incluyendo OHLC, intervalos Character, métricas de recorrido, extremos, conteos y archivos aceptados. Predicciones en `C_DECIMALES_PREDICCIONES.md`. CSV en `manual/C_frontera_nueva_0600_*`, `manual/C_frontera_nueva_1400_*`, y `manual/C_frontera_shift_0601/1401_*`.

Layout restaurado y guardado: START12oct18:55,END19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado. Captura `manual/C_fronteras_nuevas_restaurado.png`.

## Siguiente prueba útil

La siguiente hipótesis debe explicar tanto la frontera20/21 como los valores distintos77y62 con21velas. Antes de buscar más fórmulas amplias, completar ventanas de21velas con dirección alcista y un rango lateral, luego barrer START una vela manteniendo END fijo para identificar cuándo cambia C y qué datos quedan incluidos. Cada regla candidata debe producir una predicción numérica en otra ventana reservada; una coincidencia retrospectiva no cuenta como generador recuperado.

No se recuperó la fórmula general de C ni código protegido. Este informe confirma nuevas predicciones de la rama corta y agrega observaciones controladas de la rama larga.
