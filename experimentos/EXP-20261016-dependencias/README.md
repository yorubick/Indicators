# EXP-20261016-dependencias: ¿de qué datos depende C?

**Registrado:** 16-oct-2026, antes de cualquier medición nueva.
**Objetivo:** antes de buscar más fórmulas, determinar qué entradas usa el indicador para fijar C en el régimen largo ($n \ge 21$). Todas las búsquedas anteriores asumían que C depende solo de las velas START..END, y ninguna funcionó (ver `reports/MODELOS_REFUTADOS_PARA_GEMINI.md` y `docs/EVALUADOR_C.md`).

## Resultados obtenidos sin medir (16-oct)

| # | Pregunta | Resultado | Cómo reproducirlo |
|---|---|---|---|
| A1 | ¿Son fiables las velas 1 m del conector de TradingView? | Sí: las 2.569 velas 1 m del maestro coinciden exactamente (OHLC y volumen). | `NQ1_1m_2026-10-12_13.json` (12 y 13-oct completos, ETH) |
| A2 | ¿Cambia C después de publicarse? | No. Invertido vela a vela, C es constante con 4 decimales en más de 2.200 velas (62,2951 y 75,0000). | `python tools/invertir_C_csv.py manual/Lite_0445_050500_1m_b.csv` |
| A3 | ¿Es C del régimen largo $\operatorname{round}(k\,\Delta t/18.3)$ con $k$ entero? | No. En 1 m encajan 26/72 casos, frente a 22 esperados por azar. | Para cada C entero, ¿existe $k$ entero en $[(C-0{,}5)\cdot 18.3/\Delta t,\ (C+0{,}5)\cdot 18.3/\Delta t]$? Azar = $18.3/60$ por caso. |
| A4 | ¿Depende C del tiempo hasta la ruptura de la vela END? | No en forma simple: con 12 variantes, el máximo es 3/72 aciertos. En saltos como 71 → 128 (START 19:04), ambas ventanas rompen en la vela siguiente a END. | `python experimentos/EXP-20261016-dependencias/prueba_ruptura_post_END.py` |
| A6 | ¿Es C el menor entero cuya nube (rápida, media o lenta, o media y luego lenta) no es atravesada al cierre dentro de la caja? | No en la forma simple: 24 variantes (semilla en el extremo o en el cierre, atravesar una o las dos curvas, inicio en START o en el extremo del tramo); máximo 6/121 aciertos. Inspirada en los ajustes «Reject fits closed through» y «Capping cloud» de Character Tree. | `scratchpad` del 16-oct; reproducible con la descripción de esta fila |
| A7 | ¿Cómo actualiza Character Tree sus curvas tras un hueco de tiempo? | Como si pasaran $\Delta t_{hueco}/\Delta t$ actualizaciones: en el corte diario (3.660 s), $L = x - (x - L_{prev})(1-\alpha)^{61}$, exacto a 4 decimales en las 6 curvas. Sus periodos son **enteros** en velas de la fuente (33/41, 11/14, 4/5 para C = 82–83). | `manual/CME_MINI_NQ1!, 1_2026-10-16T160654.582_CT_1400_1422.csv`, vela 1791842400 |
| A8 | ¿Y el Lite? | No compensa: una sola actualización por vela, también en el corte diario. Sus periodos no son enteros ($b_0 C/\Delta t$ exacto). Nuestro clon hace lo mismo que Lite, correcto. **Para invertir C con Character Tree hay que excluir los pasos que cruzan un hueco.** | `manual/Lite_0445_050500_1m_b.csv`, vela 1791842400 |
| A5 | ¿Determina la geometría de la caja (máximo, mínimo y su posición) el valor de C? | No. START 06:00 del 12-oct: caja idéntica en n = 21…24 y C = 77, 77, 77, 73. Casos 2 m con START 14:30 del 12-oct: caja idéntica y C = 124, 153, 146, 190. | `python tools/evaluador_C.py` y la tabla del 16-oct |

## Mediciones solicitadas

### M1. Sesión ETH frente a RTH (dependencia de la historia anterior a START)

**Lógica.** Una ventana que cae entera dentro de la sesión regular tiene las mismas velas en ETH y en RTH. Lo que cambia es la historia anterior a START: en RTH no existen las velas nocturnas, y antes de las 13:30 UTC vienen las de la sesión regular anterior. Si C cambia entre ETH y RTH, C depende de datos anteriores a START. Si no cambia en ninguna ventana, esa dependencia queda muy acotada.

