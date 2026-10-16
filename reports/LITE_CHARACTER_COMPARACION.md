# Comparación medida de EMA Origin Lite y Character Tree

13 octubre 2026. NQ1!, sesión ETH, UTC, ajuste de contratos apagado. Gráfico 1m. Character Tree v6.5.36: perfil B, Manual, fuente Chart. EMA Origin Lite v1.2: fuente explícita 1m. END fijo 12 octubre 19:20:00. Dos rangos medidos, cada uno con dos exportaciones aceptadas.

| START | C inferido Lite con familia sin redondear | C entero compatible Character |
|---|---:|---:|
| 18:55 | 62 | 62 |
| 18:54 | 134 | 134 |

## Diferencia identificada

Las seis curvas de Lite cumplen la recurrencia EMA de cierre con períodos **decimales**. En el control C62:

| Plot Lite | Período Lite | Correspondencia Character | Período Character |
|---|---:|---|---:|
| Lane 3 A | 24.8 | Layer A | 25 |
| Lane 3 B | 30.6555556 | Layer A boundary | 31 |
| Lane 2 A | 8.2666667 | Layer B | 8 |
| Lane 2 B | 10.2185185 | Layer B boundary | 10 |
| Lane 1 A | 2.7555556 | Layer C | 3 |
| Lane 1 B | 3.4061728 | Layer C boundary | 3 |

La correspondencia de Lane1B se determina por su orden/familia; en el primer caso LayerC y su boundary tienen ambos período3, por lo que el comparador automático puede escoger cualquiera según el error de niveles.

Los períodos Lite satisfacen N_fast = 72*C/(divisor*resolución), N_slow = 89*C/(divisor*resolución), con divisores 3, 9, 27. Al invertir cada una de las seis curvas, C62 se recupera entre 61.999999999996 y 62.000000000002; C134 entre 133.999999999998 y 134.000000000022. El RMSE de recurrencia máximo es inferior a 2.5e-12, con más de 1,330 pares por curva. Las parejas exportadas repiten exactamente sus plots cerrados comunes.

Character recupera los períodos enteros ya conocidos y los intervalos compatibles de C62/C134. Las curvas **no son idénticas**: los distintos períodos producen distintos valores. No se atribuyen todas las diferencias de niveles exclusivamente al redondeo sin reconstruir también las semillas y otras reglas de publicación.

En C62, la primera aparición de Lane3A y Lane1A es a las 19:26 UTC, igual que LayerA/LayerC de Character. Este control de visibilidad no basta para establecer equivalencia universal de su selección de dirección.

## Qué aporta a la investigación

La versión Lite permite inferir C prácticamente sin la pérdida de precisión causada por redondear los períodos, bajo la familia que coincide en estos dos rangos. Esto facilita probar si C presenta valores fraccionarios en otros rangos y localizar cambios pequeños que Character podría ocultar. El extractor antiguo `obtener_C.py` exige diez plots y períodos enteros; no debe aplicarse directamente a Lite.

No se obtuvo código Pine ni la fórmula que genera C desde OHLC. Solo dos ventanas superpuestas de una jornada fueron comparadas. Coincidir en C62 y C134 apoya un núcleo relacionado, pero no demuestra que ambos compartan todos los casos o toda la lógica. Antes de trasladar la investigación, comparar fuente15s y las fronteras START/END que ya producen saltos conocidos.

## Archivos y UI

CSV: `manual/Lite_1855_1920_1m_a.csv`, `_b.csv` y equivalentes `1854`. Script: `comparar_Lite_Character.py`, argumento opcional START `18:54:00` o `18:55:00`. Resultados: `Lite_1855_1920_1m_comparacion.json`, `Lite_1854_1920_1m_comparacion.json`.

El primer botón Use on chart abrió OW LEVELS; se canceló la colocación inicial y se cerró esa pestaña sin completar ni guardar el indicador. Tras activar nuestro layout y volver a usar el enlace directo, TradingView abrió una segunda pestaña del layout de investigación donde se añadió Lite. No aparecía aún al buscarlo en la lista de indicadores. La comparación se realizó en esa pestaña, conservando el indicador completo.

Al finalizar se restauró START18:55 en ambos, END19:20, gráfico1m y fuenteLite1m. Lite permanece añadido al layout de investigación para los siguientes controles.
