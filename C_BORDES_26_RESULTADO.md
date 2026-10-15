# Conteo fijo no determina C: 26 velas producen134,62,134

14 octubre 2026. Mediciones reales en copia xqM5dZIf, Litev1.2 sin actualizar, NQ1!, fuente/gráfico1m. Día12 octubre UTC. Protocolo previo en C_BORDES_26_PREREGISTRO.json. Dos exportaciones por cada caso, seis ajustes independientes; Character excluido.

| START | END incluido | n | C | H | L | Ruptura UTC | Semilla |
|---|---|---:|---:|---:|---:|---|---:|
|18:54|19:19|26|134|30868.75|30846.00|19:20|30862.50|
|18:55|19:20|26|62|30870.50|30846.00|19:26|30864.50|
|18:56|19:21|26|134|30870.50|30846.00|19:26|30866.50|
|18:55|19:19|25|107|30868.75|30846.00|19:20|30862.50|
|18:55|19:21|27|106|30870.50|30846.00|19:26|30866.50|

Con n26 y resolución constante, C134/62/134 refuta una función exclusiva del conteo en estas condiciones. Dos de esas ventanas conservan además H/L y hora de ruptura (18:55–19:20 frente18:56–19:21), pero cambian START,END,semilla y demora posterior de6 a5minutos. No se aisló un ancla temporal ni toda la geometría.

START18:55 fijo, END19:19→19:20→19:21 entrega C107→62→106. El segundo cambio conserva H/L y ruptura pero altera vela END,semilla y conteo. El barrido anterior con END19:20 fijo entregó para START18:54→18:55→18:56 los valores134→62→109. Son efectos de ambos bordes; no se justifican offsets armónicos universales. El cambio134→107=27 en dos casos es una coincidencia local que requiere una predicción nueva y controles independientes; otros cambios no son múltiplos de27.

Controles completados: los timestamps nativos de cada rango y una hora posterior están presentes; OHLCV coincide exactamente con referencia nativa independiente sobre velas cerradas comunes. Dos exportaciones por caso reproducen seis curvas y OHLCV. Cada ajuste entrega C coherente entre los seis canales (dispersión<10⁻⁶,RMSE<10⁻⁸). Primera visibilidad coincide con primera ruptura alcista. Última fila excluida para evitar vela abierta. Regreso18:55–19:20 reproduce referencia y C62.

Para el siguiente contraste conviene completar las dos esquinas faltantes de la matriz3×3:18:54–19:21 y18:56–19:19. Los otros siete puntos ya están medidos entre este cruce y el barrido anterior. La matriz final permitirá cuantificar interacción START/END y comparar n repetido, extremos, semilla y geometría normalizada. Los modelos construidos sobre ella serán exploratorios y necesitarán predicciones en ventanas nuevas.

Auditoría: analizar_C_bordes26.py y C_bordes26_resultados.json con geometría de ambas velas de borde, timestamps de extremos, seis ajustes, controles y hashes SHA256. CSV en manual/C_startSweep1920_bordes_*. Captura final C_bordes26_final.png. Gráfico restaurado y guardado en18:55–19:20,NQ1!,1m. Layout principal sin cambios.
