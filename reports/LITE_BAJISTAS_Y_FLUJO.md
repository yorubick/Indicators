# Lite: controles bajistas y reconstrucción de curvas

13 de octubre de 2026. NQ1!, ETH, UTC, BADJ apagado. Character Tree v6.5.36 perfil B Manual fuente Chart; Lite v1.2 fuente explícita de 1 minuto, igual al gráfico. Anclas del 12 de octubre.

| START | END | C Lite | C entero compatible Character |
|---|---|---:|---:|
| 04:45 | 05:15 | 116 | 116 |
| 04:45 | 05:25 | 113 | 113 |
| 04:45 | 05:30 | 110 | 110 |

Dos exportaciones por control repiten exactamente los plots Lite cerrados comunes. Se ajustaron 2,184 pares por curva; las seis EMA(close) recuperan C con discrepancia inferior a 1e-9 segundos y RMSE inferior a 2.5e-12. Estos tres controles llevan a catorce configuraciones concordantes de Lite/Character, en dos episodios de la misma jornada. No son catorce episodios independientes.

## Reconstrucción de Lite con C suministrado

El nuevo script verificar_flujo_Lite.py toma el C medio de las seis curvas medido por comparar_Lite_Character.py. No estima C desde el OHLC. Usa períodos sin redondear: 72*C/(divisor*resolución), 89*C/(divisor*resolución), divisores 3,9,27.

Para cada rango con OHLC completo calcula su máximo/mínimo global y el primer cierre posterior estrictamente fuera de esos extremos. Si rompe por arriba, toma el mínimo de la vela END como semilla; si rompe por abajo, el máximo de END. Actualiza EMA(close) desde la primera vela posterior a END, incluso antes de que el plot se publique. Exige publicación de las seis curvas desde el primer cierre exterior.

Es una comprobación retrospectiva: el script selecciona la rama conociendo la ruptura histórica. No afirma haber implementado aquí un selector causal en tiempo real, ni reproduce señales de entrada/salida, alertas o flips posteriores.

Se comprobaron 12 rangos completos (9 alcistas y 3 bajistas) durante 90 minutos después de END. Resultado: 16,926 valores, error máximo 1.92813e-10 puntos, cero incumplimientos de visibilidad. Las tres muestras bajistas comienzan en el cierre de las 05:36 UTC, y usan respectivamente semillas 31,250.50 / 31,248.75 / 31,245.50.

Dos CSV iniciales de los controles de START 18:54:00 y 18:55:00 en 15s carecen de OHLC del rango seleccionado: sirven para ajustar sus recurrencias posteriores y comparar C, pero se excluyeron de la reconstrucción de semilla/publicación. Esa exclusión se registra explícitamente y no cuenta como validación.

## Alcance para la búsqueda de C

Quedan verificadas las reglas de EMA, semilla y primera publicación de Lite en estas muestras, con C medido suministrado. Esto separa la reconstrucción de las curvas del problema pendiente: el generador OHLC de C. El acuerdo de catorce configuraciones sugiere un núcleo relacionado, sin probar equivalencia universal. No se encontraron C fraccionarios en estas muestras; no se afirma que no existan.

## Archivos

CSV manual/Lite_0445_051500_1m_a.csv y _b.csv, equivalentes 052500 y 053000. JSON por control Lite_0445_HHMMSS_1m_comparacion.json. Ejemplo de ejecución: comparar_Lite_Character.py "04:45:00" 60 "05:30:00".

Script de reconstrucción: verificar_flujo_Lite.py. Resultado detallado: Lite_flujo_verificacion.json. Captura: Lite_bajista_0445_0530.jpg. Referencia restaurada y guardada: START 18:55, END 19:20, fuente/gráfico 1m.
