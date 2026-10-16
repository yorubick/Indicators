# Lite: START dentro de una vela del gráfico

13 octubre 2026. NQ1!, ETH, UTC, BADJ apagado, Replay apagado. Lite v1.2, fuente explícita 15 segundos, END fijo 12 octubre 19:04:45 UTC. Character quedó en su referencia sin modificar; este informe analiza solo Lite.

## Predicciones y resultado

Se eligió una ventana corta porque las tres hipótesis daban valores distintos según la regla corta previamente observada: C=max(15,n*15*10/183), con n inclusivo. Las predicciones se registraron en `C_DECIMALES_PREDICCIONES.md` antes de medir.

| Configuración | Número de velas nativas | C recuperado |
|---|---:|---:|
| Gráfico15s, START19:00:00 |20|16.39344262295|
| Gráfico15s, START19:00:15 |19|15.57377049180|
| Gráfico1m, mismas anclas START19:00:15 y END19:04:45 |Compatible con19|15.57377049180|

Incluir el minuto completo de START habría predicho16.39344262295; comenzar en el siguiente minuto habría predicho15. Ambas predicciones se refutan en este contraste. Conservar la subvela START seleccionada predice el valor observado.

Los dos controles nativos contienen exactamente20 y19 velas, respectivamente, con los mismos extremos globales (high30863.50, low30846.00). La diferencia de C no se explica por un cambio de esos extremos. En cada control las seis curvas recuperan C por separado con residuos de aproximadamente1e-12. En gráfico1m, cuatro actualizaciones sucesivas con cierres15s reproducen las transiciones observadas y recuperan el mismo C19, RMSE máximo6.98e-12 en1574 transiciones por curva. No se ajustó una EMA15s contra cierres agregados1m.

## Niveles y publicación

Igual C no significa iguales niveles: la comparación directa entre fuente y gráfico15s y el gráfico1m alineado a su última subvela tiene error máximo0.05581636 puntos. Se conserva este resultado, sin ocultarlo.

Al aplicar la semilla alcista del mínimo de la vela END del gráfico1m (30858.00), END efectivo19:04:45, actualizaciones posteriores con cierres15s y C19=15.573770491803279, se reproducen9546 valores (1591 por curva), error máximo4.37e-11. El primer cierre fuera del rango inclusivo es alcista a19:19:15; la visibilidad reconstruida posterior a END coincide en todas las muestras comparadas.

Las exportaciones repetidas coinciden exactamente:38,172 valores Lite del control START00,38,178 del control START15 y9576 del gráfico1m; sin discrepancias de visibilidad. Última fila de cada CSV excluida.

## Conclusión limitada

En esta ventana, cambiar el gráfico a1m conserva el comportamiento compatible con START19:00:15 nativo; no hay evidencia de que incluya todo el minuto START ni espere al minuto siguiente. **No aplicar a START la normalización de END.** Los controles respaldan un tratamiento distinto de los dos límites.

La selección interna exacta no puede leerse del código protegido. Una equivalencia de curvas y de conteo inferido respalda la hipótesis, pero no prueba todas las ventanas, símbolos, resoluciones o direcciones. Este control pertenece a la rama corta ya identificada; no resuelve el generador de C de ventanas mayores. Las discrepancias de Character entre intervalos siguen pendientes.

## Archivos y siguiente paso

Script `analizar_Lite_START_efectivo.py`; resultados `Lite_START_efectivo.json`. CSV y capturas en `manual/Lite_START_190000_*` y `manual/Lite_START_190015_*`. El script de reconstrucción compartido `analizar_Lite_END_efectivo.py` ahora acepta START opcional; mantiene18:55 como valor predeterminado para reproducir las pruebas anteriores.

Layout restaurado y guardado: gráfico1m, Lite fuente1m, Character fuenteChart, START18:55 END19:20 del12oct, Replay apagado. Captura `manual/Lite_START_efectivo_restaurado.png`.

Siguiente contraste: dirección bajista con fuente y gráfico iguales para comprobar semilla high, y luego pasar al gráfico agregado manteniendo anclas exactas. Después se podrá comparar el generador de C de Lite y Character con ventanas normalizadas, sin confundir diferencias de publicación o semilla con diferencias de C.
