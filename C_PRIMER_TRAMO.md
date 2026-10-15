# ¿C queda determinado por la primera excursión?

13 octubre 2026. Análisis local de CSV ya medidos; no hubo nuevas mediciones en TradingView en esta tanda.

## Prueba dirigida

Se reunieron 21 rangos distintos de NQ1!, perfil B, Manual y fuente/gráfico 15s: los 13 START del barrido original, cuatro END adicionales y cuatro START con parejas verificadas del barrido ampliado. Todos pertenecen al 12 octubre y sus ventanas se superponen. El control fino :16/:29/:30 no se contó como tres nuevas secuencias: sus velas efectivas son idénticas.

Cada archivo vuelve a pasar el extractor de C y la comprobación de cobertura OHLC completa. La fórmula contrastada es **C = K × descriptor del primer evento**, con un solo K positivo para todos los casos. No se ajustaron coeficientes diferentes por rango.

Se definieron, para close, hl2, hlc3 y ohlc4:

- Tiempo desde START hasta el primer cambio de dirección de los cambios no nulos del precio.
- Altura global del rango dividida entre la amplitud de la excursión anterior a ese cambio.
- Tiempo hasta el primer desplazamiento respecto al precio inicial de 2.5 %, 5 %, 10 %, 25 % o 50 % de la altura global.
- Tiempo hasta la primera salida estricta del intervalo high/low de la vela inicial.
- Tiempo hasta el primer regreso o cruce de open, close o hl2 de la primera vela, después de haberse separado de ese nivel.

Los eventos se evalúan con precios completos del rango, no se inventa un evento cuando no ocurre. Los descriptores ausentes en algún rango quedan excluidos y enumerados en el JSON.

## Resultado

**Ninguna de las 37 reglas definidas en todos los casos admite un K común compatible con los intervalos de C.** Se intersectan los intervalos [C_inferior/descriptor, C_superior/descriptor), conservando la precisión del extractor; no se usan solo los enteros redondeados. El ajuste geométrico mostrado en JSON es descriptivo y no constituye validación predictiva.

La mejor aproximación de esta familia (tiempo al primer desplazamiento de ohlc4 del 2.5 % de altura) requiere K >= 8.196759 y K < 2.234954 simultáneamente: imposible. Su ajuste descriptivo tiene un error máximo de 83.7 %. Esto descarta esa familia finita de reglas proporcionales, no toda regla de inicialización ni todo algoritmo acumulativo.

## Contraejemplo sin ajuste

| START | END | C entero compatible |
|---|---|---:|
| 18:55:00 | 19:21:00 | 115 |
| 18:55:00 | 19:22:00 | 106 |

Los primeros **105 registros OHLC son idénticos** (aperturas desde 18:55 hasta 19:21 inclusive, 26 minutos entre extremos). Los 37 descriptores admitidos también son iguales, pero los intervalos de C son distintos. Hay ocho pares de ventanas con prefijo común y C distinto en el conjunto.

Por tanto, C no queda fijado únicamente por esos primeros eventos ni por un estado que deje de incorporar datos después de ellos. Sigue siendo posible que la primera vela inicialice un cálculo que continúa hasta END, o que se utilice una condición que dependa del final. Estos CSV no excluyen por sí solos influencia de cotizaciones posteriores a END.

## Siguiente experimento que discrimina mejor

El control de segundos mostró que el salto 118 → 67 coincide con retirar una vela fuente. Ahora conviene aislar cuánto del cálculo depende del final: barrer END vela por vela con START fijo, registrar C y OHLC, y contrastar cambios de C contra entradas de nuevos extremos, reversión y acumulación de recorrido. Repetir al menos un tramo sin salto y uno con salto. Fijar las condiciones candidatas antes de comparar; evitar coeficientes individuales que solo reproduzcan cada observación.

Archivos: `probar_C_primer_tramo.py` y `C_primer_tramo.json`. No se identificó aún el generador de C.
