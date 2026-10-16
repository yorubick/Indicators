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

## Por qué importan para C (hipótesis iniciales, corregidas más abajo)

> Estas hipótesis se escribieron antes de leer los textos de ayuda. Según esos textos, los cuatro ajustes solo actúan en Auto Balanced; ver [Lectura de los textos para el problema de C](#lectura-de-los-textos-para-el-problema-de-c).

- **«Reject fits closed through»** y **«Capping cloud: Auto (middle, then slow)»** indican que el indicador **ajusta** (fit) candidatos y descarta los que el precio atraviesa al cierre, usando como techo la nube media y, si no basta, la lenta. Eso encaja con un C elegido por búsqueda entre enteros: explicaría el C entero del régimen largo, las mesetas y los saltos no monótonos al añadir una vela.
- **«Box starts at leg extreme»** sugiere que el inicio efectivo de la caja puede ser el extremo del tramo y no la vela START marcada. Eso explicaría la gran sensibilidad de C a una sola vela al inicio (88 frente a 61 con START 19:03:15 frente a 19:03:30).
- **«Range spans session breaks»** puede influir en la prueba ETH frente a RTH.

## Pendiente

- ~~Texto de cada icono de ayuda y opciones de los desplegables~~: transcritos abajo.
- Captura equivalente de los ajustes del **Lite** oficial, para saber cuáles de estas opciones existen allí y con qué valor fijo.

## Textos de ayuda (ⓘ) y opciones de los desplegables

Transcritos en el panel por Luna el 16-oct-2026 a petición del usuario, sin cambiar ajustes. Indicador identificado como **Character Tree v6.5.61 – Public (`CT6561USR`)**. Se copian literalmente.

### Setup

- **Box selection:** Manual uses START and END. Auto Balanced uses END and a later retracement wick to find the range automatically.
- **Point 1 time:** Manual: click the range START candle. Auto: click the fixed box END candle.
- **Point 2 time:** Manual: click the range END candle (price is ignored). Auto: click the later RETRACEMENT WICK, including its price. When changing modes, reposition both points for their new roles.
- **Data resolution:** Source for the range, Character, clouds and Flow Bands, in both modes. 1S is the most precise but only reaches a few days back; use 10S (weeks) or 1 minute (months) for older setups.
- **Setup direction:** Auto Balanced: Auto reads Point 2 price (above the END candle high = bullish, below = bearish); Bullish / Bearish force the side. Manual: Auto reads where END sits in the box (upper half = bearish, lower half = bullish); Bullish / Bearish force the side. The clouds start drawing from END straight away.
- **Capping cloud:** Auto Balanced only. Which Character cloud caps the retracement into the wick. Auto tries the middle cloud first and uses the slow cloud when no range carries the middle-cloud Character.
- **Reject fits closed through:** Auto Balanced only. A cloud only counts if no 1-minute close went through it between END and the wick (wicks are allowed).
- **Range spans session breaks:** Auto Balanced only. Measures range length in traded time: the daily break and weekends do not count. Lets a range just after the open include the session before the break.
- **Box starts at leg extreme:** Auto Balanced only. The range starts at its own extreme: the high the leg into END began from (bearish), or the low (bullish).
- **Auto history (source bars):** Auto Balanced only. How many source bars back the range engine reads. On 1S, 300,000 is roughly 4-5 trading days; on 10S roughly 6 weeks. Raise it, or use a coarser Data resolution, if END is older and the box does not appear.
- **Minimum range (minutes):** Auto Balanced only. 0 = no minimum. Above 0, shorter ranges are rejected; if the Character fitted to the wick cannot support a range this long, the shortest-window estimated box is drawn.

### Cloud kisses

- **Show cloud kisses:** A faster cloud is dragged into the next slower cloud, touches it without a confirmed cross (centre closing through), then releases back in the trend direction. Marked on the release bar.
- **Cloud pairs:** Fast-Middle: the fast cloud kissing the middle cloud. Middle-Slow: the middle cloud kissing the slow cloud (the parent version, labelled KISS P).
- **Show kiss level:** Line at the faster cloud's extreme during the kiss, extended until a 1-minute close goes back through it.

### Flow Bands

- **One entry per pullback:** After a BUY, no new BUY until a band candle closes back at or above the band basis (or an EXIT prints). SELL mirrors this. Stops entries stacking into a move against you.
- **Entries need middle cloud aligned:** BUY only while the middle cloud is turned up (fast above slow); SELL only while it is turned down. Blocks entries once the pullback has become a counter-trend move.
- **Show Auto direction tag:** Auto only. Marks the starting side at END and shows the live side on the last bar.
- **Auto flip confirmation:** Auto only. What the flip close must also clear. Extra cloud 1: the slowest cloud, which ignores chop around the slow cloud. Slow cloud: the slow main cloud. Swing: the last confirmed band-candle swing.
- **Auto flip speed:** Auto only. Flips when completed band candles close beyond the inner band the current side should defend AND beyond the selected confirmation. Balanced = two consecutive closes, Fast = one.

### Projections

- **Show fib projections:** Show or hide the standard horizontal price projections and their labels.
- **Show Feigenbaum lines:** Show or hide the vertical timing lines and M-end label.

En las pestañas Style y Visibility no hay textos de ayuda.

### Opciones de los desplegables

- Box selection (actual: Manual): `Manual`; `Auto Balanced`
- Setup direction (actual: Auto): `Auto`; `Bullish`; `Bearish`
- Capping cloud (actual: Auto (middle, then slow)): `Auto (middle, then slow)`; `Middle cloud`; `Slow cloud`
- Data resolution (actual: 1 minute): `Chart`; `1 tick`; `10 ticks`; `100 ticks`; `1000 ticks`; `1 second`; `5 seconds`; `10 seconds`; `15 seconds`; `30 seconds`; `45 seconds`; `1 minute`; `2 minutes`; `3 minutes`; `5 minutes`; `9 minutes`; `10 minutes`; `15 minutes`; `30 minutes`; `45 minutes`; `81 minutes`; `1 hour`; `2 hours`; `3 hours`; `4 hours`; `1 day`; `1 week`; `1 month`; `3 months`; `6 months`; `12 months`
- Cloud pairs (actual: Fast-Middle + Middle-Slow): `Fast-Middle`; `Fast-Middle + Middle-Slow`
- Auto flip confirmation (actual: Extra cloud 1): `Extra cloud 1`; `Slow cloud`; `Swing`
- Auto flip speed (actual: Balanced): `Balanced`; `Fast`

## Lectura de los textos para el problema de C

- En los textos, C se llama **«Character»**. Se calcula a partir de la fuente elegida en «Data resolution» («Source for the range, Character, clouds…»).
- Los cinco ajustes que parecían describir la elección de C (Capping cloud, Reject fits closed through, Range spans session breaks, Box starts at leg extreme, Minimum range) son **solo de Auto Balanced**. En Manual no actúan: confirmado con `manual/CT_1400_1422_reject_off_*.csv`, idénticos entre sí y con C del Lite = 83,0000.
- En **Auto Balanced** el indicador resuelve el problema inverso: **ajusta el Character a la mecha de retroceso** («the Character fitted to the wick»), con la nube que debe «capar» el retroceso desde END hasta la mecha, y luego busca un **rango que «lleve» ese Character** («no range carries the middle-cloud Character»). Por tanto existe una correspondencia rango → Character que el motor evalúa sobre muchos rangos candidatos (hasta 300.000 velas de la fuente), y la longitud del rango se mide en **tiempo negociado** («Range spans session breaks»).
- «The clouds start drawing from END straight away»: las nubes de Character Tree arrancan en END.