**Configuración.** NQ1!, gráfico 1 m, fuente del indicador 1 m, UTC, B-ADJ desactivado, Replay desactivado, perfil y modo iguales a los de las mediciones del 12-oct (`B`, `Manual`). Lo **único** que se cambia es la sesión del gráfico a **RTH** (horario regular).

| Control | START (UTC) | END (UTC) | n | C medido en ETH | Predicción si C depende solo de la ventana |
|---|---|---|---:|---:|---:|
| M1-0 (comprobación del método, régimen corto) | 2026-10-12 14:00 | 14:19 | 20 | 65,5738 | 65,5738 |
| M1-1 | 2026-10-12 14:00 | 14:20 | 21 | 62 | 62 |
| M1-2 | 2026-10-12 14:00 | 14:22 | 23 | 83 | 83 |
| M1-3 | 2026-10-12 14:00 | 14:23 | 24 | 76 | 76 |
| M1-4 | 2026-10-12 15:27 | 15:51 | 25 | 93 | 93 |
| M1-5 | 2026-10-12 15:30 | 15:50 | 21 | 69 | 69 |
| M1-6 (nueva, junto a la apertura) | 2026-10-12 13:31 | 13:53 | 23 | medir **también en ETH** | ETH = RTH |

M1-6 es la más sensible: en RTH solo hay una vela de esa sesión antes de START, frente a toda la madrugada en ETH.

### M2. Replay en la primera vela publicada (dependencia de datos posteriores)

Ventana 2026-10-12 19:04–19:28, fuente 1 m (C = 128 en modo normal). Activar Replay en 19:28, avanzar de una en una vela hasta que aparezcan las curvas y exportar el CSV en ese momento. Predicción si C no usa datos futuros: 128. Si sale distinto, el indicador usa datos posteriores (lookahead o recálculo con toda la historia).

### M3. Ajustes del indicador

Captura de **todas** las entradas de PoiSzn EMA Origin Lite (pestañas «Inputs» y «Style»), con el número de versión visible. Si alguna entrada tiene icono de ayuda, captura también su texto. Sirve para saber si hay entradas (modo de anclaje, sensibilidad, «balanced/broad») que intervengan en C.

## Formato de entrega

Para cada control M1/M2: una exportación CSV del gráfico («Exportar datos del gráfico», formato de hora UNIX), con el mismo nombre que la configuración, por ejemplo `manual/RTH_20261012_1400_1420_1m_a.csv`. El CSV debe incluir las columnas `Lane 1 A` … `Lane 3 B` y varias velas posteriores a la ruptura. No hace falta leer valores a mano: C se recupera con `tools/invertir_C_csv.py`.

### M4. Interruptores de Character Tree (prioridad máxima)

**Lógica.** Character Tree (instancia CT6561USR, ver [`manual/ajustes_CT6561USR_2026-10-16/`](../../manual/ajustes_CT6561USR_2026-10-16/README.md)) expone ajustes cuyo nombre describe el mecanismo de C: «Reject fits closed through», «Capping cloud: Auto (middle, then slow)», «Box starts at leg extreme», «Range spans session breaks» y «Setup direction». Si al cambiar uno de ellos cambia C con la misma ventana, ese ajuste interviene en el cálculo. En 74/74 casos del maestro, el C de Character Tree coincide con el de Lite, así que el mecanismo con los ajustes por defecto es el mismo.

**Hipótesis nula registrada:** estos ajustes solo afectan a las señales, y C sigue en 83 en todas las variantes.

**Configuración fija:** NQ1!, 1 m, **ETH**, UTC, B-ADJ desactivado. Character Tree: Profile B, Box selection Manual, Point 1 = 2026-10-12 14:00, Point 2 = 2026-10-12 14:22, Data resolution 1 minute. Con Lite cargado en la misma ventana, si es posible. Valor de referencia: C = 83.

| Archivo | Cambio respecto a los ajustes por defecto |
|---|---|
| `CT_1400_1422_base.csv` | ninguno. Recibido el 16-oct como `manual/CME_MINI_NQ1!, 1_2026-10-16T160654.582_CT_1400_1422.csv` (solo Character Tree, sin nubes extra): curvas desde 14:23, C compatible con {82, 83}, referencia 83. |
| `CT_1400_1422_reject_off.csv` | Reject fits closed through: desactivado |
| `CT_1400_1422_legext_off.csv` | Box starts at leg extreme: desactivado |
| `CT_1400_1422_capping_<opción>.csv` | Capping cloud: cada opción distinta de «Auto (middle, then slow)» |
| `CT_1400_1422_sessionbreaks_off.csv` | Range spans session breaks: desactivado |
| `CT_1400_1422_direction_<opción>.csv` | Setup direction: cada opción distinta de «Auto» |

