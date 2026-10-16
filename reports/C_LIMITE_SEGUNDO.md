# Salto de C al excluir la primera vela

13 octubre 2026. NQ1!, Character Tree v6.5.36, perfil B, Manual. END fijo: 12 octubre 19:20:00 UTC. Fuente explícita: 15 segundos; las curvas se exportaron en gráfico de 15 segundos.

| START exacto UTC | Primera vela con apertura >= START | Velas hasta END inclusive | C entero compatible |
|---|---|---:|---:|
| 18:54:15 | 18:54:15 | 104 | 118 |
| 18:54:16 | 18:54:30 | 103 | 67 |
| 18:54:29 | 18:54:30 | 103 | 67 |
| 18:54:30 | 18:54:30 | 103 | 67 |

## Cómo se colocaron segundos exactos

El campo horario de configuración truncó el intento de escribir 18:54:16 a 18:54. Por ello se utilizó Replay y gráfico de un segundo para arrastrar el punto START a una vela exacta, manteniendo la fuente Manual fija en 15 segundos. Capturas de las anclas en `manual/C_limite_185416_ancla.jpg`, `C_limite_185429_ancla.jpg` y `C_limite_185430_ancla.jpg`.

Después se cargó Replay hasta 19:40 y se cambió el gráfico a 15 segundos. Al regresar a un segundo se comprobó que 18:54:16 y 18:54:29 seguían conservados: capturas terminadas en `_conservada.jpg`. En el gráfico grueso la etiqueta del control muestra la próxima vela de 15 segundos; esa etiqueta por sí sola no demuestra que el timestamp interno haya cambiado.

Durante los cambios de intervalo hubo cargas pendientes y reversiones a 1s. El CSV `C_limite_185430_pendiente_1s.csv` conserva un intento sin curvas y queda excluido. Las parejas `_a.csv` / `_b.csv` aceptadas contienen diez curvas EMA de cierre de período entero en 15 segundos. La fuente más gruesa sobre gráfico fino mostró RE10142, por lo que no se infirió C en gráfico 1s.

## Validación y alcance

`analizar_C_limite_segundo.py` recupera los períodos y el intervalo de C de cada pareja; compara 2,980 celdas de plots repetidos por caso, omitiendo filas finales abiertas. Verifica cobertura OHLC completa del conjunto definido por START <= apertura <= END. Los máximos y mínimos globales son iguales en los cuatro casos: 30868.75 y 30846.

Las diez curvas de 18:54:16, :29 y :30 son exactamente iguales en los timestamps cerrados comunes. Sus intervalos compatibles son [66.99438202247191, 67.04861111111111); el de :15 es [117.95138888888889, 118.00561797752809). Se informa el único entero compatible; esto no prueba por sí solo que el C interno sea entero.

**El salto ocurre al pasar de :15 a :16, no exige esperar hasta :30.** Esto apoya que el rango se forma seleccionando velas por su timestamp de apertura y excluyendo la vela de :15 cuando START queda dentro de ella. Los 14 segundos adicionales entre :16 y :30 no cambian las curvas. No se editaron cotizaciones históricas.

El experimento distingue el efecto de pertenencia temporal, pero no separa las propiedades de la vela retirada: precio, cuerpo, posición en la secuencia y posibles pivotes cambian junto con su exclusión. No demuestra que los pivotes sean irrelevantes, ni identifica aún la fórmula de C. La primera vela podría inicializar un estado que luego procesa el resto del rango.

Próxima hipótesis dirigida: comprobar reglas de inicialización y procesamiento de la secuencia al retirar una vela, usando varios pares vecinos con saltos y sin saltos. Comparar cuerpo, extremo inicial, primer tramo y estado acumulado con predicciones fijadas antes de medir. Un único swing limpio sería un control descriptivo, insuficiente para identificar el generador.

Resultados reproducibles: `C_limite_segundo.json`. CSV y capturas: `G:\trading\guias\analisis\manual`.

## Referencia restaurada

Al finalizar: gráfico y fuente Chart de 1m, START 18:55, END 19:20, Replay apagado y layout guardado. C_referencia_restaurada_limite_segundo.csv reproduce C62 (1,172 pares por curva; RMSE máximo 1.63e-12). Captura: C_limite_segundo_referencia_final.jpg.

