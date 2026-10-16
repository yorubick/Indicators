# Ventanas mínimas y primer contraejemplo a C siempre entero

13 de octubre de 2026. Mediciones nuevas, NQ1!, ETH, UTC, BADJ apagado. Anclas del12 de octubre. Gráfico1m. Lite v1.2 fuente explícita1m; Character v6.5.36 perfilB Manual fuenteChart. START fijo19:00 salvo control de retirada.

## Resultados

| START | END | Velas incluidas | C recuperado Lite | C entero compatible Character |
|---|---|---:|---:|---|
| 19:00 | 19:00 | 1 | No observable | No observable |
| 19:00 | 19:01 | 2 | 60 | 60 |
| 19:00 | 19:02 | 3 | 60 | 60 |
| 19:00 | 19:03 | 4 | 60 | 60 |
| 19:00 | 19:07 | 8 | 60 | 60 |
| 19:00 | 19:11 | 12 | 60 | 60 |
| 19:00 | 19:15 | 16 | 60 | 60 |
| 19:00 | 19:16 | 17 | 60 | 60 |
| 19:00 | 19:17 | 18 | 60 | 60 |
| 19:00 | 19:18 | 19 | 62.2950819672 | Ninguno; intervalo compatible con Lite |
| 19:00 | 19:19 | 20 | 65.5737704918 | Ninguno; intervalo compatible con Lite |
| 19:00 | 19:20 | 21 | 77 | 77 |
| 19:01 | 19:18 | 18 | 60 | 60 |

## Hallazgo principal

En las ventanas19:00–19:18 y19:00–19:19, C no es entero. Las seis curvas Lite recuperan el mismo decimal con dispersión inferior a1e-8 segundos, y los intervalos de Character contienen ese C sin admitir ningún entero. Para END19:18 el intervalo Character es [62.13483146,62.35955056); por tanto ni62 ni63 son posibles con la familia reconstruida.

Esto refuta la hipótesis general de cuantizar siempre C a segundos enteros en estos modos. Los catorce controles Lite anteriores sí daban enteros; su observación no se generaliza. Un listado vacío de enteros compatibles no significa ausencia de C ni fallo de medición: se conserva el intervalo y el C decimal de Lite.

## Transición y retirada

Entre END19:17 y19:18, C sale del mínimo observado60 sin cambiar el máximo30864.50 ni el mínimo30846.00 del rango. La vela añadida19:18 tiene O30854.00, H30863.00, L30853.50, C30863.00: no crea un extremo global. Al retirar la vela inicial19:00 y conservar END19:18, C vuelve a60; el mínimo del nuevo rango cambia a30849.00. Esa retirada no aísla por sí sola conteo frente a precio.

Los dos C decimales son numéricamente compatibles con3800/61 y4000/61, respectivamente; equivalen en estos dos casos a número de velas×200/61. Esta identidad local no es una fórmula descubierta. Para21 velas produciría68.852459, pero medimos77. Una regla que depende únicamente del conteo con esa pendiente falla en el siguiente END.

Los END19:04–19:06,19:08–19:10 y19:12–19:14 no se midieron. Por ello no se afirma haber localizado la ventana no saturada más corta de todo el episodio: se localizó una transición concreta entre dos finales consecutivos19:17/19:18. El siguiente experimento debe usar una fuente más fina y otro episodio para obtener una ventana informativa con menos velas y distinguir saturación, normalización y selección de estructura.

## Verificación y limitaciones

Cada rango válido tiene dos exportaciones aceptadas y una adicional de recálculo conservada como diagnóstico. El análisis compara exactamente16 curvas (6 Lite,10 Character) en todos los timestamps cerrados comunes de cada pareja; verifica cobertura OHLC completa y acuerdo de C Lite con el intervalo Character. No se editaron velas ni se accedió a código protegido.

La prueba de START=END no ofrece curvas en ninguno de los dos indicadores, aunque los OHLC del rango están presentes. Se registra como no observable, sin deducir C=0 ni una prohibición universal del rango de una vela.

Al inicio, Go to conservó la fecha actual13 de octubre. Los primeros archivos a/b de la prueba de una vela se excluyen porque no cubrían el rango histórico. Se corrigió explícitamente la fecha a12 de octubre; c/d son la pareja utilizada para ese caso. No se sobrescribieron los archivos diagnósticos. Las demás parejas tienen el rango completo confirmado.

Scripts: comparar_Lite_Character.py y analizar_C_ventanas_minimas.py. Resultado: C_ventanas_minimas.json con todos los OHLC de cada selección e intervalos. CSV manual/Lite_1900_HHMMSS_1m_[a/b].csv; END19:20 conserva etiqueta1920. Control de retirada: Lite_1901_191800_1m_[a/b].csv. Evidencia: C_minimas_1900_1920.jpg y C_minimas_1901_1918.jpg.

Al finalizar se restauraron START18:55–END19:20, fuente/gráfico1m y se guardó el layout. Captura C_minimas_referencia_final.jpg. El generador de C continúa pendiente.
