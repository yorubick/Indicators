# C: estructura del precio y comprobación con rangos reservados

Prueba ejecutada el 13 de octubre de 2026. Perfil B, selección Manual.

**Resultado: no se identificó el generador de C.** Ninguna de las 3,360 fórmulas probadas admite un coeficiente común compatible con todos los intervalos originales de C del conjunto de ajuste.

## Método reproducible

Ejecutar `probar_C_estructura.py` con Python y NumPy. El script importa el extractor `obtener_C.py`, comprueba la cobertura completa de OHLC y vuelve a verificar el C compatible con los diez plots de cada exportación. No modifica TradingView.

- Ajuste: 28 rangos previamente medidos, incluidos tres controles que están en el mínimo empírico C = resolución.
- Comprobación reservada: seis casos de los rangos 18:54–19:21:30 y 18:00–19:21:30, con fuentes de 30, 60 y 120 segundos. El final efectivo cambia según la apertura de la última vela incluida.
- Los resultados reservados no se usan para ajustar el coeficiente ni ordenar las fórmulas. Se ordena por el peor error relativo en el conjunto de ajuste.
- Son rangos de la misma fecha y hay solapamiento de precios. Constituyen un contraste adicional, no validación independiente entre jornadas. El rango que comienza a las 18:00 amplía la ventana y la fuente de 120 segundos no estaba en el ajuste.
- Tres exportaciones antiguas carecen de todo el comienzo del rango. Para sus OHLC se utiliza `character_manual_15m_1m.csv`, que contiene los timestamps completos; C se extrae de los plots de su propio archivo. Esto queda identificado por `OHLC_fallback` en el resultado.

Se calculan 40 características comunes: duración, altura respecto a rango/verdadero rango/cuerpo/cambio de precio, dispersión, eficiencia, recorrido acumulado, distancia y antigüedad de extremos, duración media de giros, separación de pivotes y autocorrelación del precio sin tendencia lineal. Se prueban seis potencias de cada característica y productos/cocientes de dos características con potencias ±1.

Familia acotada:

`C_estimado = max(resolución, K × resolución × característica_1^p × característica_2^q)`

El coeficiente K se ajusta únicamente con casos de ajuste por encima del mínimo, mediante media geométrica. La saturación en la resolución es una hipótesis empírica, no una regla interna demostrada.

Para rechazar una fórmula exacta no se depende solo de ese ajuste: cada intervalo medido de C impone un intervalo admisible de K. Se comprueba si la intersección de todos ellos está vacía. Fue vacía en las 3,360 candidatas, incluso usando solamente los casos por encima del mínimo.

## Mejor aproximación, todavía inservible como réplica

La menor desviación máxima de ajuste corresponde a una fórmula equivalente al número de cambios de signo del cierre, ignorando cambios de precio iguales a cero:

`C_estimado = max(resolución, 0.1163064843942518 × resolución × (giros + 1))`

Falla hasta 29.69 % en ajuste y 42.42 % en comprobación reservada. No coincide con ningún intervalo de C de los seis casos reservados. No debe incorporarse a una réplica como si estuviera validada.

| Inicio UTC | Última apertura UTC | Fuente | C compatible medido | C estimado |
|---|---|---:|---:|---:|
| 18:54:00 | 19:21:30 | 30 s | 136 | 90.72 |
| 18:54:00 | 19:21:00 | 60 s | 109 | 104.68 |
| 18:54:00 | 19:20:00 | 120 s | 120 | 153.52 |
| 18:00:00 | 19:21:30 | 30 s | 196 | 268.67 |
| 18:00:00 | 19:21:00 | 60 s | 196 | 279.14 |
| 18:00:00 | 19:20:00 | 120 s | 268 | 348.92 |

## Pista para orientar el próximo experimento

Dos selecciones con fuente de 15 segundos y END 19:20:00 difieren únicamente en quitar la primera vela:

| START UTC | Velas | C compatible | Altura / TR medio | Altura / rango medio |
|---|---:|---:|---:|---:|
| 18:54:15 | 104 | 118 | 7.116932 | 7.229947 |
| 18:54:30 | 103 | 67 | 7.156515 | 7.237838 |

C cae 43.22 %, pero altura/TR medio cambia aproximadamente 0.56 % y altura/rango medio 0.11 %. Esto no demuestra una regla discreta: una transformación continua muy sensible también podría producir el salto. Sí justifica priorizar un umbral, una selección entre ramas o una condición vinculada a la primera vela antes que repetir fórmulas de volatilidad promedio.

Una prueba siguiente útil sería mantener END y fuente fijos, medir START en una ventana más amplia alrededor de esos dos puntos y buscar si los saltos coinciden con cambios de pivote, contacto o condición de la vela inicial. Los saltos ya observados no bastan para elegir entre esas explicaciones.

Datos completos y diez mejores candidatas: `C_estructura.json`. Script: `probar_C_estructura.py`.

Alcance del rechazo: únicamente esta familia finita de fórmulas, con sus características, potencias y saturación indicadas. No descarta cálculos adaptativos, búsquedas de períodos, reglas distintas de pivotes ni dependencia de información fuera del rango.
