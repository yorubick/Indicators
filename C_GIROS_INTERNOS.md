# C y las escalas temporales de giros internos

13 de octubre de 2026. Análisis de las exportaciones ya verificadas; sin cambios en TradingView.

**No se encontró un generador de C.** Se contrastaron 224 reglas de escala temporal y se encontró un contraejemplo directo para usar exclusivamente el mayor giro entre pivotes consecutivos del cierre.

## Prueba de duraciones

Se emplean 34 casos anteriores para ajustar y ordenar los modelos. Las cuatro ventanas del último barrido (START 18:52, 18:53, 19:01 y 19:02, END 19:20, fuente 15 s) se contrastan después y no se usan para elegir el coeficiente ni ordenar las candidatas. Los cuatro resultados ya se conocían; esta separación limita el ajuste numérico, pero no equivale a una prueba prospectiva. Las ventanas se superponen y pertenecen a la misma jornada.

La cobertura OHLC completa y el C inferido se verifican de nuevo mediante `load()` y `recover()`. Se utilizan únicamente las exportaciones aceptadas del barrido nuevo.

Se prueban pivotes de mechas, cierre y hl2, con 1/2/3/5/8/13 vecinos por lado, así como una variante explícita de giros confirmados por retrocesos del 2.5/5/10/15/20/25/33.33/50 % de la altura del rango. Esta variante no pretende replicar una función oficial de ZigZag.

Las medidas incluyen separación entre pivotes, distancia desde START o hasta END, primer/último giro y duración del movimiento de mayor/menor amplitud. De todas las definiciones, 112 medidas están disponibles en los 38 casos. Cada una se contrasta con y sin redondeo a segundos:

`C = max(resolución, K × medida_temporal)`

La saturación en la resolución y el redondeo son hipótesis explícitas. El indicador no ha sido demostrado como internamente entero en todos los modos.

Cada observación impone límites admisibles al coeficiente K. Ninguna de las 224 reglas admite un K compatible con todos los casos de ajuste. El rechazo es para esta familia finita; no descarta reglas adaptativas ni todos los algoritmos de pivotes.

La mejor aproximación según el peor error de ajuste utiliza la antigüedad del primer máximo local del cierre, con un vecino por lado, más una vela, multiplicada por 0.0597663704569834. Su peor error es 44.39 % en ajuste y 47.76 % en las cuatro ventanas posteriores. Las predicciones son 99, 95, 65 y 64 segundos frente a C medido 67, 118, 47 y 47. Ninguna coincide con su intervalo original. No debe incorporarse a una réplica.

## Contraejemplo que no depende de ajustar K

En quince ventanas con END 19:20:00 y fuente 15 s, el movimiento de mayor amplitud entre pivotes consecutivos opuestos del cierre, definidos con un vecino por lado, es exactamente el mismo:

- Mínimo local: 19:00:15 UTC, cierre 30,848.75.
- Máximo local siguiente: 19:02:00 UTC, cierre 30,862.00.
- Duración: 105 segundos; amplitud: 13.25 puntos.

Sin embargo, C toma los valores 66, 67, 79, 88, 106, 118 y 123 según START. Un ejemplo con dos mediciones nuevas repetidas es START 18:52 → C67 frente a START 18:53 → C118: ambos conservan el giro descrito.

Por tanto, ninguna función que utilice **solo ese giro identificado** —sus extremos, precios, amplitud y duración— puede explicar los C distintos de esas ventanas. Esto no descarta seleccionar otro giro o combinarlo con el borde inicial, el resto del recorrido o los extremos globales.

## Lo que cambia en la búsqueda

Tenemos un contraejemplo concreto para una explicación intuitiva del indicador: C no es simplemente la duración del mayor giro del cierre, ni una transformación de ese giro aislado. Siguen abiertas la calibración al recorrido completo, una regla cuantitativa que dependa del borde inicial y la selección adaptativa entre distintas soluciones. No hay evidencia para estimar cuánto falta para reconstruir la fórmula.

Reproducción: `probar_C_giros_internos.py` con Python y NumPy. Resultados, intervalos admisibles, mejores aproximaciones y ventanas que comparten el giro: `C_giros_internos.json`.
