# C: nuevos máximos y primera ruptura no bastan

13 de octubre de2026. Siete selecciones nuevas en NQ1!,12 de octubre, ETH, UTC, BADJ apagado. Fuente/gráfico60s, Lite v1.2 fuente explícita1m; Character v6.5.36 perfilB Manual fuenteChart. Todas pasan cobertura OHLC completa, igualdad exacta de16 curvas cerradas por pareja y acuerdo de C Lite/intervalo Character con tolerancia1e-8.

## Ventanas de longitud fija que incluyen19:25

| Selección | Velas | C |
|---|---:|---:|
| 19:03–19:24, anterior | 22 | 52 |
| 19:04–19:25, nueva | 22 | 71 |
| 19:02–19:24, anterior | 23 | 55 |
| 19:03–19:25, nueva | 23 | 71 |

Ambas ventanas nuevas incluyen la vela19:25 y elevan el máximo global hasta30871.25. El control anterior19:02–19:25 de24 velas también daba71. La repetición apoya estudiar selección de estructura, pero no identifica cuál ni prueba causalidad del máximo: desplazar la ventana también cambia los OHLC iniciales.

## START fijo19:04 y END consecutivos

| END | Velas | C | Máximo global | Mínimo global | Primera ruptura por cierre |
|---|---:|---:|---:|---:|---|
| 19:24, anterior | 21 | 50 | 30870.75 | 30849.00 | 19:26 |
| 19:25 | 22 | 71 | 30871.25 | 30849.00 | 19:26 |
| 19:26 | 23 | 71 | 30873.00 | 30849.00 | 19:29 |
| 19:27 | 24 | 71 | 30874.75 | 30849.00 | 19:29 |
| 19:28 | 25 | 128 | 30874.75 | 30849.00 | 19:29 |
| 19:29 | 26 | 134 | 30876.00 | 30849.00 | 19:30 |
| 19:30 | 27 | 109 | 30877.50 | 30849.00 | 19:32 |

Dos máximos nuevos19:26 y19:27 no cambian C71. Añadir19:28 cambia C71→128 sin nuevo extremo global. Por tanto, crear un máximo nuevo no es condición suficiente ni necesaria para cambiar C en estas selecciones.

## Predicción previa contrastada

Se registró antes de medir19:26–28 la hipótesis restringida C=f(maxglobal,minglobal). Puesto que19:28 no superaba el máximo19:27, esa regla predecía C27=C28. La medición71 frente a128 la refuta. Es un rechazo de la regla basada exclusivamente en esos extremos, no de todos los algoritmos que los utilicen.

El par19:27/19:28 ofrece además una comparación con la misma ruptura: ambas ventanas rompen por arriba el19:29 con close30875.75. Conservan START19:04, máximos/mínimos globales, timestamp, dirección y precio de la primera ruptura. Aun así dan71 y128. No basta una función que reciba únicamente esos datos. Cambian END, conteo y OHLC de END: no se excluye usar esas entradas ni el recorrido completo.

El tiempo entre END y ruptura tampoco basta por sí solo: un retraso de una vela se observa con C71(END19:25),128(19:28) y134(19:29). Tampoco se demuestra que el generador ignore cotizaciones posteriores a END; eso sigue abierto por la auditoría de observabilidad.

La vela19:28 tiene O30873.25,H30874.50,L30869.50,C30872.75. Su máximo es menor que el del19:27 y el cierre retrocede0.25. Es compatible con confirmar un giro local de una vela a cada lado. No se convierte esa coincidencia en explicación de C128: falta definir el selector y probarlo en otros episodios. Los controles anteriores ya mostraron cambios de C con y sin reversión.

## Archivos y siguiente control

Analizar_C_matriz.py y C_matriz.json ahora incluyen24 selecciones comprobadas y la primera ruptura de cada una. Los siete archivos nuevos son manual/Lite_1903_192500_1m_[a/b].csv y Lite_1904_192500/192600/192700/192800/192900/193000_1m_[a/b].csv. Los pendientes se conservan; no se sobrescribieron mediciones anteriores.

Capturas C_maximo_*_anclas.jpg. Referencia12 de octubre18:55–19:20, fuente/gráfico1m, restaurada y guardada; C_maximo_referencia_final.jpg.

Para la siguiente prueba conviene definir una regla concreta de selección de pivotes y registrar qué evento elegiría en cada ventana antes de comparar C. Separar «cambia la estructura seleccionada» de «cómo esa estructura se transforma numéricamente en C». Estos controles restringen entradas posibles, pero todavía no recuperan el generador general.
