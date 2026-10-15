# C: ciclos del recorrido y cuantización a segundos

13 de octubre de 2026. Búsqueda del generador de C mediante CSV ya medidos. No se modificó TradingView ni se hicieron nuevas mediciones en esta tanda.

## Hipótesis nueva

C podría ser una escala de ciclo del precio dentro del rango, multiplicada por un factor global y eventualmente cuantizada a segundos. Se contrasta:

`C = max(resolución, cuantizar(K × resolución × período_espectral_en_velas))`

Se definen 288 descriptores antes de evaluar los resultados:

- Precios: close, hl2, hlc3, ohlc4.
- Transformaciones: quitar media; quitar tendencia lineal y media; diferencias consecutivas y quitar media.
- Ventanas de ponderación: rectangular, Hann, Hamming.
- Longitud FFT: la de la serie y cuatro veces esa longitud mediante relleno con ceros.
- Medidas: período del pico de potencia; promedio de períodos ponderado por potencia; inverso de frecuencia media ponderada; período en la mediana acumulada de potencia.

Se excluye la frecuencia cero. El relleno con ceros interpola la malla de frecuencias; no añade observaciones. La FFT es una herramienta local para probar la hipótesis, no una afirmación sobre el código del autor ni sobre funciones disponibles en Pine.

Cada descriptor se evalúa sin cuantizar y redondeando al segundo más cercano, al inferior o al superior: 1,152 reglas. Se exige un mismo K positivo para todos los rangos. No se cambia ventana, precio, transformación ni coeficiente según el C de cada caso.

## Datos y criterio de rechazo

Se usan 30 casos históricos sin saturación en la resolución, con cobertura OHLC comprobada y extracción de C repetida. Proceden de los casos de ajuste y agregación de C_estructura.json. Cinco END del barrido posterior se usan como diagnóstico, sin ajustar K ni seleccionar modelos con ellos. Son rangos superpuestos de una misma jornada; no constituyen validación independiente de mercado.

Cada rango impone un intervalo admisible de K. Sin cuantizar se conserva el intervalo inferido de los períodos originales. Con cuantización se usa el único entero C compatible: [C−0.5,C+0.5) para redondeo próximo, [C,C+1) para floor, y (C−1,C] para ceil. En el código se almacenan extremos numéricos; la inclusión invertida de ceil no afecta aquí, porque todas las intersecciones fallan por una separación estrictamente positiva.

## Resultado

**Ninguna de las 1,152 reglas admite un K común.** La menor separación entre restricciones contradictorias de K es 0.0983822, suficientemente mayor que el error numérico de extracción para que los extremos inclusivos no rescaten una candidata.

La mejor aproximación según el peor error en los 30 casos usa el pico espectral del cierre sin tendencia lineal, ponderación Hann, relleno 4× y redondeo próximo. Tiene error máximo del 45.45 % en ajuste. Exige simultáneamente:

| Restricción | START | END | Fuente | C | K requerido |
|---|---|---|---:|---:|---:|
| Inferior | 19:11 | 19:31 | 60 s | 80 | ≥ 0.173512 |
| Superior | 18:55 | 19:20:45 | 15 s | 66 | < 0.0745994 |

Esas condiciones son incompatibles. Su K descriptivo ajustado solo a los casos históricos es 0.107986 y produce:

| END con START 18:55 y fuente 15 s | C medido | Predicción |
|---|---:|---:|
| 19:21:00 | 115 | 97 |
| 19:21:15 | 106 | 98 |
| 19:21:30 | 79 | 99 |
| 19:21:45 | 66 | 100 |
| 19:22:00 | 106 | 101 |

No coincide en ningún END y no debe incorporarse a una réplica. No se descartan todos los modelos de ciclos, modelos no proporcionales ni selecciones adaptativas entre raíces. Se descarta esta familia finita y su cuantización explícita.

## Estado de la búsqueda

La regla que genera C desde OHLC sigue sin identificarse. Las mediciones de Lite permiten separar la precisión de C del redondeo de los períodos; no proporcionan por sí solas una fórmula. Una próxima búsqueda debe explicar los cambios abruptos por retirar una vela inicial o añadir una final. Este resultado evita continuar con un ciclo espectral global proporcional que suaviza los saltos de END en vez de reproducirlos.

Reproducción: ejecutar [probar_C_espectro.py](G:/trading/guias/analisis/probar_C_espectro.py). Resultados y casos de restricción: [C_espectro.json](G:/trading/guias/analisis/C_espectro.json).
