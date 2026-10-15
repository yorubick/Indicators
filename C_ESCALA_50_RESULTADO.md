# Prueba de escala de precios: C permanece en 50

14 octubre 2026. Medición real en la copia TradingView xqM5dZIf, Lite cargado v1.2. START 12 octubre 19:02 UTC, END 19:22 UTC, fuente y gráfico de 1 minuto; 21 velas. Character actualizado por el usuario a v6.5.58 no se usa en esta medición.

| Condición | Rango H−L | C de las seis curvas |
|---|---:|---:|
| CME_MINI:NQ1! original | 21.75 | 50 |
| (CME_MINI:NQ1!+CME_MINI:NQ1!)/2 | 21.75 | 50 |
| 2*CME_MINI:NQ1! | 43.50 | 50 |
| Regreso a CME_MINI:NQ1! | 21.75 | 50 |

El primer control preregistrado NQ1!+0 fue normalizado al símbolo nativo por TradingView: no se aceptó como control sintético. Antes de medir su C se declaró la alternativa de dos términos en C_ESCALA_50_IDENTIDAD_ALTERNATIVA.json. Esta reparación es exploratoria y se conserva separada del preregistro original.

La alternativa mantuvo su fórmula visible en el diálogo de exportación. Reprodujo exactamente OHLC, volumen, visibilidad y valores de las seis curvas en 2.710 velas cerradas comunes, incluidos todos los timestamps del rango. La duplicación mantuvo asimismo la fórmula sintética visible y produjo OHLC y seis curvas exactamente iguales a dos veces los originales; el volumen permaneció idéntico. Dos exportaciones de la duplicación coinciden en 2.713 velas cerradas comunes. El regreso reprodujo la referencia en las 2.710 velas comunes. Se descarta la última fila de cada CSV para evitar la vela abierta.

Se reconstruye C por la recurrencia EMA sobre cierres de 1 minuto, sin etiquetas de Gemini: seis ajustes independientes dan 50 con dispersión menor que 10⁻⁶ y RMSE máximo inferior a 5×10⁻¹². La ventana completa y la hora posterior a END están presentes. El control de cobertura usa una hora para evitar la pausa diaria de mercado a las 21:00 UTC.

La predicción publicada antes de la medición por el evaluador congelado de Gemini v4 era 50→77 al duplicar OHLC; falla en este control. El resultado respalda invariancia de C ante duplicación en esta ventana. No demuestra una fórmula armónica ni identifica qué parte del historial alimenta C. Metadatos y solicitudes internas del script no son totalmente observables; las conclusiones se limitan a las series OHLCV y a la recurrencia de Lite comprobadas. La transformación afecta también el historial previo y las velas posteriores al rango.

Siguiente prueba propuesta: traslación P→P+10000 con control de igualdad OHLCV y curvas trasladadas. Conserva alturas y diferencias, pero cambia niveles y porcentajes. Si C se conserva, conviene probar variables de geometría normalizada y anclas temporales; si cambia, estudiar dependencia del nivel de precio o metadatos antes de concluir.

Datos y auditoría: C_escala50_resultados.json incluye hashes SHA256, seis ajustes y comparaciones completas. Ejecutar analizar_C_escala50.py vuelve a verificarlos. CSV y capturas están en manual/C_escala50_*. El gráfico se dejó guardado en NQ1!, 1 minuto y el rango original de la prueba. El layout principal uXfdB8FS no se modificó.
