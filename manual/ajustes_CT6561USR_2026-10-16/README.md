# Ajustes de Character Tree (instancia CT6561USR), 16-oct-2026

Capturas tomadas por el usuario en TradingView al configurar la prueba M1 de [`EXP-20261016-dependencias`](../../experimentos/EXP-20261016-dependencias/README.md). NQ1!, 1 m, ETH, UTC. El panel se titula **CT6561USR**, aunque la leyenda del gráfico mostraba antes «Character Tree v6.3 - User Release»: no es la v6.5.36 de la que salieron las etiquetas «C/3 …s» documentadas en `reports/ETIQUETAS_OFICIALES_PARA_GEMINI.md`.

Línea de estado del indicador: `CT6561USR B Dark Manual 29,480.44 29,840.75 1 Auto Auto (middle, then slow) 300,000 0 Fast-Middle + M…`

## Inputs visibles (valores de las capturas)

| Sección | Ajuste | Valor | Icono de ayuda |
|---|---|---|---|
| Appearance | Profile | B | |
| | Theme | Dark | |
| | Show delivery signals | sí | |
| Setup | Box selection | Manual | sí |
| | Point 1 price / time | 29480.442 / 2026-10-12 14:00 | sí |
| | Point 2 price / time | 29840.75 / 2026-10-12 14:22 | sí |
| | Data resolution | 1 minute | sí |
| | Setup direction | Auto | sí |
| | **Capping cloud** | **Auto (middle, then slow)** | sí |
| | **Reject fits closed through** | **sí** | sí |
| | **Range spans session breaks** | **sí** | sí |
| | **Box starts at leg extreme** | **sí** | sí |
| | Auto history (source bars) | 300000 | sí |
| | Minimum range (minutes) | 0 | sí |
| Cloud kisses | Show cloud kisses | sí | sí |
| | Cloud pairs | Fast-Mi… (Fast-Middle + …) | sí |
| | Show kiss level | sí | sí |
| Flow bands signals | Show Flow Bands signals | sí | |
| | Direction mode | Auto | |
| | Show Auto flips (BULL FLOW / BEAR FLOW) | sí | |
| | One entry per pullback | sí | sí |
| | Entries need middle cloud aligned | sí | sí |
| | Show Auto direction tag | sí | sí |
| | Auto flip confirmation | Extra cl… | sí |
| | Auto flip speed | Balanced | sí |
| | Colores, textos y visibilidad de BUY/SELL/EXIT/COVER, Signal display (Pane la…), Signal size (Tiny) | — | |
| 3. Character EMAs | Show extra EMA clouds | no | |
| | Extra cloud 1 / 2 colour | — | |
| Projections | Show fib projections | no | sí |
| | Show Feigenbaum lines | no | sí |
| Display | Show range | sí | |
| | Show PD arrays | no | |
| | Range transparency | 90 | |
| PD array colours | Show PD array 50% lines, colores, Fill transparency 87 | — | |

**No aparece** la opción «Show EMA timeframe labels» de la v6.5.36, así que en esta instancia no se puede leer C en la etiqueta «C/3 …s».

## Por qué importan para C (hipótesis, no resultados)

- **«Reject fits closed through»** y **«Capping cloud: Auto (middle, then slow)»** indican que el indicador **ajusta** (fit) candidatos y descarta los que el precio atraviesa al cierre, usando como techo la nube media y, si no basta, la lenta. Eso encaja con un C elegido por búsqueda entre enteros: explicaría el C entero del régimen largo, las mesetas y los saltos no monótonos al añadir una vela.
- **«Box starts at leg extreme»** sugiere que el inicio efectivo de la caja puede ser el extremo del tramo y no la vela START marcada. Eso explicaría la gran sensibilidad de C a una sola vela al inicio (88 frente a 61 con START 19:03:15 frente a 19:03:30).
- **«Range spans session breaks»** puede influir en la prueba ETH frente a RTH.

## Pendiente

- Texto de cada icono de ayuda (ⓘ) y la lista completa de opciones de cada desplegable: Box selection, Setup direction, Capping cloud, Cloud pairs, Auto flip confirmation, Auto flip speed y Data resolution.
- Captura equivalente de los ajustes del **Lite** oficial, para saber cuáles de estas opciones existen allí y con qué valor fijo.
