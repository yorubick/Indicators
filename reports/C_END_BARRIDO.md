# Barrido de END en pasos de 15 segundos

13 octubre 2026. Cinco mediciones nuevas de NQ1!, Character Tree v6.5.36, perfil B, Manual, gráfico 15s y fuente Chart. START fijo: 12 octubre 18:55:00 UTC. Replay apagado. Se cambiaron anclas mediante arrastre en gráfico 15s; las capturas muestran END exacto. El precio visual de Point2 cambió al arrastrar, parámetro descrito como ignorado en Manual y previamente controlado.

| END UTC | C entero compatible | Low de END | Close de END | Recorrido acumulado de cierres |
|---|---:|---:|---:|---:|
| 19:21:00 | 115 | 30868.75 | 30869.25 | 167.50 |
| 19:21:15 | 106 | 30868.50 | 30869.25 | 167.50 |
| 19:21:30 | 79 | 30866.50 | 30867.00 | 169.75 |
| 19:21:45 | 66 | 30866.75 | 30868.50 | 171.25 |
| 19:22:00 | 106 | 30866.75 | 30867.50 | 172.25 |

Cada selección tiene dos CSV aceptados `_a` / `_b` en `manual/C_END_*.csv`. El análisis recupera C de las diez curvas, comprueba períodos repetidos iguales y compara entre 54,540 y 54,600 celdas de plots comunes cerrados por pareja, excluyendo filas finales. Las ventanas OHLC están completas y cada siguiente ventana es exactamente la anterior más una vela. Los controles 19:21 y 19:22 reproducen C115 y C106 de la tanda anterior.

## Qué descarta este control

El máximo global permanece en 30870.50 y el mínimo en 30846.00 en los cinco rangos. Ninguna vela añadida crea un extremo global nuevo. Por tanto, **C puede cambiar sin cambiar los extremos globales**.

La vela 19:21:15 cierra exactamente donde cerró 19:21:00, tiene cuerpo cero y no añade distancia al recorrido acumulado de cierres. Sin embargo, C pasa de 115 a 106. Esto descarta que C sea función exclusivamente del cierre final, extremos globales y suma de cambios absolutos de cierres. No descarta una regla basada en cierre que también use conteo, duración, promedio, actualización recursiva o tratamiento de repeticiones.

19:21:45 y 19:22 tienen el mismo low de END y extremos globales, pero C pasa de 66 a 106. El low de END más los extremos globales tampoco basta. Una regla de selección de semilla para publicar EMAs no equivale a una regla generadora de C.

Hay cambios de C tanto con reversión de cierres como sin ella: 19:21:15 repite cierre; 19:21:30 continúa bajando; las dos últimas velas revierten. El simple evento de reversión no es requisito para cambiar C ni identifica su valor.

## Límites y continuación

Se midieron tres valores intermedios nuevos y se reprodujeron dos controles, todos en ventanas superpuestas de una jornada. La coincidencia de ciertas secuencias de C con otras ventanas no demuestra una regla periódica. No se modificaron precios y no se leyó código protegido. La fórmula de C sigue desconocida.

El siguiente contraste útil es evaluar algoritmos que procesen cada vela —incluidas velas de cierre repetido— y usen un criterio final; comprobar también cómo varía el cálculo al añadir velas sin nuevos extremos en otra zona. Antes de ampliar búsquedas masivas, conviene probar si el mismo conteo y los mismos precios finales pueden producir distintos C.

Script reproducible: `analizar_C_END_barrido.py`; resultados: `C_END_barrido.json`; anclas: `manual/C_END_*_ancla.jpg`.
