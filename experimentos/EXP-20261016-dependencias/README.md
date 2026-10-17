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

**Resultado M5 (16-oct, ejecutado por Luna; datos en [`experimentos/CT_auto_balanced_M5_2026-10-16/`](../CT_auto_balanced_M5_2026-10-16/README.md)).** C recuperado de los periodos enteros de las 10 curvas de Character Tree (con nubes extra el intervalo mide menos de 0,2 s). Las curvas se reconstruyen hacia atrás desde su primer valor con la recurrencia exacta.

| Mecha (Point 2) | START Auto (leído de la captura) | C Auto | Semilla en END | ¿Cierres que atraviesan las nubes entre END y la mecha? |
|---|---|---|---|---|
| 14:26 · 30859 (bajista) | 14:02 | 54,31–54,49 | 30899,50 = high END | 0 |
| 14:29 · 30906 (alcista) | 14:02 | 28,75–28,88 | 30885,25 = low END | 3–4 en todas las nubes |
| 14:43 · 30911,25 (alcista) | 13:56 | 159,44–159,58 | 30885,25 = low END | 6–8 en todas las nubes |
| 14:48 · 30921,25 (alcista) | 13:49 | 224,38–224,58 | 30885,25 = low END | 6–9 en todas las nubes |
| Manual 14:00–14:22 | — | 82,92–83,03 (Lite: 83,0000) | — | — |

Conclusiones:

1. **Semilla:** las 10 curvas valen exactamente el extremo de la vela END (mínimo en alcista, máximo en bajista). La reconstrucción hacia atrás converge sin ajuste.
2. **El C de Auto no es entero:** es un ajuste continuo, a diferencia del C entero del Lite en Manual en el régimen largo.
3. **Las curvas aparecen 16 minutos después de la mecha** en los cuatro casos.
4. **Predicción (b) refutada en su forma literal:** ninguna nube pasa por el precio marcado en la vela de la mecha (diferencias de 12 a 38 puntos).
5. **Los setups no eran válidos (error de diseño del protocolo):** en los tres casos alcistas el precio cae bajo el mínimo de END a las 14:26–14:27 y todas las nubes quedan atravesadas al cierre, de modo que ningún C cumple «Reject fits closed through». En el bajista se marcó un mínimo, no una mecha de retroceso hacia arriba. Estos C probablemente vienen del respaldo «shortest-window estimated box». M5 no contrasta el criterio de ajuste y debe repetirse con setups limpios.
6. **Predicción (a) sin evaluar:** falta la exportación Manual 14:02–14:22. Además, las mechas 14:26 y 14:29 dan C muy distintos (54 frente a 29) con el mismo START aparente, así que en Auto el C no es el Manual del rango dibujado.

### M5b. Auto Balanced con setups válidos (predicciones registradas)

Tres setups del 16-oct elegidos con `predecir_auto_balanced.py`: END en un pivote, mecha de retroceso posterior por el lado correcto del END (por debajo de su máximo si es bajista, por encima de su máximo si es alcista) y ningún cierre que atraviese la nube media entre END y la mecha. Predicciones de C en [`M5b_predicciones.json`](M5b_predicciones.json), para tres maneras de «tocar» la nube:

| Caso | Dirección | Point 1 (END) | Point 2 (mecha, precio) | C si toca la línea rápida | C si toca el centro | C si toca la línea lenta |
|---|---|---|---|---:|---:|---:|
| M5b-1 | alcista | 16-oct 14:28 | 14:42 · 29880 (mínimo) | 100,65 | 90,29 | 81,42 |
| M5b-2 | bajista | 16-oct 15:47 | 16:07 · 29657,75 (máximo) | 108,47 | 97,11 | 87,75 |
| M5b-3 | bajista | 16-oct 17:00 | 17:11 · 29530,5 (máximo) | 68,72 | 61,44 | 55,60 |

