# Lite: límite efectivo de END y semilla en gráficos agregados

13 octubre 2026. Continuación del contraste `C_FUENTE_VS_GRAFICO.md`. NQ1!, ETH, UTC, BADJ apagado, Replay apagado. Lite v1.2, fuente explícita 15s, START 12 octubre 18:55:00 UTC. Character conserva su referencia; este informe compara exclusivamente las seis curvas Lite.

## Resultado

| Contraste | C nativo recuperado | Comparación de niveles |
|---|---:|---|
| Gráfico 15s END 19:20:15 frente a gráfico 30s END 19:20:00 |79|18,882 valores exactamente iguales, sin diferencias de visibilidad|
| Gráfico 15s END 19:20:45 frente a gráfico 1m END 19:20:00 |66|Mismo C, niveles distintos; se reproducen al usar low de vela 1m como semilla|
| Gráfico 15s END 19:21:45 frente a gráfico 1m END 19:21:00 |66|Control predeclarado confirmado; mismo C y reconstrucción con low de vela 1m|

Para estos casos, los datos respaldan dos dependencias de Lite respecto al gráfico: el límite efectivo incluye la última subvela 15s de la vela del gráfico que contiene END, y la semilla alcista usa el mínimo de esa vela del gráfico completa. No basta con seleccionar la misma fuente y escribir la misma hora de END para obtener las mismas curvas.

## Primer contraste: coincidencia directa

END exacto 19:20:15 se fijó arrastrando el ancla una vela en gráfico 15s. La captura `manual/Lite_END_192015_ancla.png` muestra los segundos exactos; los campos de ajustes solo admiten minutos. Dos CSV repiten 37,992 valores Lite cerrados sin diferencias. Las seis estimaciones independientes de C dan 79, con RMSE máximo 1.75e-12 en 6310 transiciones por curva.

Al comparar con el gráfico 30s se alinea su timestamp T con la subvela nativa T+15s. Las seis curvas coinciden exactamente en 3147 muestras por curva y su visibilidad coincide. La primera publicación nativa es 19:20:45; el CSV 30s la etiqueta 19:20:30 porque ese es el inicio de la vela agregada. Las dos semillas son 30864.50, por eso no es necesaria una corrección de niveles.

## Segundo contraste: separar C de la semilla

END nativo exacto 19:20:45 da C66 en las seis curvas, con RMSE máximo 2.29e-12. Las parejas repiten 37,854 valores Lite cerrados. Contra el gráfico 1m alineado en T+45s, el C coincide pero el error de niveles llega a 2.42306583 puntos.

El low de la subvela END 19:20:45 es 30868.00; el low de toda la vela 19:20 de un minuto es 30864.50. La diferencia de semillas es 3.50 puntos. Retroproyectar el residuo con los seis períodos da esa diferencia por separado en cada curva. Esa observación originó la hipótesis de semilla y se registró antes de reconstruir la serie completa.

Reconstrucción: semilla 30864.50, C66 suministrado, períodos no redondeados 72/89 divididos por 3/9/27 y normalizados a 15s, actualizaciones con cada cierre nativo posterior a END 19:20:45. Se comparan las muestras de última subvela de cada minuto. Reproduce 9396 valores (1566 por curva), error máximo 7.64e-11. El primer cierre fuera del rango inclusivo es 19:26:45, alcista; la visibilidad reconstruida coincide en todas las muestras posteriores a END.

## Tercer contraste: predicción en otro minuto

Antes de medir se registró gráfico 1m END19:21:00 -> C66, y gráfico 15s END19:21:45 -> C66. Se confirmó tanto ajustando las seis curvas nativas como ajustando cuatro actualizaciones 15s entre muestras agregadas. Los pares de CSV repiten 9504 valores del gráfico 1m y 37,890 del gráfico 15s exactamente.

La semilla del minuto completo es 30866.50, frente a low nativo END21:45 de 30866.75. La comparación directa tiene diferencias de hasta 0.18401547 puntos. Usando la semilla del minuto completo, la reconstrucción reproduce 9474 valores (1579 por curva), error máximo 7.64e-11. La primera ruptura vuelve a ser 19:26:45 y la visibilidad posterior a END coincide.

## Alcance

Esto explica las diferencias Lite observadas en tres contrastes de la misma sesión, dos minutos adyacentes y solo dirección alcista. No demuestra el tratamiento de START en una subvela intermedia, dirección bajista, otras fuentes, datos faltantes ni una regla universal. C sigue suministrado o recuperado de curvas originales: **no se ha obtenido el generador general de C a partir de OHLC**.

Las discrepancias de Character entre intervalos siguen pendientes; este resultado no las explica ni demuestra equivalencia entre generadores Lite y Character. Las mediciones anteriores con fuente igual al intervalo del gráfico siguen siendo controles válidos.

## Reproducción y continuación

Script `analizar_Lite_END_efectivo.py`, salida `Lite_END_efectivo.json`. CSV y capturas en `manual/Lite_END_192015_*`, `manual/Lite_END_192045_*`, `manual/Lite_minuto21_chart60_*` y `manual/Lite_minuto21_END45_*`. Se excluye la última fila de cada CSV. El script conserva las comparaciones directas fallidas y las reconstrucciones con semillas distintas.

Layout restaurado y guardado: gráfico1m, Lite fuente1m, Character fuenteChart, anclas12oct18:55–19:20, Replay apagado. Captura `manual/Lite_END_efectivo_restaurado.png`.

Siguiente contraste útil: mantener fuente y gráfico iguales para buscar el generador de C; usar ventanas con límites de minuto completos cuando se comparen intervalos diferentes. Comprobar primero START en subvela intermedia y un rango bajista para saber si también requieren normalización. No mezclar C de ambos indicadores sin verificar límites efectivos.
