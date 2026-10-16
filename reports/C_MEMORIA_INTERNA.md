# Memoria del precio en ventanas internas prefijadas

13 octubre 2026. Análisis local de los CSV existentes; no nuevas mediciones en TradingView.

## Hipótesis y definición

Se contrastó si C representa una escala de memoria obtenida mediante una relación autorregresiva de primer orden: precio siguiente = intercepto + phi × precio anterior. Phi se calcula como covarianza centrada entre ambas secuencias dividida por la varianza de la secuencia retrasada.

Para 0 < phi < 1 se evaluaron dos escalas: período EMA equivalente (1+phi)/(1-phi), y tiempo de decaimiento en velas -1/log(phi). Se probaron por separado phi positivo y valor absoluto de phi; no se recortaron coeficientes fuera del intervalo para fabricar un resultado.

Las ventanas se fijaron antes del cálculo: rango completo, última mitad, último cuarto, desde el último máximo global, desde el último mínimo global y últimas 8, 13, 21, 34 o 55 velas cuando existen. Las cuatro fuentes son close, hl2, hlc3 y ohlc4. Cada una se procesa como nivel, residual respecto a una recta ajustada a esa ventana, o diferencias consecutivas. Se exigen al menos cinco precios en la ventana original y varianza positiva.

Son **480 variantes**, sin seleccionar una ventana distinta por caso para aproximarse al C observado. La predicción contrastada es C = max(resolución, K × resolución × escala). El piso es una opción empírica y no se afirma que sea la regla interna.

## Resultados

Se utilizaron 30 casos anteriores con C superior a la resolución para ajustar y ordenar las reglas; las cinco ventanas recientes del barrido END se evaluaron después. Las 30 incluyen muestras que fueron reservadas en pruebas anteriores: aquí son datos previos, no una validación independiente. Todo procede de una jornada y ventanas superpuestas.

154 variantes están definidas en todos los casos anteriores; **ninguna tiene un intervalo común compatible de K**. Las demás no se pueden calcular en algún caso por ventana insuficiente, varianza nula o phi fuera de (0,1). No se interpretan esos fallos como pruebas contra toda medida posible de memoria.

La mejor variante por error máximo anterior usa el rango completo, cierres con tendencia lineal retirada, phi positivo y período EMA equivalente. Necesita simultáneamente K >= 0.748107 y K < 0.255003, por lo que no puede ser exacta. El ajuste descriptivo K = 0.434980 tiene error máximo anterior de 70.6 %.

| END UTC | C entero compatible medido | Predicción de la mejor variante anterior |
|---|---:|---:|
| 19:21:00 | 115 | 101.91 |
| 19:21:15 | 106 | 104.18 |
| 19:21:30 | 79 | 98.41 |
| 19:21:45 | 66 | 102.39 |
| 19:22:00 | 106 | 100.87 |

No coincide con ninguno de los cinco intervalos inferidos de C. La regla varía poco y no reproduce los saltos medidos. No se eligió por sus resultados en esas cinco ventanas.

## Alcance y siguiente discriminación

Esto descarta la familia definida de memoria AR(1) proporcional, no todas las reglas de selección de ventanas internas, todas las regresiones o las medidas adaptativas. Aún no conocemos el generador de C.

Para avanzar con mediciones nuevas, conviene aislar una posible selección discreta de puntos: desplazar END alrededor de un pivote confirmado, con rangos de igual número de velas en otra zona, y ver si C conserva o sustituye un valor al confirmar ese pivote. El salto del barrido actual no lo explica una escala suave de memoria como la aquí probada.

Script: `probar_C_memoria_interna.py`. Resultados, casos, cobertura y diez mejores reglas anteriores: `C_memoria_interna.json`.
