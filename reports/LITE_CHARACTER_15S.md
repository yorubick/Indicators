# Lite y Character: controles en fuente de 15 segundos

13 octubre 2026. NQ1!, ETH, UTC, BADJ apagado. Gráfico15s, Character Tree v6.5.36 perfil B Manual fuente Chart; Lite v1.2 fuente explícita15s. END fijo2026-10-12 19:20:00.

| START UTC | C recuperado de seis curvas Lite | C entero compatible de Character |
|---|---:|---:|
| 18:54:00 | 123 | 123 |
| 18:55:00 | 106 | 106 |
| 18:54:15 | 118 | 118 |
| 18:54:30 | 67 | 67 |

Cada control tiene dos exportaciones CSV. Los plots Lite cerrados comunes se compararon exactamente entre ambas. Se excluye la última fila del ajuste; se usan pares consecutivos separados15s. Las seis curvas cumplen EMA(close) con períodos decimales y RMSE inferior a2.4e-12. En los controles de segundos se ajustaron más de5380 pares por curva. Los C recuperados son enteros dentro de aproximadamente2e-10; no se observaron fracciones de C en estas muestras, aunque sí períodos fraccionarios.

El salto118→67 también está presente en los períodos sin redondear de Lite. Por tanto no es un artefacto del redondeo de períodos de Character. No se ha identificado el generador OHLC de C, ni demostrado equivalencia universal de los indicadores. Con los dos controles previos de1m hay seis configuraciones coincidentes de una misma jornada y rango END.

## Anclaje preciso

El campo de hora de Lite no preservó los segundos al introducir18:54:15: al perder foco mostró18:54. Se descartó ese intento como control de segundos y se midió18:54:00.

Para colocar los segundos se abrió Go to a2026-10-12 19:00 en gráfico15s. Al seleccionar el indicador por su leyenda apareció el handle azul de START. Se arrastró desde18:55 a18:54:15 y luego una vela a18:54:30, sin abrir ni aceptar su diálogo de hora después. Se confirmó cada hora completa en la etiqueta azul de ancla del eje temporal y se guardó captura por indicador. END se mantuvo19:20. Mover la altura del handle Character cambia el precio Point1, ignorado por su modo Manual; la comparación usa las horas.

## Reproducción

Datos enmanual/Lite_185400_1920_15s_a.csv y_b.csv, equivalentes185500,185415,185430. Evidencia enmanual/Lite_185415_15s_ancla.jpg yCharacter_185415_15s_ancla.jpg, y equivalentes185430.

Ejecutarcomparar_Lite_Character.py "18:54:15" 15 y "18:54:30" 15. El segundo argumento agrega soporte a resolución15s; sin argumento sigue usando60s y los archivos previos de1m. JSONpor control: Lite_HHMMSS_1920_15s_comparacion.json.

Siguiente control útil: aplicar Lite al barrido de END19:21:00/15/30/45 y19:22:00, donde Character ya produjo115/106/79/66/106, para comprobar la coincidencia también al cambiar el extremo final. La investigación de fórmulas continúa después de establecer ese alcance.