**Resultado M5b (16-oct, medido por Luna; CSV pendientes de subir a la rama):** C ≈ 63 (caso 1), ≈ 28 (caso 2) y ≈ 49,4 (caso 3). **Ninguna de las tres predicciones acierta.** Tampoco las 36 variantes probadas después (nube rápida, media, lenta y extra 1; línea rápida, centro y lenta; precio objetivo = extremo, cierre o apertura de la vela de la mecha): ninguna reproduce los tres valores. Queda refutado que el Character de Auto se ajuste para que una nube toque la mecha en su vela. **Verificación con los CSV** (`experimentos/CT_auto_balanced_M5_2026-10-16/CT_M5b_*.csv`, commit abbc0a6): C ∈ [62,92, 63,03) → 63; [27,98, 28,19) → 28; [49,33, 49,55), no entero. Semilla de nuevo igual al extremo de la vela END en los tres casos. En la captura del caso 3 la caja va de unas 16:40 a 17:00, aparece la etiqueta «middle cap» junto a la mecha y las nubes se dibujan en el gráfico desde END, aunque en el CSV empiezan a las 17:28. El «retraso» de 16 a 20 minutos es, por tanto, una propiedad de la exportación (probablemente esa parte se dibuja con objetos gráficos), no del cálculo. Con el C observado, la mecha atraviesa la nube media (lo que la ayuda permite).

**Segunda familia refutada:** C = menor valor para el que ningún cierre entre END y la mecha (incluyéndola o no) atraviesa la nube media o la lenta (borde cercano, centro o lejano). Da, por ejemplo, 26,8–42,8 frente a 49,4 en el caso 3, y no acierta ningún caso.

**Decisión (16-oct):** tras unas 80 variantes sin acierto, se deja de buscar el ajuste de Auto por prueba y error. Auto aportó tres hechos firmes: la semilla en el extremo de END, un Character continuo y la caja que el indicador asocia a cada ajuste. Se vuelve al objetivo, el C de Manual, con M1 y con la comprobación de la predicción (a) en modo Manual.

### Resultado M1 y control de la caja Auto (17-oct)

Exportaciones de Luna, commit 032bc72, en `manual/`. C del Lite verificado con `tools/invertir_C_csv.py`, exacto y constante tras la publicación:

| Ventana | Sesión | C Lite | Character Tree | Predicción registrada | Resultado |
|---|---|---:|---|---|---|
| 12-oct 14:00–14:22 | RTH | 83 | 82,92–83,03 | igual que ETH (83) | **se cumple** |
| 12-oct 13:31–13:53 | RTH | 89 | 88,88–89,03 | igual que ETH | **se cumple** |
| 12-oct 13:31–13:53 | ETH | 89 | 88,88–89,03 | — | — |
| 16-oct 16:40–17:00 | ETH | 88 | 87,98–88,19 | (a): ≈ 49,4, el C de Auto con esa caja | **refutada** |

**Conclusiones.**

1. **C no depende de las velas anteriores a START.** La ventana 13:31–13:53 tiene en RTH una sola vela de la sesión antes de START (el resto es la sesión regular del viernes) y en ETH toda la madrugada, y da 89 en ambas. La premisa del evaluador, C = f(velas de START a END), queda respaldada.
2. **La caja que dibuja Auto no «lleva» el Character de Auto en sentido Manual** (88 frente a 49,4).
3. **Dos casos largos nuevos, nunca usados para construir reglas:** 16:40–17:00 (n = 21, C = 88) y 13:31–13:53 (n = 23, C = 89). Ninguna regla del evaluador los acierta (predicciones 66–125 y 72–83).

**Hipótesis H_interno refutada** (`prueba_ajuste_interno.py`, definida antes de ejecutarla): «el Character del rango es el C con el que la nube sembrada en el extremo de START toca la mecha de END». 0/123 en 18 variantes; en 68 casos no existe solución.

**Exploración sin resultado:** entre los 21 casos de 1 m con n = 21, ninguna propiedad simple de la ventana (rango, recorrido, eficiencia, posición de END, posición de los extremos, volumen, dispersión) se correlaciona con C por encima de |r| = 0,40. Cuando se añade una vela al inicio, C cambia en 22 de 34 casos aunque esa vela no sea un nuevo extremo.

### M6. Escalera de resoluciones (predicciones registradas el 17-oct)