Cada exportación debe incluir varias decenas de velas posteriores a 14:22, con **«Show extra EMA clouds» activado** (sus periodos, unos 3 C/Δt, reducen el intervalo de C a menos de 0,3 s) y, si es posible, con Lite cargado en la misma ventana para tener C exacto. Después de cada variante se vuelve al valor por defecto. C se recupera con `obtener_C.recover` (Character Tree) y `tools/invertir_C_csv.py` (Lite).

**Resultado M4 (16-oct):** `manual/CT_1400_1422_reject_off_middle_cloud.csv` y `manual/CT_1400_1422_reject_off_slow_cloud.csv` son idénticos, con C del Lite = 83,0000 y C de Character Tree en {82, 83}. Se mantiene la hipótesis nula, pero la prueba no informa: según los textos de ayuda, esos ajustes solo actúan en **Auto Balanced** (ver `manual/ajustes_CT6561USR_2026-10-16/README.md`). M4 queda sustituida por M5.

### M5. Auto Balanced: el indicador elige el rango para un Character

**Lógica.** En Auto Balanced, Character Tree ajusta el Character (C) a una mecha de retroceso posterior a END y dibuja el rango que «lleva» ese Character. Cada ejecución da un par (rango, C) generado por el propio indicador, y la curva desde END hasta la mecha muestra qué criterio de ajuste usa.

**Configuración:** NQ1!, 1 m, ETH, UTC, B-ADJ desactivado. Character Tree: Box selection **Auto Balanced**, Data resolution 1 minute, **Show range** y **Show extra EMA clouds** activados, resto por defecto. Point 1 = vela END **2026-10-12 14:22**. Lite cargado en Manual con START 14:00 y END 14:22 (referencia fija, C = 83).

| Archivo | Point 2 (mecha) | Dirección esperada según la ayuda |
|---|---|---|
| `CT_auto_1422_w1429H.csv` | 14:29, precio 30906 (high) | alcista (> high de END, 30899,5) |
| `CT_auto_1422_w1443H.csv` | 14:43, precio 30911.25 (high) | alcista |
| `CT_auto_1422_w1448H.csv` | 14:48, precio 30921.25 (high) | alcista |
| `CT_auto_1422_w1426L.csv` | 14:26, precio 30859 (low) | bajista (< low de END, 30885,25) |

Para cada una, además del CSV: captura con la caja dibujada y la cruceta en su vela izquierda, para leer el START que eligió el indicador.

**Predicciones registradas:** (a) si C depende solo del rango, poner ese rango en Manual (START de la caja, END 14:22) da el mismo C que Auto; (b) la nube que «capa» (la media por defecto) toca la mecha: en la vela de la mecha, el precio de la mecha queda sobre el borde de la nube.

### Lectura rápida alternativa con Character Tree

En los 74 casos del maestro medidos con ambos indicadores, el C de Lite cae siempre dentro del intervalo de Character Tree. Por eso, para M1 bastaría leer en Character Tree la etiqueta **«C/3 …s»** (perfil B, modo Manual, resolución de datos 1 minuto, «Show EMA timeframe labels» activado), que aparece al publicarse las curvas: $C = 3 \times$ el valor de la etiqueta, con error de ±0,015 s, suficiente para identificar un C entero. Si alguna ventana da en RTH un C distinto del de ETH, se exporta además el CSV de Lite de esa ventana como evidencia primaria. **Actualización:** la instancia CT6561USR del usuario no tiene la opción de etiquetas, así que M1 se mide también por exportación CSV.

Seven Cloud (EMA 78/84 en temporalidades fijas, sin anclas) y Manual Anchored CCII (detector CSD/IDM, sin EMA) no calculan C y no intervienen en este experimento.

## Criterio de decisión

- **M1 sin diferencias en las 7 ventanas:** la historia anterior a START no interviene (al menos más allá de unas pocas velas). Siguiente paso: barrido denso START/END a 1 m con fuente 1 m para estudiar las transiciones.
- **M1 con diferencias:** C depende de la historia previa. Siguiente paso: medir cuántas velas previas intervienen, moviendo M1-6 a distintas distancias de la apertura de RTH.
- **M2 distinto de 128:** el indicador usa datos posteriores; cambia el planteamiento por completo.
