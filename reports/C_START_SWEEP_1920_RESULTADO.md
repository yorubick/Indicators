# Barrido START con END19:20: saltos de C con extremos y ruptura constantes

14 octubre 2026. Prueba real en copia xqM5dZIf, Lite v1.2, fuente/gráfico1m, NQ1!. Día12 octubre UTC, END fijo19:20 incluido. Protocolo previo en C_START_SWEEP_1920_PREREGISTRO.json. Dos exportaciones por cada una de las15 ventanas; Character excluido.

| START | n | C | H | L | Primera ruptura UTC |
|---|---:|---:|---:|---:|---|
|18:48|33|118|30877.50|30844.25|19:32|
|18:49|32|134|30871.75|30844.25|19:26|
|18:50|31|118|30870.50|30844.25|19:26|
|18:51|30|118|30870.50|30844.25|19:26|
|18:52|29|125|30870.50|30844.25|19:26|
|18:53|28|121|30870.50|30846.00|19:26|
|18:54|27|134|30870.50|30846.00|19:26|
|18:55|26|62|30870.50|30846.00|19:26|
|18:56|25|109|30870.50|30846.00|19:26|
|18:57|24|77|30870.50|30846.00|19:26|
|18:58|23|77|30870.50|30846.00|19:26|
|18:59|22|77|30870.50|30846.00|19:26|
|19:00|21|77|30870.50|30846.00|19:26|
|19:01|20|65.57377049|30870.50|30849.00|19:26|
|19:02|19|62.29508197|30870.50|30849.00|19:26|

En18:53–19:00 son idénticos H/L, altura24.50, END, ruptura alcista19:26 y semilla END low30864.50. El tramo posterior es idéntico. C cambia121→134→62→109→77 y permanece77 al reducir n24→21. También18:50–18:52 conservan H/L y ruptura pero C118→118→125.

Inferencia: C no es función exclusiva de H/L, dirección y tiempo END→ruptura. Tampoco varía monótonamente con duración en este barrido. No se descarta un mecanismo no monotónico basado en n, tiempos, posición relativa inicial, forma normalizada o historial previo. START cambia conteo y geometría simultáneamente; igualdad de extremos no equivale a igualdad de toda la forma. Los valores finales n20 y19 coinciden con la regla corta previamente verificada C=n×60×10/183, como comprobación posterior a la medición. La transición n21 entrega77 y pertenece a otra rama.

Cada par de exportaciones reproduce OHLCV y seis curvas sobre sus timestamps cerrados comunes. OHLCV coincide exactamente con referencia nativa independiente. Cobertura completa de cada rango y una hora posterior. Ajustes EMA independientes entregan C concordante en seis canales con dispersión menor que10⁻⁶ y RMSE menor que10⁻⁸. La primera aparición de cada canal coincide con la primera ruptura. Última fila de cada CSV excluida. Regreso a18:55 reproduce exactamente la referencia y C62.

Próximo contraste propuesto: tres ventanas de26velas,18:54–19:19,18:55–19:20 y18:56–19:21, más controles con START18:55 y END19:19/19:21. Este cruce permite comprobar si distintos C aparecen con n fijo y distinguir el efecto observado al cambiar cada borde. Verificar previamente extremos, ruptura y semilla en todas; cualquier cambio se documenta y limita la interpretación. No garantiza aislar toda la geometría ni un ancla oculta. Las predicciones de cualquier fórmula nueva que use este barrido deben declararse antes de medir esas ventanas.

Auditoría reproducible: analizar_C_startSweep1920.py genera C_startSweep1920_resultados.json con ajustes, geometría inicial, timestamps de extremos, comparaciones, hashes y controles compartidos. CSV/captura en manual/C_startSweep1920_*. Gráfico restaurado y guardado en START18:55,END19:20,NQ1!,1m. Layout principal sin cambios.