**Lógica.** La misma ventana con distintas «Data resolution». Con pocas velas por fuente el régimen es corto y la fórmula exacta; con más velas, el mismo tramo pasa al régimen largo. Así se ve qué añade el régimen largo sobre la fórmula corta con los mismos precios y el mismo tiempo.

Configuración: 16-oct, NQ1!, gráfico 1 m, ETH, UTC, B-ADJ desactivado, modo Manual. Lite y Character Tree con la misma ventana; se cambia **solo** la resolución de la fuente en ambos.

| Archivo | Ventana | Resolución | n | Predicción |
|---|---|---|---:|---|
| `RES_1016_1645_1700_1m.csv` | 16:45–17:00 | 1 minuto | 16 | 52,4590 (fórmula corta, exacta) |
| `RES_1016_1645_1700_30s.csv` | 16:45–17:00 | 30 segundos | 31 | entero (régimen largo) |
| `RES_1016_1645_1700_15s.csv` | 16:45–17:00 | 15 segundos | 61 | entero |
| `RES_1016_1645_1700_5s.csv` | 16:45–17:00 | 5 segundos | 181 | entero |
| `RES_1016_1645_1700_1s.csv` | 16:45–17:00 | 1 segundo | 901 | entero |
| `RES_1016_1640_1700_30s.csv` | 16:40–17:00 | 30 segundos | 41 | entero (a 1 m vale 88) |
| `RES_1016_1640_1700_15s.csv` | 16:40–17:00 | 15 segundos | 81 | entero |

**Resultado M6 (17-oct; exportaciones de Luna, commit 8780bf4).** El CSV solo trae valores por vela de 1 m, pero con las velas de la fuente descargadas del conector (`NQ1_30s_…`, `NQ1_15s_…`, `NQ1_5s_…`, `NQ1_1s_…` en esta carpeta), [`tools/invertir_C_subfuente.py`](../../tools/invertir_C_subfuente.py) simula las seis EMA con las subvelas reales y recupera C. **Residuo 0,000000 pt** en las 6 curvas en todos los casos, siempre con semilla en el máximo de END:

| Ventana | 1 m | 30 s | 15 s | 5 s | 1 s |
|---|---:|---:|---:|---:|---:|
| 16:45–17:00 | 60 | 47 | 40 | 82 | 73 |
| 16:40–17:00 | 88 | 86 | 85 | — | — |

- **Corrección:** la «predicción» 52,4590 para 1 m era errónea por descuido mío: la fórmula corta lleva el mínimo $\max(\Delta t, \dots)$ y da 60, justo lo medido. **La fórmula corta se confirma.**
- **16:40–17:00 es casi estable** con la resolución (88, 86, 85). **16:45–17:00 salta** (47, 40, 82, 73), mientras que $T/18.3$ daría 49–51 en todas. Es lo propio de una **elección discreta** que cambia con la granularidad, no de una función suave de la duración.
- Los 9 casos se añadieron al evaluador como conjunto `nuevos`. **Ninguna regla existente acierta ninguno de los 8 largos.**
- **Familia refutada:** C = fórmula de duración aplicada al tramo desde el extremo de la ventana (máximo, mínimo o según dirección; primera o última aparición) hasta END, en la resolución de la fuente. Como mucho 2/129.

### M7. Barrido de START en la zona 16:30–17:00

**Configuración:** 16-oct, NQ1!, gráfico 1 m, fuente 1 minuto, ETH, UTC, B-ADJ desactivado, modo Manual. Lite y Character Tree con el mismo START y END; END fijo a las 17:00. Se exportaron los 15 START de 16:30 a 16:44, de minuto en minuto, en `manual/SWP_1016_<START>_1700.csv`.

**Resultado (16-oct):** los 15 CSV contienen 300 velas del gráfico y 239 velas con curvas publicadas en Lite y Character Tree. `tools/invertir_C_csv.py` recupera un C constante dentro de cada ventana:

