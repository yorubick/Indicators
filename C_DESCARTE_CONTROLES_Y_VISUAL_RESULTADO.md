# Descarte extendido y comparación real62/83

14octubre2026. Se terminaron dos trabajos: aplicar las medidas fijas a controles anteriores fuera de la matriz y repetir un par conocido en TradingView con comparación visual/numérica. No se entrenó predictor ni se ajustaron longitudes/umbrales.

## Controles fuera de matriz

El maestro histórico tiene72casos de1minuto,n>=21,Cmedido en Lite. De ellos13no tienen cobertura completa en el CSV ampliado y2pertenecen a la matriz; quedan57controles fuera de ella. Se verificó igualdad exacta de OHLCV con cada caso del maestro. Es una selección por cobertura,resolución y procedencia,no por etiqueta. Ventanas solapadas y etiquetas conocidas: no es validación ciega ni57observaciones estadísticamente independientes.

Se conservaron las fórmulas de geometría y los períodos24,89/3,8,89/9,72/27,89/27,72y89. Los57casos conservan signos,conteos de cruces y orden de EMAs en ambos bordes bajo el control de semilla±100puntos. Hay7grupos con firma discreta idéntica y Cdistinto tanto al usar6como8EMAs. Ejemplos con8:

-12octubre14:00–14:21/14:22/14:23: C62/83/76.
-12octubre19:00–19:21/19:22: C102/77.
-12octubre19:04–19:27/19:28: C71/128.
-13octubre06:25–06:48/06:49: C83/84.

Estos contraejemplos descartan las firmas discretas examinadas como determinantes únicos. No descartan longitudes diferentes,EMAs ancladas a otra vela,distancias/pendientes continuas ni todos los armónicos.

## Repetición en TradingView

Litev1.2 cargado,fuente/gráfico1m,NQ1!,día12octubreUTC,copiaxqM5dZIf. Protocolos previos C_GEOMETRIA_EMA_CONTROLES_PROTOCOLO.json y C_COMPARACION_VISUAL_1400_PROTOCOLO.json.

| Medida |14:00–14:21|14:00–14:22|
|---|---:|---:|
|C,inferido de6curvas|62|83|
|Velas incluidas|22|23|
|H|30974.50|30974.50|
|L|30867.25|30867.25|
|CloseEND normalizado|(0.254079)|0.254079|
|Eficiencia|0.280156|0.280156|
|Primera ruptura bajistaUTC|14:26|14:26|
|Distancia ENDclose−EMA24 / altura|−0.244723|−0.225145|
|Distancia ENDclose−EMA89 / altura|−0.794705|−0.777045|

La vela añadida cierra al mismo precio que la anterior; conserva variación total de cierres,closeinicial/final y eficiencia. Pero altera conteo,OHLCdeEND,tiempo,otra actualización EMA y posiblemente el estado interno. C62/83 con igual eficiencia descarta toda conversión basada exclusivamente en esa eficiencia,incluso no lineal; no identifica cuál de las otras variables causa el cambio.

DosCSVporcada configuración concuerdan en curvas/OHLCV. Los datos nativos coinciden con la fuente ampliada. Rangos completos y una hora posterior,última fila excluida. C62y83 se reconstruyen independientemente de las seis recurrencias conRMSE<10⁻⁸ y concordancia<10⁻⁶. La firma de8EMAsproxies coincide según el análisis histórico,con sensibilidad de semilla comprobada. Regreso a18:55–19:20 reproduce referencia y C62. Character no se utilizó ni actualizó.

## Lectura visual

Capturas reales C_visual1400_1421.png yC_visual1400_1422.png muestran las curvas de salida de Lite tras cada rango,con la misma vista temporal. Su diferencia es efecto de C ydeEND; no demuestra la variable previa que selecciona C.

Se generó C_comparacion1400_normalizada.svg con ReportLab:panelAcloseyEMAsfijas históricas;panelBsalidasLiteAde3capas,continuoC62/discontinuoC83,en escala común(P−L)/(H−L). Datos ySVGXML comprobados;no se verificó visualmente elSVG en el visor disponible. La comparación visual confirmada es la de las capturas de TradingView.

## Estado del trabajo

Este descarte concreto queda terminado. No hay fórmula ni predicción nueva validada. Distancias,pendientes,distribución temporal de la forma y posibles anclas siguen abiertas. La propuesta de Gemini es útil si las superposiciones visuales se acompañan de mediciones y si se separan EMAsde referencia de curvas de salida. Reconocer una forma semejante no basta para concluir queCproviene de alineación armónica.

Artefactos reproducibles:evaluar_C_geometria_controles.py,C_geometria_controles_resultados.json,auditar_C_visual1400.py,C_visual1400_resultados.json,incluyendo procedencia,hashes,exclusiones y comparación de regreso. Gráfico restaurado y guardado18:55–19:20,NQ1!,1m,vista19:10. Layoutprincipal sin cambios.
