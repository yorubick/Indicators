# Traslación P + 10000: C permanece en 50

Prueba real del 14 octubre 2026, en la copia xqM5dZIf. Lite v1.2 sin actualizar, fuente y gráfico 1 minuto. START 12 octubre 19:02 UTC, END 19:22 UTC; 21 velas. Predicciones y controles declarados antes de aplicar la transformación en C_TRASLACION_50_PREREGISTRO.json. Character no se utiliza.

| Condición | H | L | C de las seis curvas |
|---|---:|---:|---:|
| Original | 30870.75 | 30849.00 | 50 |
| CME_MINI:NQ1!+10000 | 40870.75 | 40849.00 | 50 |
| Regreso original | 30870.75 | 30849.00 | 50 |

La expresión sintética quedó visible en el título y diálogo de exportación. En 2.717 velas cerradas comunes, las cuatro columnas OHLC son exactamente originales +10000 y el volumen es idéntico. Las seis curvas presentan la misma visibilidad y equivalen a originales +10000 con error máximo 2.92×10⁻¹¹ puntos, dentro de precisión numérica. Dos exportaciones de la traslación coinciden; el regreso reproduce exactamente la referencia. La referencia fresca reproduce además la anterior prueba de escala en 2.710 velas comunes. Se descarta la última fila de cada CSV.

Las seis recurrencias EMA ajustadas independientemente entregan C=50 con error menor de 10⁻⁶ y RMSE menor de 4×10⁻¹². Se comprueban los 21 timestamps y una hora posterior a END. El script analizar_C_traslacion50.py reproduce la auditoría y genera C_traslacion50_resultados.json con ajustes, comparaciones y hashes SHA256.

Conclusión limitada: en esta ventana, C conserva su valor al duplicar los precios y al sumar 10000. Esto respalda buscar relaciones normalizadas o estructura temporal. La prueba de traslación no separa Gemini v4 de la invariancia, pues ambos predijeron 50; la predicción v4 que falló fue la duplicación 50→77. No demuestra armonía ni invariancia universal. Metadatos y solicitudes internas no son totalmente observables y la transformación afecta todo el historial disponible.

Próximo contraste propuesto: reflexión P'=70000−P en el mismo rango. Conserva distancias absolutas y timestamps, pero invierte direcciones y posiciones relativas. Verificar O'=70000−O, C'=70000−C, H'=70000−L, L'=70000−H y volumen. Declarar previamente qué canales deberían corresponder y no exigir un resultado C=50 para aceptar la medición. Si C cambia, estudiar sensibilidad direccional; si conserva 50, buscar medidas simétricas y anclas temporales. El resultado seguiría limitado a esta ventana y al contexto sintético.

El gráfico se dejó guardado en NQ1!, 1 minuto y el rango de referencia. Capturas y CSV en manual/C_traslacion50_*. Layout principal sin modificar.