| START | Velas inclusivas | C Lite | Archivo |
|---|---:|---:|---|
| 16:30 | 31 | 108 | [`SWP_1016_1630_1700.csv`](../../manual/SWP_1016_1630_1700.csv) |
| 16:31 | 30 | 108 | [`SWP_1016_1631_1700.csv`](../../manual/SWP_1016_1631_1700.csv) |
| 16:32 | 29 | 108 | [`SWP_1016_1632_1700.csv`](../../manual/SWP_1016_1632_1700.csv) |
| 16:33 | 28 | 108 | [`SWP_1016_1633_1700.csv`](../../manual/SWP_1016_1633_1700.csv) |
| 16:34 | 27 | 108 | [`SWP_1016_1634_1700.csv`](../../manual/SWP_1016_1634_1700.csv) |
| 16:35 | 26 | 88 | [`SWP_1016_1635_1700.csv`](../../manual/SWP_1016_1635_1700.csv) |
| 16:36 | 25 | 93 | [`SWP_1016_1636_1700.csv`](../../manual/SWP_1016_1636_1700.csv) |
| 16:37 | 24 | 82 | [`SWP_1016_1637_1700.csv`](../../manual/SWP_1016_1637_1700.csv) |
| 16:38 | 23 | 88 | [`SWP_1016_1638_1700.csv`](../../manual/SWP_1016_1638_1700.csv) |
| 16:39 | 22 | 88 | [`SWP_1016_1639_1700.csv`](../../manual/SWP_1016_1639_1700.csv) |
| 16:40 | 21 | 88 | [`SWP_1016_1640_1700.csv`](../../manual/SWP_1016_1640_1700.csv) |
| 16:41 | 20 | 65,5738 | [`SWP_1016_1641_1700.csv`](../../manual/SWP_1016_1641_1700.csv) |
| 16:42 | 19 | 62,2951 | [`SWP_1016_1642_1700.csv`](../../manual/SWP_1016_1642_1700.csv) |
| 16:43 | 18 | 60 | [`SWP_1016_1643_1700.csv`](../../manual/SWP_1016_1643_1700.csv) |
| 16:44 | 17 | 60 | [`SWP_1016_1644_1700.csv`](../../manual/SWP_1016_1644_1700.csv) |

**Conclusión:** el cambio de régimen queda entre 16:40 (21 velas inclusivas, C = 88) y 16:41 (20 velas, C = 65,5738). Desde 16:41, C coincide con la fórmula corta `max(60, n × 60 × 10 / 183)`: en 16:42 da 62,2951 y desde 16:43 queda en el mínimo de 60. En el régimen largo C también cambia con START y no es monótono (por ejemplo, 108 a 16:34, 88 a 16:35 y vuelve a 93 a 16:36); el umbral corto/largo se identifica por la coincidencia con la fórmula y el paso de 21 a 20 velas, no por cualquier salto aislado.

**Verificación M7 (17-oct, commit 040b43b):** los 15 C de Luna coinciden con `tools/invertir_C_csv.py` (exactos y constantes tras la publicación). Las capturas de los ajustes del Lite están en [`manual/ajustes_Lite_v1_3_2026-10-17/`](../../manual/ajustes_Lite_v1_3_2026-10-17/README.md): sus únicas entradas que pueden afectar a C son START, END y la resolución de la fuente.

**Lectura de M7.** Con START de 16:30 a 16:34, el máximo de la caja cambia (16:30, 16:32, 16:33, 16:39) y C sigue en 108. Con 16:34 y 16:35 la caja es la misma (máximo a las 16:39, mínimo a las 16:57, misma posición de END) y C pasa de 108 a 88. Ni los extremos ni la posición de END determinan C. La vela de 16:34 es la vecina izquierda del mínimo de 16:35, lo que sugería que C depende solo de las velas desde el primer pivote confirmado.

**H_pivote refutada** (`prueba_pivote_inicial.py`, prueba de colisión sin ajuste): entre ventanas con el mismo END y las mismas velas desde el primer pivote (fuerza 1, 2 o 3; alto, bajo o cualquiera), C difiere en la mayoría de grupos, entre 12 y 17 incoherentes de 16 a 22. Las velas anteriores al primer pivote sí influyen; la meseta de M7 es particular de ese caso. Los 10 casos largos de M7 se añadieron al conjunto `nuevos` del evaluador.

