# Segunda ventana: C62 conserva las tres simetrías

14 octubre 2026. Prueba real en copia TradingView xqM5dZIf, Lite cargado v1.2, fuente/gráfico 1 minuto. START 12 octubre 18:55 UTC, END19:20 UTC (26 velas). Protocolo previo en C_SIMETRIA_1855_PREREGISTRO.json. Character excluido.

| Condición | C de seis recurrencias |
|---|---:|
| Referencia NQ1! | 62 |
| 2*NQ1! | 62 |
| NQ1!+10000 | 62 |
| 70000−NQ1! | 62 |
| Regreso NQ1! | 62 |

Cada fórmula sintética permaneció visible en el diálogo de exportación. Sobre 2.725 velas cerradas comunes con referencia fresca, las cuatro columnas OHLC satisfacen exactamente cada transformación, intercambiando H/L en la reflexión; volumen idéntico en todas. Todas las curvas mantienen la visibilidad y corresponden a la transformación de la misma curva original: duplicación exacta, traslación y reflexión con error máximo menor que 6×10⁻¹¹ puntos. Dos exportaciones por transformación coinciden. El regreso reproduce exactamente la referencia.

Se comprobaron los 26 timestamps de la ventana y una hora posterior. La última fila de cada CSV se excluye. Seis ajustes EMA independientes por exportación entregan C62 con dispersión menor que 10⁻⁶ y RMSE inferior a 5×10⁻¹². No se exigió C62 como criterio de aceptación de la medición transformada.

La simetría observada en C50 se reproduce en una segunda ventana con C62. Es una réplica sobre rangos solapados del mismo día y mercado; no demuestra invariancia universal ni independencia de todo contexto oculto. Las transformaciones actúan sobre todo el historial disponible, y no se observan metadatos ni solicitudes internas del script. Sigue siendo compatible tanto con un mecanismo temporal como con geometría normalizada y simétrica. No identifica un generador armónico.

Siguiente prueba propuesta: barrer START en pasos de un minuto con END19:20 fijo sobre datos nativos. Declarar antes las ventanas, medir C sin ajustar una fórmula después de cada punto, registrar n, extremos y ruptura; comparar especialmente ventanas que conservan H/L y primera ruptura. Esto puede localizar saltos temporales y evaluar anclas anteriores. Que H/L y ruptura coincidan no conserva toda la geometría ni demuestra por sí solo dependencia exclusiva del tiempo.

Auditoría: analizar_C_simetria1855.py y C_simetria1855_resultados.json incluyen ajustes, cobertura, todas las comparaciones y hashes SHA256. Exportaciones/capturas en manual/C_simetria1855_*. Gráfico guardado en NQ1!,1m, rango18:55–19:20; layout principal sin cambios.
