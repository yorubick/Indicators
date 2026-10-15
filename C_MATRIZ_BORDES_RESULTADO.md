# Matriz completa de bordes: interacción START/END

14 octubre2026. Litev1.2 sin actualizar, NQ1!, fuente/gráfico1minuto en copiaxqM5dZIf. Día12octubre UTC. Dos esquinas nuevas preregistradas en C_MATRIZ_BORDES_PREREGISTRO.json, siete puntos anteriores recuperados de auditorías guardadas. Character excluido.

| START / END incluido |19:19|19:20|19:21|
|---|---:|---:|---:|
|18:54|134|134|109|
|18:55|107|62|106|
|18:56|77|109|134|

Los nuevos casos son18:54–19:21,n28,C109 y18:56–19:19,n24,C77. Ambos se midieron con dos exportaciones y seis ajustes independientes. OHLCV nativo coincide exactamente con referencia sobre timestamps cerrados comunes; rangos completos y una hora posterior presentes, última fila excluida. C concuerda entre canales con dispersión<10⁻⁶ y RMSE<10⁻⁸; visibilidad coincide con primera ruptura. Regreso18:55–19:20 reproduce exactamente referencia y C62.

Con END19:19, las tres filas tienen H30868.75,L30846,ruptura alcista19:20 ysemilla30862.50. Con END19:20,todas tienen H30870.50,L30846,ruptura19:26 ysemilla30864.50. Con END19:21,todas tienen H30870.50,L30846,ruptura19:26 ysemilla30866.50. C varía en cada columna pese a esos controles compartidos. Las diagonales de n constante conservan distintos C, como se comprobó antes.

Una función aditiva C=f(START)+g(END), a resolución fija, requiere diferencias mixtas iguales a cero. Las cuatro diferencias observadas son−45,+69,+77 y−19; por tanto esa forma simple tampoco explica la matriz. Esto es una comprobación algebraica posterior, no un modelo predictivo ajustado. No excluye formas no lineales, redondeos de variables latentes, mecanismos temporales más complejos, geometría normalizada ni estado previo.

La combinación central C62 es menor que sus ocho vecinos, pero llamarla resonancia o alineación armónica sería una interpretación sin prueba. Los resultados disponibles no identifican qué variable selecciona C. El conteo, la hora y la geometría cambian conjuntamente y la matriz local por sí sola no separa causalidad.

Siguiente paso propuesto: analizar los nueve rangos con medidas normalizadas de geometría (posición inicial/final dentro de H/L, eficiencia del recorrido, cuerpos/mechas y distancias a EMAs históricas de longitudes declaradas). Priorizar candidatos por capacidad de explicar controles ya observados sin umbrales en puntos que violen las simetrías. Antes de medir otra ventana, fijar una predicción diferenciadora y evitar elegir la fórmula por un ajuste retrospectivo de esta matriz. No se ha realizado aún ese análisis ni descubierto una regla.

Auditoría: analizar_C_matriz_bordes.py y C_matriz_bordes_resultados.json reúnen9casos, diferencias mixtas, geometría, hashes de nuevosCSV y regreso. Datos nuevos en manual/C_startSweep1920_bordes_1854_1921_* y*_1856_1919_*. Captura C_matriz_bordes_final.png. Gráfico restaurado y guardado en18:55–19:20,NQ1!,1m; layout principal sin cambios.
