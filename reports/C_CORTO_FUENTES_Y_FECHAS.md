# Relación corta de C: contraste entre fuentes y fechas

13 de octubre de2026. Nuevas mediciones con predicciones prefijadas en C_DECIMALES_PREDICCIONES.md. NQ1!, ETH, UTC, BADJ apagado, Character v6.5.36 perfilB Manual fuenteChart. Fuente explícita Lite v1.2 igual al gráfico.

## Hipótesis y resultados

Se contrasta C=max(Δ,n*Δ*10/183), con n igual al número inclusivo de velas y Δ a la fuente en segundos. Es la normalización de la pendiente200/61 identificada en fuente60s. No se presupone continuidad de esa relación para21 velas.

| Fecha UTC | START–END | Δ | n | C previsto por relación | C medido |
|---|---|---:|---:|---:|---:|
| 12 octubre | 19:00–19:04:30 | 15 | 19 | 15.57377049 | 15.57377049 |
| 12 octubre | 19:00–19:04:45 | 15 | 20 | 16.39344262 | 16.39344262 |
| 12 octubre | 19:00–19:05:00 | 15 | 21 | 17.21311475 | 16 |
| 13 octubre | 19:00–19:18 | 60 | 19 | 62.29508197 | 62.29508197 |
| 13 octubre | 19:00–19:19 | 60 | 20 | 65.57377049 | 65.57377049 |
| 13 octubre | 19:00–19:20 | 60 | 21 | 68.85245902 | 81 |

Las cuatro predicciones nuevas de19/20 velas coinciden con error menor a1e-7 segundos. La continuación proporcional falla en21 velas, como ocurrió en los episodios anteriores de1m con C75/77. Para el nuevo control de21 en1m no se predijo81: se trata de medición diagnóstica de la frontera.

## Interpretación

La regla corta se reproduce en dos fuentes y dos fechas y es compatible con conteo y resolución como entradas de esa parte del cálculo. Los datos apoyan explorar una rama de respaldo para menos de21 velas, que cambia al disponer de más historial. No se demostró una condición universal n<21 ni el motivo del factor10/183; tampoco se identificó el generador de la rama que produce16/75/77/81.

Los cambios se comparan por número de velas fuente, no por un mismo recorrido OHLC reagrupado. Cambiar resolución modifica precios agregados y cobertura: esta tanda contrasta la normalización de la relación corta, sin afirmar que se aisló un cambio de resolución sobre datos idénticos.

## Verificación y recálculo

Se verifica cobertura completa de los OHLC seleccionados, igualdad exacta de las16 curvas en cada pareja cerrada aceptada, acuerdo de las seis estimaciones Lite y pertenencia de C Lite al intervalo Character. Los seis controles pasan esas condiciones.

En la jornada13, las primeras exportaciones podían repetir datos obsoletos de Character incluso cuando a/b era idéntica. Por ejemplo, el corte de20 velas mantenía períodos de19 velas, y el de21 mantenía los de20. Se inspeccionaron las anclas, se dejó completar el recálculo mientras se verificaban datos, y se obtuvieron parejas c/d de cada estado. Con c/d los intervalos de Character coinciden con Lite. Los a/b se conservan como diagnóstico y no se aceptan como prueba de diferencia entre productos. Dos exportaciones iguales por sí solas no garantizan que el último cambio de inputs ya esté aplicado.

Los END subminuto se colocaron por arrastre en gráfico15s y se verificaron mediante etiquetas de ancla con segundos completos. Se guardaron capturas de ambos indicadores en manual/C_corto15s_*_ancla.jpg. Las anclas de la jornada13 se verificaron en diálogo con ambas fechas13 de octubre y fuente1m.

## Archivos

comparar_Lite_Character.py ahora acepta una fecha opcional y sufijos de pareja, conservando por defecto12 de octubre y a/b. Ejemplo: comparar_Lite_Character.py "19:00:00" 60 "19:19:00" "2026-10-13" "c,d". Los archivos de otra jornada llevan20261013 en el nombre para no sobrescribir selecciones anteriores.

Analizador: analizar_C_corto_fuentes.py. Datos y auditoría: C_corto_fuentes.json. CSV manual/Lite_190000_190430/190445/190500_15s_[a/b].csv y manual/Lite_20261013_1900_191800/191900/1920_1m_[c/d].csv. Captura C_corto_otrajornada_anclas.jpg.

Al finalizar se restauró12 de octubre START18:55–END19:20, fuente/gráfico1m y layout guardado. C_corto_fuentes_referencia_final.jpg.

Siguiente experimento: comprobar el umbral con fuentes adicionales y aislar cómo obtiene C a partir de21 velas. La relación corta no debe usarse como réplica general del indicador.
