# C: primeras muestras observables en replay

13 de octubre de 2026. Primer control después de la auditoría de supuestos. NQ1!, ETH, UTC, BADJ apagado. START 12 octubre18:55 y END19:20. Gráfico1m; Character v6.5.36 perfilB Manual fuenteChart; Lite v1.2 fuente explícita1m. Las anclas no se modifican. Histórico de referencia: manual/Lite_1855_1920_1m_b.csv, C62.

Se solicitaron cortes19:25,19:29,19:33 y19:40. El último timestamp exportado es el minuto anterior al corte. Su estado de curvas repite el del minuto previo del histórico, por lo que se excluye la última fila. Todas las velas del rango seleccionado están presentes. En los timestamps comparables incluidos no hay discrepancias OHLC respecto al histórico.

| Corte | Última apertura incluida tras excluir fila final | Pares consecutivos por curva Lite | C recuperado Lite | Valores no vacíos Lite+Character idénticos al histórico |
|---|---|---:|---:|---:|
| 19:25 | 19:23 | 0 | No observable | 0 |
| 19:29 | 19:27 | 1 | 62 | 32 |
| 19:33 | 19:31 | 5 | 62 | 96 |
| 19:40 | 19:38 | 12 | 62 | 208 |

La primera muestra publicada histórica es19:26, al primer cierre exterior al rango. Las dos muestras19:26/19:27 permiten inferir la recurrencia mediante un par por cada curva. Los seis C recuperados en el corte19:29 están entre61.999999999863 y62.000000000316. Con un solo par, el residuo de ajuste cero es tautológico y no valida la hipótesis: la corroboración proviene del acuerdo entre las seis curvas, repetición de exportaciones y coincidencia exacta de niveles con el histórico. Los cortes posteriores aportan más pares y conservan C62.

## Recálculo y archivos rechazados

Después de seleccionar un corte nuevo, la primera exportación no siempre ha terminado el recálculo de Character. Las parejas iniciales a/b de19:29,19:33,19:40 tenían respectivamente20,60,130 celdas de curvas Character diferentes en los timestamps cerrados comunes: campos vacíos en la primera y curvas en la segunda. No se interpretan como repintado. Se conservan como diagnóstico y se rechazan para validar estabilidad.

Se obtuvieron parejas c/d tras el recálculo para esos tres cortes. Las16 curvas (6 Lite y10 Character) coinciden exactamente en todos los timestamps cerrados comunes de cada pareja. Para19:25 se admite a/b, que repetía campos vacíos. Los archivos terminados_pendiente se conservan solo como diagnóstico. No se sobrescribieron exportaciones anteriores.

## Alcance del resultado

En este rango C62 se puede observar con las primeras dos muestras publicadas y esas muestras no cambian en los otros cortes comprobados ni respecto al histórico completo. No es necesario esperar hasta19:33 para obtener la estimación de Lite, aunque el extractor estricto de Character necesita cinco pares.

No se observó C antes de la ruptura y no se asigna C=0 a ese estado. Sigue sin excluirse que el generador utilice datos entre END19:20 y la ruptura19:26, ni se identifica su fuente interna. Seleccionar cortes independientes no comprueba todavía si avanzar secuencialmente desde antes de END conserva el mismo estado. Tampoco prueba ausencia universal de repintado, filtración por series internas ni causalidad del generador.

Próximos controles: repetir arranque frente a avance secuencial para el mismo rango; ampliar a los casos C118/C67 de15s y uno bajista. Después separar intervalo visible de fuente y estudiar ventanas mínimas fuera de saturación, según C_AUDITORIA_DE_SUPUESTOS.md.

Script: analizar_C_observabilidad.py. Resultado: C_observabilidad.json. CSV: manual/C_observabilidad_HHMM_[a/b/c/d].csv. Capturas: C_observabilidad_1929.jpg, C_observabilidad_1933.jpg. Al finalizar se salió de replay, manteniendo fuente/gráfico1m y START18:55–END19:20; C_observabilidad_referencia_final.jpg.
