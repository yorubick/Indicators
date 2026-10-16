# Lite y Character: barrido de END en 15 segundos

13 de octubre de 2026. NQ1!, ETH, UTC, ajuste de contratos apagado. Gráfico de 15 segundos. Character Tree v6.5.36, perfil B, Manual, fuente Chart; EMA Origin Lite v1.2, fuente explícita de 15 segundos. START fijo: 2026-10-12 18:55:00.

| END UTC | C inferido de Lite | C entero compatible de Character |
|---|---:|---:|
| 19:21:00 | 115 | 115 |
| 19:21:15 | 106 | 106 |
| 19:21:30 | 79 | 79 |
| 19:21:45 | 66 | 66 |
| 19:22:00 | 106 | 106 |

Cada control tiene dos exportaciones. Las seis curvas Lite se repiten exactamente en los timestamps cerrados comunes. Ajustando EMA(close), sus períodos decimales recuperan el mismo C en las seis curvas, con discrepancia inferior a 1e-9 segundos y RMSE inferior a 2.3e-12. Hay entre 5,377 y 5,386 pares por curva. Character se vuelve a extraer del mismo CSV combinado y reproduce los cinco resultados del barrido anterior.

## Qué se establece

La secuencia no monótona 115→106→79→66→106 también aparece en Lite sin redondear períodos. No se debe al redondeo de períodos de Character. Los controles adicionales amplían la concordancia a once configuraciones: dos en 1m, cuatro de START en 15s y estas cinco de END, todas de la misma jornada. Todavía no se establece equivalencia universal de sus generadores.

Aunque los períodos Lite son decimales, los C recuperados en todos estos controles son enteros dentro de tolerancia numérica. Esto apoya investigar reglas que cuantizan C en segundos. No prueba que C sea entero en todos los casos ni determina cómo se obtiene.

El informe previo C_END_BARRIDO.md ya establece que en estas cinco ventanas el máximo y mínimo global no cambian y que el primer incremento conserva el cierre final y el recorrido absoluto de cierres. Esta nueva comparación reproduce sus valores de C; no vuelve a deducir esas propiedades a partir de los plots.

## Procedimiento y archivos

END inicial 19:21 se fijó en los ajustes de ambos indicadores. Con Go to a 2026-10-12 19:21 y gráfico 15s, se seleccionó cada indicador por su leyenda y se arrastró su handle END una vela por paso. Antes de exportar cada control se verificó la hora completa en la etiqueta azul del eje temporal. Se guardó captura de cada indicador, sin reabrir su diálogo de hora para los segundos intermedios. El precio de Point2 de Character varió con el magnetismo de velas, pero su modo Manual ignora ese precio.

CSV: manual/Lite_185500_192100_15s_a.csv y _b.csv, equivalentes 192115, 192130, 192145 y 192200. Capturas: manual/Lite_END_HHMMSS_ancla.jpg y Character_END_HHMMSS_ancla.jpg.

Script actualizado: comparar_Lite_Character.py START segundos_fuente END. Ejemplo: comparar_Lite_Character.py "18:55:00" 15 "19:21:45". Los valores omitidos conservan los controles anteriores: fuente 60 y END 19:20. JSON por control: Lite_185500_HHMMSS_15s_comparacion.json.

El generador de C desde OHLC sigue pendiente. La próxima búsqueda puede usar Lite para separar una regla continua de una regla con cuantización a segundos, sin la ambigüedad de los períodos enteros de Character. Antes de afirmar cuantización universal conviene incluir otras jornadas y rangos bajistas.
