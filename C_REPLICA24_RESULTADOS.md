# Búsqueda prospectiva de réplica de duración/24

13 octubre 2026. Se hicieron dos mediciones nuevas en TradingView, fuente y gráfico1m, CharacterB/Manual/sourceChart y Lite1m. No se actualizó el indicador ni se usaron los27 controles reservados para validación.

## Selección y predicción congeladas

`seleccionar_C_replica24.py` comparó660 ventanas continuas de21 velas del13oct entre07:00 y17:59 UTC, rango>=5puntos. Para cada ventana normalizó los84 valores OHLC por su mínimo y máximo global y calculó la menor distancia RMS respecto de las tres plantillas de21velas de entrenamiento conC50. Seleccionó las dos mejores ventanas que no se solapan. No leyó C/curvas de las ventanas candidatas.

Se guardó `C_replica24_predicciones.json` antes de medir: C50 para ambas. Si alguna coincidía, se había previsto ampliarla a22/23/24velas con predicciones52/55/57. Esa condición no se cumplió; no se hicieron las extensiones.

Es una selección exploratoria por semejanza, no un clasificador validado. No se fijó un umbral para declarar semejanza suficiente. Los84 valores de cada candidata no son idénticos a sus plantillas.

## Resultados

| START–END UTC, 13oct | RMS normalizado | Rango puntos | Predicción | C medido |
|---|---:|---:|---:|---:|
|11:14–11:34|0.14967625|42.25|50|82|
|15:33–15:53|0.15843484|35.50|50|66|

`analizar_C_replica24.py` verificó OHLC exactos frente al preregistro, repetición de16curvas, acuerdo de los seis C recuperados de Lite<1e-7, residuos de recurrencia<1e-8 y compatibilidad con el intervalo recuperado de Character. Las parejas aceptadas son1:c/d y2:e/f, con87696 celdas de curvas repetidas en total; no quedan fallos en las parejas finales.

La pareja2:c/d no fue estable durante el recálculo y se conservó sin usarla para el resultado. Se descargaron e/f y superaron la comprobación. Archivos y capturas de configuración: `manual/C_replica24_1_*` y `manual/C_replica24_2_*`. Resultados detallados: `C_replica24_resultados.json`.

## Interpretación

No encontramos una réplica de la fórmula parcial con este procedimiento. La semejanza de OHLC normalizados, tal como se definió aquí, no fue suficiente para predecirC50. Esto no refuta la posibilidad de una rama duración/24 con otra condición, ni todas las fórmulas que dependen de la forma del precio. Amplitud absoluta, microestructura de otra resolución e información exterior al rango siguen siendo posibles entradas; estas mediciones no las aíslan.

No promover duración/24 a rama del generador ni ajustar un umbral de semejanza con estos dos resultados. El siguiente contraste debe aislar una entrada concreta. Un candidato es repetir la misma selección temporal original usando gráfico y fuente15s alineados y comparar con1m, registrando qué velas inclusivas se agregan; eso probaría la dependencia de resolución, no permitiría atribuir por sí solo el cambio a un componente del cálculo.

Se restauraron y guardaron ambas anclas al12oct18:55–19:20 UTC y la vista al episodio original. Captura: `manual/C_replica24_restaurado.png`. El indicador de volumen ya estaba visible al iniciar este turno y se conservó su estado.
