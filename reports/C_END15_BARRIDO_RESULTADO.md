# Barrido de END a resolución fija de 15 segundos

START 12 de octubre de 2026 18:52:00 UTC. NQ1!, gráfico y fuente de 15 segundos. PS EMA LITE v1.2. Protocolo registrado antes de medir en C_END15_BARRIDO_PREREGISTRO.json.

| END UTC | Velas incluidas | C | Cambio de C |
|---|---:|---:|---:|
| 19:16:45 | 100 | 66 | — |
| 19:17:00 | 101 | 66 | 0 |
| 19:17:15 | 102 | 67 | +1 |
| 19:17:30 | 103 | 67 | 0 |
| 19:17:45 | 104 | 106 | +39 |
| 19:18:00 | 105 | 67 | −39 |
| 19:18:15 | 106 | 106 | +39 |
| 19:18:30 | 107 | 64 | −42 |
| 19:18:45 | 108 | 152 | +88 |

## Verificación

Las nueve posiciones tienen dos exportaciones concordantes, sin incidencias. Se recuperó C independientemente de cada una de las seis curvas y se reconstruyó su actualización desde el extremo de la vela END durante la hora posterior. Se verificó la presencia de todas las velas nativas y la visibilidad desde la primera ruptura posterior. Los tres controles previos (66, 106 y 152) se reprodujeron.

El precio y volumen de las nuevas exportaciones coinciden exactamente con la referencia nativa de 15 segundos en todo el ámbito comprobado. En las nueve cajas H=30864.50 y L=30844.25; la primera ruptura alcista posterior ocurre en la misma vela de 19:19:30 UTC. La semilla del cálculo cambia entre END porque corresponde al mínimo de su subvela; la reconstrucción incorpora ese cambio y aun así confirma los cambios de C. Por tanto, los saltos no son únicamente diferencias de posición vertical entre las curvas.

Se restauraron gráfico y fuente de un minuto, START18:55 y END19:20, y se verificó nuevamente C=62 y concordancia de las curvas con la referencia reciente. Captura final: manual/C_END15_regreso_final.png.

## Interpretación

La secuencia 67→106→67→106 localiza cambios reversibles al incorporar subvelas individuales a una ventana de origen fijo. No es una evolución monotónica con duración creciente. En particular, una regla monotónica de duración con H/L constantes no puede explicar este barrido por sí sola. El escalón +1 y los saltos +39, −42 y +88 tampoco pertenecen todos a una cuadrícula de desplazamientos de 9 o de 27 como la propuesta inicialmente.

Estos resultados no demuestran una selección armónica. Una cuantización más general, una transformación de características del camino de precios, una selección de régimen o una regla de índices siguen siendo hipótesis. N crece con el barrido y cambian simultáneamente la vela final, la historia incluida y el trayecto posterior hasta la ruptura. No atribuimos causalidad exclusiva al cierre, volumen, color o fase temporal.

La siguiente comparación debe centrarse en las transiciones observadas 19:17:30→19:17:45→19:18:00→19:18:15. Se pueden contrastar numéricamente sus caminos normalizados y características de EMA a fuente fija, preservando estas etiquetas de C. Los periodos de referencia serán proxies declarados, no longitudes del código protegido. Cualquier regla candidata deberá explicar también 19:18:30=64 y 19:18:45=152 y luego predecir un caso nuevo antes de medirlo. No basta encajar la alternancia 67/106.

Resultados, ajustes de las seis curvas y hashes: C_END15_barrido_resultados.json. Auditor reproducible: auditar_C_END15_barrido.py. Exportaciones preservadas: manual/C_estructura15_barrido_*.
