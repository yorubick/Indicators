# Predicción de Gemini v4 para una transformación de precio

14 octubre 2026. Segunda lectura del informe y del código, usando la copia congelada Gemini_v4_evaluador_recibido.py. Solo se extrajo y ejecutó la función predict_C inspeccionada, con math de la biblioteca estándar; no se ejecutó el evaluador externo completo.

Caso: 12 octubre 2026, START19:02:00 y END19:22:00 UTC, gráfico/fuente1m, 21velas. OHLC de Gemini_v4_cases112_recibidos.json. Rango21.75puntos; C original previamente verificado aproximadamente50.

| Transformación de todos los OHLC | Predicción v4 | Rama |
|---|---:|---|
|P|50|CONSOLIDATION_M24|
|P+10000|50|CONSOLIDATION_M24|
|2P|77|MACRO_BASE_77|
|0.5P|50|CONSOLIDATION_M24|

Estas son predicciones del código sobre entradas transformadas localmente, no mediciones del indicador original en TradingView. La etiqueta C del caso original no se usa para predecir los casos transformados.

La duplicación conserva tiempos, conteo, posición relativa inicial/final, direcciones y orden de precios, pero cambia la altura21.75→43.5 y atraviesa los umbrales en puntos de v4. Así v4 proporciona una predicción diferenciadora50→77. Una hipótesis de invariancia de C bajo escalamiento positivo predice50→50.

El contraste requiere primero los controles de compatibilidad de C_PROTOCOLO_TRANSFORMACIONES_PRECIO.md: aceptar símbolo sintético, igualdad de datos P'=2P, volumen disponible/conservado o limitación documentada, metadatos y recurrencia de las curvas, exportaciones estables y referencia de identidad. Si no se conservan las otras entradas relevantes, el resultado no aísla la escala de precio.

Si el original conserva50 con datos/compatibilidad aceptados, contradice la predicción v4 en ese control. Si entrega77, respalda esa predicción individual y merece otra réplica; no demuestra que los umbrales internos o la fórmula completa sean los de Gemini. Otro valor contradice ambos candidatos concretos.

No se realizaron mediciones nuevas ni se cambió la configuración del gráfico durante esta evaluación. El experimento transforma también la prehistoria y el tramo posterior; no determina qué intervalo alimenta C.
