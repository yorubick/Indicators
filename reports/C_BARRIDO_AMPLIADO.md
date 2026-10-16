# Barrido ampliado de START y controles de recálculo

13 de octubre de 2026. NQ1!, Character Tree v6.5.36, perfil B, Manual, fuente Chart, gráfico de 15 segundos. END fijo: 12 de octubre, 19:20:00 UTC.

## Mediciones incorporadas

| START UTC | C entero compatible con los diez plots |
|---|---:|
| 18:52:00 | 67 |
| 18:53:00 | 118 |
| 19:01:00 | 47 |
| 19:02:00 | 47 |

Cada nueva selección se exportó después del recálculo y se repitió sin cambiar los inputs. El script compara los períodos y todos los valores de los diez plots en los timestamps comunes cerrados; excluye las dos últimas filas comunes. La cobertura OHLC de cada rango está completa y coincide exactamente con una referencia común. El control de START 18:54:00 se reprodujo con C = 123, como en el barrido previo.

Las cuatro mediciones nuevas se analizan junto con los trece inicios previamente medidos. Son ventanas superpuestas de una sola jornada, no una prueba independiente entre mercados o fechas.

## Resultado de las hipótesis dirigidas

Se clasificó la primera vela por dirección del cuerpo y por pivote local, usando 1, 2, 3 o 5 velas por lado. Para máximos: superior estricto a los vecinos izquierdos y superior o igual a los derechos; para mínimos, el criterio inverso. Los vecinos anteriores a START solo se usan para describir el pivote, no para afirmar que el indicador los utiliza.

Ninguna de estas clasificaciones, ni su combinación con la dirección del cuerpo, determina C por sí sola. Por ejemplo, la categoría alcista/sin pivote de una vela por lado contiene C = 47, 67 y 118. La categoría bajista/sin pivote contiene 67, 88, 106 y 123. Esto descarta una tabla simple basada exclusivamente en esas categorías; no descarta reglas con distancia, magnitud, pivotes internos o selección adaptativa.

## Hallazgo del procedimiento: una EMA correcta puede pertenecer al rango anterior

En el primer intento se cambiaron anclas y se exportó demasiado pronto. Tres archivos no pasaron la comprobación de EMA de cierre de período entero. Otros sí la pasaron, pero conservaban los períodos de la selección anterior. Por ejemplo, el primer archivo etiquetado 18:53 daba 67; la selección aplicada y estabilizada da 118. Un control provisional etiquetado 18:54 daba 47; después del recálculo volvió a 123.

Por ello, **pasar la recurrencia EMA no demuestra que la exportación corresponda al input recién solicitado**. Hay que verificar también las anclas, completar el recálculo, reproducir un control conocido y repetir la exportación sin cambios. La repetición tampoco es una garantía universal si ambas exportaciones se hacen antes de que termine el mismo recálculo.

Los archivos `C_barrido_15s_start*.csv` iniciales y los terminados en `_confirmado.csv` o `_repetido.csv` quedan conservados como diagnósticos, pero excluidos de las nuevas mediciones. El análisis acepta únicamente pares explícitos `_estabilizado.csv` / `_verificado.csv`. El control `_1854_estabilizado.csv` se usa para comprobar C = 123 y el OHLC común.

Este problema no invalida automáticamente todos los experimentos anteriores: los controles previos que fueron repetidos conservan evidencia de reproducibilidad. Sí añade un requisito de trazabilidad para futuras muestras y aconseja repetir cualquier caso aislado antes de usarlo como contraejemplo decisivo.

## Estado de la investigación

C sigue sin generador identificado. El barrido amplía el conjunto y permite rechazar las reglas categóricas indicadas. La siguiente pregunta es si los cambios de C responden a una condición cuantitativa de un pivote o contacto interno, no simplemente a que START sea alcista, bajista o pivote local.

Script reproducible: `analizar_C_barrido_ampliado.py`. Datos, intervalos, conteos de valores repetidos y categorías completas: `C_barrido_ampliado.json`. La referencia final se restaura a START 18:55, END 19:20 y fuente/gráfico de un minuto; su C esperado es 62.
