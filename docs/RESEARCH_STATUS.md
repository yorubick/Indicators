# Estado de la investigación — 16-oct-2026

> **Revisión crítica del 16-oct-2026.** Esta versión sustituye a la anterior. Varias afirmaciones previas («operador completo 21/21», «ecuación universal $T/18.3$», «celosía de 9 s / 27 s», «autonomía total del modo Auto») no resisten la comprobación contra el dataset maestro ni contra el propio código. Las cifras de esta página se recalcularon sobre `master_all_C_cases.json`; el detalle está en la sección [Revisión de afirmaciones previas](#revisión-de-afirmaciones-previas).

## Resumen en una frase

Las **curvas** están resueltas cuando se conoce C, y el **régimen corto** (menos de 21 barras de la fuente) tiene una fórmula exacta. En el **régimen largo**, la regla que elige C sigue **sin descubrir**: ninguna regla propuesta ha acertado casos que no se usaran para construirla.

## Resultados sólidos (reproducibles y con datos primarios)

| # | Resultado | Evidencia | Alcance y salvedades |
|---|---|---|---|
| R1 | **Motor de curvas.** Con C fijado, las seis curvas se reproducen con EMA estándar, $\alpha = 2/(b_0 C/\Delta t + 1)$ y $b_0 \in \{24,\ 89/3,\ 8,\ 89/9,\ 8/3,\ 89/27\}$. | Residuo < 0,005 pt en las 13 ventanas de [`experimentos/15s_serie_1903/`](../experimentos/15s_serie_1903/README.md); 0,00 pt en el caso 2 m del 15-oct. | Validado solo en `NQ1!`, sesión ETH y las ventanas comprobadas. |
| R2 | **Régimen corto.** Si $n < 21$, con $n$ = número **inclusivo** de barras de la fuente ($n = (END-START)/\Delta t + 1$), $C = \max(\Delta t,\ n\,\Delta t \cdot 10/183)$, sin redondeo. | 35/35 casos Lite del maestro con error máximo $7{,}6\times10^{-12}$ s. Hay además controles en 2 m del 15-oct (ver [informe n=21](INFORME_VALIDACION_FRONTERA_21_Y_REGIMENES.md), sección D). | Todos los casos son de `NQ1!`. Con $n$ **no** inclusivo la fórmula falla; ver [`ANALISIS_K_145.md`](ANALISIS_K_145.md). |
| R3 | **C es entero en el régimen largo.** Si $n \ge 21$, el C de Lite es un entero en segundos. | 110/110 casos largos del maestro (residuo < $10^{-10}$). | Dice cómo se presenta C, no cómo se elige. |
| R4 | **La resolución de la fuente cambia C.** Con las mismas anclas, $C_{15\,s} \ne C_{1\,m}$. | 13 inversiones de la serie 19:03, con 6 curvas cada una. | No dice qué variables de la fuente lo determinan. |
| R5 | **Seven Cloud, cierres históricos.** Una instancia recién añadida desde el código guardado coincide con el estudio oficial en 392 barras × 32 curvas (12.544 valores, 0 discrepancias). | [`SEVEN_CLOUD_AUDIT_2026-10-16.md`](SEVEN_CLOUD_AUDIT_2026-10-16.md), `python tools/audit_seven_cloud_exports.py`. | La instancia ya cargada en el gráfico no coincidió, y la paridad dentro de la vela en formación (20:32–20:34 UTC) sigue abierta. |

## Evaluador

Toda regla de C se mide con [`tools/evaluador_C.py`](EVALUADOR_C.md): validación cruzada por grupo, comparación con el azar y predicciones registradas antes de medir. Marcador al 16-oct-2026: ninguna regla predice el régimen largo. El modo Auto del clon Pine acierta 1/110 en el maestro y 0/11 en los casos de 2 m, por debajo de la línea base `round(T/18.3)`, que acierta 8/110.

## Experimento en curso

[`EXP-20261016-dependencias`](../experimentos/EXP-20261016-dependencias/README.md) busca qué datos usa el indicador para fijar C, antes de seguir probando fórmulas. Resultados sin medición nueva: C es constante tras publicarse (más de 2.200 velas); no depende de forma simple del tiempo hasta la ruptura; y la geometría de la caja no lo determina. Pendientes: sesión ETH frente a RTH (historia previa), Replay en la primera publicación (datos futuros) y captura de los ajustes del indicador.

## Lo que sigue abierto

1. **La regla del régimen largo ($n \ge 21$).** Es el objetivo principal y está sin resolver.
2. Qué variables alimentan esa regla: anclas, OHLCV de la caja, la barra END, estado persistente u otras.
3. La equivalencia completa entre Character Tree y Lite, sobre todo en huecos de sesión y cambios de régimen.
4. Si los regímenes corto y largo cuentan $T$ igual. El corto exige $n$ inclusivo, pero la mejor línea base del largo usa $T$ transcurrido (ver la tabla de abajo). Esa diferencia puede ser una pista.
5. La paridad dentro de la vela en formación en Seven Cloud.

## Revisión de afirmaciones previas

Cifras recalculadas sobre los 110 casos largos Lite del maestro. $\Delta C = C - \operatorname{round}(T/18.3)$.

| Afirmación anterior | Comprobación | Veredicto |
|---|---|---|
| «Operador completo C: 21/21 casos exactos (100 %)» (`operador_completo_C.py`) | 18 de los 21 resultados están **escritos a mano** en el código según la hora de START o END (`if e_str == "19:32": return 106`, etc.). Solo 3 salen de una fórmula. Las variables de vela que el script calcula (`cl_pos`, `last_piv_h`) no se usan para decidir. | **Retirada.** Es una tabla de consulta: el 100 % está garantizado y no demuestra nada. |
| «Ecuación analítica universal $C = \operatorname{round}(T/18.3)$» | Aciertos exactos: **3/110** con $T$ inclusivo y **8/110** con $T$ transcurrido. La mediana del error absoluto es 7–9 s. En la misma serie de END 19:33 falla: START 19:18 da 39 (la fórmula, 49) y START 19:15 da 77 (la fórmula, 59). | **Retirada.** Sirve como centro aproximado, no como ley. |
| «Celosía de potencias de 3: saltos de 9 s y 27 s» | $\Delta C$ múltiplo de 9: 7/110 o 16/110, frente a 12,2 esperados por azar. A ≤ 2 s de un múltiplo de 9: 62/110 o 68/110, frente a 61,1 por azar ($5/9$). Múltiplo de 3: 31 o 35, frente a 36,7 por azar. | **Refutada.** Los datos no se distinguen del azar. El «53,1 %» del benchmark del 15-oct está, de hecho, al nivel del azar. |
| «Saltos cuánticos» y «bifurcaciones» ($66-27=39$, $77=66+11$, …) | Relaciones aritméticas buscadas después de ver los valores. Con enteros entre 15 y 125 siempre aparecen. | **Interpretación sin poder predictivo.** No usar como evidencia. |
| «Frontera universal $n=21$: $C=125$ s» (comentario del clon Pine v1.3) | Hay 22 casos del maestro con $n=21$, con C entre 50 y 87 s en fuente 1 m, 16 s en 15 s y 137 s en 2 m. | **Refutada.** |
| «Autonomía total del modo Auto, residuo 0,00 pt» (informe n=21, sección F) | Es un solo caso (2 m, 14:30–15:16), y la corrección «+33 s» de la regla se calibró para ese mismo caso. | **Ajuste dentro de la muestra**, no validación. |
| «Predicción ciega» de START 19:28 → 16 s y de START 19:30 → 15 s | La predicción se registró en git unos minutos antes del resultado, lo cual es correcto. Pero 19:30–19:33 es régimen corto (piso de R2), y 19:28 usa $T$ transcurrido en vez del inclusivo de R2 (que daría 17). | Aciertos válidos pero de bajo valor informativo. No confirman una ley universal. |
| Control 19:36 → predicción $C = 87$ | La lectura oficial en 19:37 salió vacía (`∅`) porque no hubo ruptura del high de END; ver [informe](../experimentos/15s_serie_1903/CONTROL_1936_EVAL_1937.md). | **Sin evaluar.** La predicción no llegó a probarse. |

## Otros resultados de contexto

- `master_all_C_cases.json` registra 179 selecciones únicas: 145 con C Lite medido y 34 solo de Character, que no deben presentarse como C Lite medidos. **Ningún caso** está marcado como ciego o prospectivo (`blind_or_prospective = false` en los 145).
- La revisión de v4 registra 96/112 casos exactos con la tolerancia estricta de su informe, pero cinco controles de 15 s fallan. Lee `reports/GEMINI_V4_REVISION.md` para definiciones y salvedades. v4 no es una regla prospectiva validada.
- Las pruebas de agregación y timeframe no aíslan una causa temporal; ver `reports/PAQUETE_PARA_GEMINI.md` y los JSON de barrido asociados.
- El adjunto [`imports/codex/2026-10-14_telemetry_paste.txt`](../imports/codex/2026-10-14_telemetry_paste.txt) es una tabla pegada de una conversación. Sirve como pista, no como sustituto de los CSV fuente. Un patrón «armónico» o «pico/meseta» no demuestra un mecanismo hasta que prediga casos nuevos.

## Cómo continuar sin repetir errores

1. **Separar datos de entrenamiento y de control antes de mirar.** Toda regla nueva se construye con un subconjunto y se evalúa con casos que no participaron en su diseño, registrados en git *antes* de leer el valor oficial.
2. **Prohibido codificar casos por su hora o identificador** en una regla que se presente como general. Las entradas permitidas son las que el indicador oficial puede ver: OHLCV de la fuente, anclas, $\Delta t$ y estado previo.
3. **Comparar siempre con el azar y con una línea base simple**, como $\operatorname{round}(T/18.3)$ o la mediana por $n$. Una regla que no mejora a la línea base en los controles no aporta.
4. Antes de medir, leer `reports/MODELOS_REFUTADOS_PARA_GEMINI.md`, `reports/GEMINI_V4_REVISION.md` y `reports/COMO_CONTINUAR_MANUALMENTE.md`, y seguir [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Convenciones

- **Medido**: lectura primaria en un archivo exportado o en una captura verificable, con contexto suficiente.
- **Ajustado/inferido**: C estimado ajustando las curvas. Registrar método, tolerancia y residuo.
- **Predicción**: valor escrito y versionado antes de consultar el control.
- **Hipótesis**: interpretación que aún no han discriminado controles independientes.
- **Retirada/refutada**: afirmación previa que no superó la comprobación. Se conserva el documento original, con una nota de revisión al inicio.

## Registro de controles 15 s (END 19:33, evaluación 19:34)

C invertido con residuo < 0,005 pt en las seis curvas. Los informes originales conservan las interpretaciones de su autor; esta tabla se limita a los valores medidos.

| START | $n$ inclusivo | C medido | $\operatorname{round}(T/18.3)$, T transcurrido | Informe |
|---|---:|---:|---:|---|
| 19:03 | 121 | 87 | 98 | [serie 19:03](../experimentos/15s_serie_1903/README.md) |
| 19:08 | 101 | 70 | 82 | [CONTROL_1908](../experimentos/15s_serie_1903/CONTROL_1908_1933_EVAL_1934.md) |
| 19:10 | 93 | 66 | 75 | [CONTROL_1910](../experimentos/15s_serie_1903/CONTROL_1910_1933_EVAL_1934.md) |
| 19:13 | 81 | 66 | 66 | [CONTROL_1913](../experimentos/15s_serie_1903/CONTROL_1913_1933_EVAL_1934.md) |
| 19:15 | 73 | 77 | 59 | [CONTROL_1915](../experimentos/15s_serie_1903/CONTROL_1915_1933_EVAL_1934.md) |
| 19:18 | 61 | 39 | 49 | [CONTROL_1918](../experimentos/15s_serie_1903/CONTROL_1918_1933_EVAL_1934.md) |
| 19:23 | 41 | 33 | 33 | [CONTROL_1923](../experimentos/15s_serie_1903/CONTROL_1923_1933_EVAL_1934.md) |
| 19:28 | 21 | 16 | 16 | [CONTROL_1928](../experimentos/15s_serie_1903/CONTROL_1928_1933_EVAL_1934.md) |
| 19:30 | 13 | 15 | (corto: piso 15) | [CONTROL_1930](../experimentos/15s_serie_1903/CONTROL_1930_1933_EVAL_1934.md) |

Lo que muestra esta tabla: C **no es monótono** con START. Entre 19:18 y 19:15 sube de 39 a 77 aunque la ventana solo se alarga 3 minutos. Eso sugiere que C depende del **contenido de la caja** y no solo de su duración; es la línea más prometedora para la siguiente fase.
