# C decimal: relación por conteo y posible rama para ventanas cortas

13 de octubre de2026. NQ1!, ETH, UTC, BADJ apagado, gráfico1m. Lite v1.2 fuente1m; Character v6.5.36 perfilB Manual fuenteChart. Anclas del12 de octubre. Se hicieron siete nuevos controles, con cobertura OHLC y comparación de16 curvas cerradas por pareja.

## Predicciones previas

Se fijó C=max(60,n*200/61), donde n es el conteo inclusivo de velas, a partir de los dos decimales anteriores. Las cuatro primeras predicciones y las dos del episodio bajista se escribieron en C_DECIMALES_PREDICCIONES.md antes de medirlas. Se sabía que la regla universal ya fallaba en19:00–19:20: el objetivo es delimitar la relación local, no rescatarla con coeficientes elegidos por caso.

| START | END | n | Predicción | C medido |
|---|---|---:|---:|---:|
| 18:59 | 19:18 | 20 | 65.57377049 | 65.57377049 |
| 18:58 | 19:18 | 21 | 68.85245902 | 77 |
| 19:01 | 19:19 | 19 | 62.29508197 | 62.29508197 |
| 18:59 | 19:19 | 21 | 68.85245902 | 77 |
| 04:45 | 05:03 | 19 | 62.29508197 | 62.29508197 |
| 04:45 | 05:04 | 20 | 65.57377049 | 65.57377049 |
| 04:45 | 05:05 | 21 | 68.85245902 | 75 |

Las seis predicciones previas aciertan cuatro: las ventanas19/20. Fallan ambas de21. La séptima medición extiende el control de frontera al episodio bajista; el C75 de Character de esa selección ya era conocido, por lo que no se presenta como una predicción nueva independiente.

## Qué aporta

Las ventanas19/20 recuperan exactamente los mismos decimales en episodios distintos, con diferentes precios, extremos, anclas y dirección. La selección19:01–19:19 cambia tanto el máximo como el mínimo respecto a19:00–19:18, conservando19 velas y C62.29508197. El caso bajista tiene extremos31259.25/31235.75 y comparte esos decimales con el alcista. Esto fortalece la hipótesis de una regla por conteo para las ventanas cortas.

Al pasar de20 a21 velas hay dos clases de resultados en estas muestras: el alcista da77 y el bajista75, ambos fuera de la continuación proporcional68.85245902. En el par18:59–19:18 frente a18:58–19:18, ambos extremos globales y END son idénticos; solo se incluye una vela anterior, y C pasa de65.57377049 a77.

Es compatible con una rama de respaldo o calentamiento que usa conteo cuando hay pocas velas y cambia de cálculo al superar un umbral. **No se demostró el código de esa rama ni un umbral universal de21.** También podría intervenir un selector estructural que coincida en estos conteos. Todas las observaciones son de una misma jornada y dos episodios, no una validación entre jornadas.

La regla candidata para fuente60s y ventanas cortas es max(60,200*n/61). No se ha establecido cómo se normaliza en otras fuentes. No debe trasladarse a15s simplemente sustituyendo60 por15 sin medirlo. Como C usa n inclusivo en esta relación, sustituir n por los minutos transcurridos entre anclas predice otra cantidad y no reproduce los decimales.

## Verificación

Las seis curvas Lite concuerdan en C con dispersión inferior a1e-8 segundos. Cada media de C pertenece al intervalo inferido de Character. Los períodos Character no admiten un entero en los casos decimales; eso no se trata como una extracción fallida. Se comprobaron OHLC completos y16 plots cerrados comunes exactamente iguales entre las parejas aceptadas.

La pareja a/b de04:45–05:05 no coincidía en Character por recálculo incompleto. Se conserva y se rechaza para comparar estabilidad; c/d sí coincide y es la pareja aceptada de ese control. Los datos pendientes se conservan sin sobrescribir archivos.

## Próximo contraste que discrimina

Repetir n19/20/21 con fuentes15s y2m y en otra jornada, fijando predicciones explícitas antes de medir. Si la normalización sigue fuente×conteo, debe explicar los decimales de las otras resoluciones y mantener una frontera por número de velas. Si cambia la frontera o la pendiente, registrar ese resultado antes de formular excepciones.

Investigar la rama que produce75/77 y otros C mayores sin mezclarla con el posible respaldo de ventanas cortas. La fórmula generadora general sigue pendiente, pero ahora hay una regla local con predicciones verificadas y una frontera medible.

Archivos: C_DECIMALES_PREDICCIONES.md; analizar_C_regimen_decimal.py; C_regimen_decimal.json con todos los OHLC y restricciones. CSV manual/Lite_HHMM_HHMMSS_1m_[a/b].csv, con c/d para04:45–05:05. Captura C_decimales_bajista_0445_0504.jpg. Referencia START18:55–END19:20, fuente/gráfico1m, restaurada y guardada; C_decimales_referencia_final.jpg.
