# Fuente explícita 15s y cambio de intervalo del gráfico

13 octubre 2026. NQ1!, ETH, UTC, BADJ apagado, Replay apagado. Character Tree v6.5.36 perfil B Manual y PoiSzn EMA Origin Lite v1.2. Ambos con fuente **15 segundos explícita**, START12 octubre18:55:00 y END19:20:00. Se cambió únicamente el intervalo visible entre mediciones. Configuraciones documentadas en `manual/C_fuente15_Lite_config.png` y `manual/C_fuente15_Character_config.png`.

## Resultado principal

| Gráfico | Fuente | C Lite recuperado con cierres nativos15s | Character |
|---|---|---:|---|
| 15s, referencia |15s|106|C compatible106, diez períodos recuperados|
| 1m |15s|66|Mantiene períodos compatibles106 en diagnóstico inicial; niveles no idénticos|
| 15s, regreso |15s|106|C compatible106; mismas curvas de referencia|
| 30s, control dirigido |15s|79|Mantiene períodos compatibles106 en diagnóstico inicial; niveles no idénticos|

La prueba de invariancia completa de las16curvas **no pasa**. Esto revela que seleccionar fuente15s no basta para asumir comportamiento idéntico entre intervalos de gráfico, especialmente en Lite.

## Cómo se recuperó Lite con gráfico agregado

No se ajustó una EMA15s contra cierre1m. Cada transición de una muestra1m a la siguiente se reconstruyó con los cuatro cierres15s observados, en orden temporal, aplicando la familia de períodos no redondeados72/89. Se estimó C independientemente en cada una de las seis curvas. Con gráfico1m, las seis dan66: entre65.99999999998792 y66.00000000002831, 1549transiciones por curva, RMSE máximo6.08e-12. Con gráfico30s se reconstruyeron dos actualizaciones15s: las seis dan79,3128transiciones por curva, RMSE máximo3.10e-12. Un ajuste directo contra cierre agregado tiene residuos grandes y C incompatibles entre curvas; se conserva como diagnóstico fallido en JSON.

El control30s fue registrado antes de su medición en `C_DECIMALES_PREDICCIONES.md`: predicción Lite79, Characterperíodos106. La predicción numérica Lite pasa. Los datos son compatibles con que Lite incluya las subvelas hasta el final de la vela del gráfico que contiene END:19:20:00 en15s,19:20:15 en30s y19:20:45 en1m. **Esta interpretación es una hipótesis sobre el límite efectivo, no código recuperado ni regla general demostrada.** Aún puede haber otra dependencia del intervalo que produzca estos valores.

## Character: distinguir períodos de niveles

Períodos nativos de la referencia:170,210,57,70,19,23,509,629,1526,1887. Al predecir las muestras agregadas con esos períodos y los cierres15s, durante19:20–20:50 todas las curvas cumplen la recurrencia:88transiciones1m por curva, error máximo1.10e-11;178transiciones30s, máximo7.28e-12. Este subrango90min se definió **después** de observar discrepancias completas y se identifica como diagnóstico posterior; no sustituye el contraste completo.

Los niveles iniciales no coinciden exactamente con la muestra15s alineada: diferencia máxima0.18225 en el diagnóstico30s y0.149755 en1m. La visibilidad también difiere en1m. Además, el contraste de recurrencia sobre todo el CSV tiene errores máximos0.423825 en1m y0.389428 en30s. El origen de estas discrepancias tardías está pendiente de identificar; no se atribuye sin pruebas a sesiones, datos faltantes o fallback. Por tanto, no afirmar equivalencia completa de Character entre gráficos.

Al regresar a gráfico15s, las16curvas repiten exactamente100512valores comunes (6282por curva), cero discrepancias de visibilidad. Lite y Character recuperan106. Esto reduce la posibilidad de que el cambio observado fuera una modificación persistente de anclas.

## Evidencia y reproducción

CSV en `manual/`:

- `C_source15_chart15_antes_a/b.csv`: referencia.
- `C_source15_chart60_a/b.csv`: primera exportación, sin rango12oct completo; conservada pero no usada como pareja principal.
- `C_source15_chart60_c/d.csv`: pareja aceptada tras cargar explícitamente12oct19:40.
- `C_source15_chart15_regreso_a/b.csv`: regreso a referencia.
- `C_source15_chart30_a/b.csv`: predicción dirigida.

Cada pareja aceptada repite las16curvas comunes cerradas; última fila excluida. Script `analizar_C_fuente_vs_grafico.py`; salida `C_fuente_vs_grafico.json`. Ejecutar con Python desde esta carpeta. Se conservan resultados completos, ajustes exploratorios y diagnóstico90min separado.

Layout restaurado y guardado: gráfico1m, Litefuente1m, CharacterfuenteChart, START18:55 END19:20 del12oct, Replay apagado. Evidencia `manual/C_fuente_vs_grafico_restaurado.png`.

## Siguiente contraste

Medir directamente Lite con gráfico15s y END19:20:15/19:20:45; comparar tanto C como semilla, primera publicación y niveles completos contra las exportaciones30s/1m. Repetir el control en otro minuto con valores conocidos diferentes. Si coinciden, podremos normalizar límites efectivos antes de mezclar observaciones Lite y Character en la búsqueda del generador de C. Las mediciones anteriores con fuente igual a gráfico no quedan refutadas por este hallazgo.