**Búsqueda sistemática de optimización (17-oct, `busqueda_optimizacion.py`):** C como entero de 1 a 400 que cumple u optimiza un criterio con las EMA del indicador corriendo dentro de la caja. Criterios: valor de la línea en END igual al cierre, extremo, extremo opuesto, apertura de END o centro de la caja; equilibrio de cierres por encima y por debajo; menor C sin cierres o sin mechas que atraviesen; mínimo error cuadrático; máximo de toques. Con 5 semillas y 8 líneas suman 400 variantes, solo sobre entrenamiento (maestro + 2 m, 121 casos largos). **La mejor acierta 2/121.** Criterio de éxito fijado antes de ejecutar: ≥ 50 %. Familia descartada en esas formas.

### M8. Metadatos del Lite y de Character Tree por DevTools (pendiente)

Ejecutar [`tools/devtools_volcar_metainfo.js`](../../tools/devtools_volcar_metainfo.js) en la consola con ambos indicadores cargados y guardar el JSON en `manual/metainfo_<fecha>.json`. Objetivo: entradas ocultas (`isHidden`), plots ocultos (un posible plot de C), tooltips y `pineFeatures`. El script omite el ILScript cifrado; no se intenta descifrarlo.

### M9. Treinta ventanas independientes (predicciones registradas el 17-oct)

**Por qué.** Los 147 casos largos medidos hasta ahora forman solo unos 14 bloques independientes de ventanas solapadas: la muestra efectiva es pequeña y está concentrada en pocas zonas de precio. Los valores de C «repetidos» en ventanas distintas vienen casi siempre del mismo bloque (son mesetas), no de un conjunto fijo de valores.

**Diseño.** [`generar_M9.py`](generar_M9.py) sortea, con semilla 20261017, 30 ventanas de 1 m: días 12, 13, 15 y 16 de oct, sesión ETH, n entre 21 y 45, sin cruzar el corte diario y sin solaparse (margen de 5 min) entre sí ni con nada ya medido. Las predicciones de todas las reglas del evaluador están en [`M9_ventanas.json`](M9_ventanas.json). Verificación: [`verificar_M9.py`](verificar_M9.py).

Configuración: NQ1!, gráfico 1 m, ETH, UTC, B-ADJ desactivado. Lite en Manual con «Source data resolution» de 1 minute. Un CSV por ventana, con el nombre del campo `archivo` (p. ej. `manual/M9_1012_0035_0105.csv`). Character Tree no es necesario.

### Lectura rápida alternativa con Character Tree

En los 74 casos del maestro medidos con ambos indicadores, el C de Lite cae siempre dentro del intervalo de Character Tree. Por eso, para M1 bastaría leer en Character Tree la etiqueta **«C/3 …s»** (perfil B, modo Manual, resolución de datos 1 minuto, «Show EMA timeframe labels» activado), que aparece al publicarse las curvas: $C = 3 \times$ el valor de la etiqueta, con error de ±0,015 s, suficiente para identificar un C entero. Si alguna ventana da en RTH un C distinto del de ETH, se exporta además el CSV de Lite de esa ventana como evidencia primaria. **Actualización:** la instancia CT6561USR del usuario no tiene la opción de etiquetas, así que M1 se mide también por exportación CSV.

Seven Cloud (EMA 78/84 en temporalidades fijas, sin anclas) y Manual Anchored CCII (detector CSD/IDM, sin EMA) no calculan C y no intervienen en este experimento.

## Criterio de decisión

- **M1 sin diferencias en las 7 ventanas:** la historia anterior a START no interviene (al menos más allá de unas pocas velas). Siguiente paso: barrido denso START/END a 1 m con fuente 1 m para estudiar las transiciones.
- **M1 con diferencias:** C depende de la historia previa. Siguiente paso: medir cuántas velas previas intervienen, moviendo M1-6 a distintas distancias de la apertura de RTH.
- **M2 distinto de 128:** el indicador usa datos posteriores; cambia el planteamiento por completo.
