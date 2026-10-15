# Informe independiente: modelo C de PoiSzn Lite / Character Tree

**Fecha:** 14 de octubre de 2026  
**Datos:** `master_all_C_cases.json`, el barrido END de 17 posiciones y el control 15s/1m/2m.  
**Hash SHA-256 del maestro usado:** `ef9533acdce3e1c2c2db3c72caee5059a2957f7dee4c60e725f6dcf56ccc9c05`.

## Resultado

No encontré una ley matemática unificada que explique los 145 valores Lite medidos. Encontré una relación empírica exacta para los casos observados con menos de 21 velas. Una candidata explícita para el régimen largo, ajustada sin precio absoluto y sin condiciones por caso, falla una partición temporal reservada y el barrido de 15 s. Por eso no la presento como el generador de C.

La validación adicional por bloques de cobertura temporal disjuntos también falla: al dejar fuera el episodio que contiene las 39 mediciones Lite de 15 s, la forma común más simple `C=Δq(n)` obtiene MAE `17.2490` sobre 84 casos y no predice dentro de ±1 más que 3. Esta separación evita que ventanas contiguas del mismo episodio se filtren entre ajuste y prueba; sigue siendo retrospectiva porque todas las etiquetas del maestro ya eran conocidas.

El dato que falta no se puede suplir con más ajuste sobre las mismas etiquetas: hace falta una predicción congelada antes de medir una serie o episodio nuevo. El paquete contiene mediciones ya conocidas y ventanas muy solapadas; no permite identificar de forma única el operador original.

Controles complementarios fuera del maestro ya establecen dos restricciones: para `n=21..40` a 1 s, C alterna entre ≈1 y ≈2, y el cruce START/END da una diferencia de diferencias ≈−1; además, `n=27→28` mide `1→1` donde `round(n/18.3)` predijo `1→2`. Una prueba preregistrada nueva en 1 m confirma invariancia de C al duplicar los precios en un caso: OHLC y canales Lite escalan exactamente ×2, volumen permanece igual y C permanece en 50. La predicción alternativa 77 queda refutada por 27 puntos. Es una restricción de simetría adicional, no el operador completo.

## Datos y control de calidad

El script vuelve a validar 179 casos únicos, 145 `C_Lite` decimales medidos y 34 casos `Character-only`, con OHLCV completo y separación temporal uniforme. Para los 34 `Character-only` se evalúa compatibilidad con el intervalo capturado; no se les inventa un residuo Lite decimal.

La revisión de metadatos confirma que los 179 casos son del mismo símbolo (`CME_MINI:NQ1!`), sesión ETH, modo Manual, perfil B, UTC y contrato sin ajuste; `source_seconds` coincide con la resolución del gráfico. La cobertura es 15 s: 57 casos, 30 s: 2, 60 s: 114 y 120 s: 6. Esto controla esos posibles confusores dentro del paquete, pero limita la inferencia a ese símbolo, perfil y sesión; el script guarda estos conteos en `input_validation` del JSON.

El barrido se trata como una secuencia de 17 ventanas inclusivas con una vela nueva por paso. Los valores Character del archivo no se utilizan para representar los 17 END: Character permaneció fijo en 19:20 durante ese barrido. La comparación temporal 15 s / 1 m / 2 m también cambia el OHLC agregado, el número de barras y la cobertura de END, de modo que no aísla un efecto puro de temporalidad.

Como control de la entrada, el script agrupó arrays OHLCV exactamente idénticos (incluidos timestamps y volumen) aunque START/END solicitados fueran distintos. Halló dos grupos: cuatro selecciones de 60 s con 26 velas efectivas y tres selecciones de 15 s con 103 velas efectivas. En cada grupo hay una medición Lite y los intervalos Character de las selecciones repetidas contienen esa misma C (`62` y `67`, respectivamente). Esto apoya que en esos controles manda la secuencia efectiva de velas, no el ancla solicitada dentro de la misma vela. Como solo hay una lectura decimal Lite por grupo, no cuenta como cuatro ni tres réplicas decimales independientes. El detalle está en `identical_effective_input_audit` del JSON de resultados.

## Relación empírica en el régimen corto

Sean `n` el número de velas inclusivas y `Δ` el intervalo nativo en segundos (`source_seconds`). La candidata corta es

\[
\widehat C_{<21}(n,\Delta)=\Delta\max\left(1,\frac{10n}{183}\right),\qquad n<21.
\]

En el maestro reproduce **35/35** valores Lite de `n<21`; el mayor residuo absoluto `C_hat - C_Lite` es `7.631228982063476e-12`. Los casos observados con `n≤18` tienen `C=Δ`; los de `n=19` y `n=20` tienen `C/(nΔ)=10/183` dentro de la precisión de captura.

Esto es una compresión exacta de las etiquetas cortas, no una constante física derivada: `10/183` no tiene justificación independiente en el paquete. No la elevo a ley descubierta ni la extiendo a `n≥21`. En `n=21` los 20 casos de 60 s ya abarcan `C=50..87` y 11 enteros distintos; para 15 s se midió 16 y para 120 s, 137. Una prolongación del mismo factor corto no resuelve esa dispersión.

### Secuencia complementaria nativa de 1 s, fuera del maestro

Verifiqué las exportaciones manuales nativas de 1 s de una misma ancla (`14:04:00 UTC`) para `n=20..40`. En cada conteo hay dos exportaciones concordantes en OHLCV y las seis curvas Lite; entre las seis estimaciones de `C`, la máxima dispersión fue `7.25197679685×10⁻¹³`, el RMSE EMA máximo `2.47033581182×10⁻¹²`, el error máximo de reconstrucción tras la primera ruptura `5.82076609135×10⁻¹¹` y hubo cero diferencias de visibilidad. Las ventanas consecutivas son prefijos OHLCV exactos. Estas mediciones no se añadieron al maestro de 179 casos ni cuentan como episodio independiente.

| n | C Lite reconstruido | Predicción preregistrada | Residuo `C−Ĉ` |
|---:|---:|---:|---:|
| 20 | 1.092896174863442 | 1.092896174863388 | `+5.44×10⁻¹⁴` |
| 21 | 1.000000000000075 | 1.000000000000000 | `+7.48×10⁻¹⁴` |
| 22–24, 26–29 | `1` a ±`2.8×10⁻¹⁴` | 1 en el preregistro complementario | máximo absoluto `2.8×10⁻¹⁴` (7/7 dentro de `10⁻⁶`) |
| 25, 30 | `1` a ±`1.7×10⁻¹⁴` | 1 en el preregistro inicial | ambas dentro de `10⁻⁶` |
| 31–32 | `1` a ±`1.5×10⁻¹⁴` | barrido adaptativo, sin predicción de nivel punto a punto | no evaluable |
| 33 | 1.999999999999842 | sin predicción de nivel punto a punto | no evaluable |
| 34–35 | `1` a ±`3.1×10⁻¹⁴` | barrido adaptativo, sin predicción punto a punto | no evaluable |
| 36–39 | `2` a ±`1.0×10⁻¹³` | barrido adaptativo, sin predicción punto a punto | no evaluable |
| 40 | 1.999999999999999 | 1 en el preregistro inicial | `+0.999999999999999` (fallo) |

El preregistro inicial acertó `n=25,30` y falló `n=40`; un preregistro posterior acertó las siete cuentas omitidas `n=22,23,24,26,27,28,29`. Los archivos de `n=31..39` quedaron después del fallo de `n=40`; no los trato como predicciones de nivel independientes. El par aceptado de `n=33` se volvió a guardar después de `n=39` (mtime UTC 14:51:54 frente a 14:46:31). La captura `pending` y las dos exportaciones actuales de `n=33` coinciden en todas sus celdas OHLCV/curvas comunes, y sus medias `C` difieren solo `9.26×10⁻¹⁴`; el último mtime no conserva el orden original de la primera pasada adaptativa. La secuencia `n=21..40` contiene catorce niveles `C≈1` y seis `C≈2`: `1` en `21..32`, `2` en `33`, `1` en `34–35` y `2` en `36..40`.

Los tres cambios de nivel (`32→33`, `33→34`, `35→36`) ocurren sin que la vela entrante haga un nuevo máximo o mínimo global. Además, hay nuevos mínimos en `n=30..32` sin cambio de `C`; en esta secuencia el evento de extremo global no es necesario ni suficiente para explicar las transiciones. Las razones de volumen de las tres velas de cambio respecto de la media previa son aproximadamente `0.972`, `1.426` y `0.697`; sus posiciones de cierre dentro del rango individual son `0`, `0.9` y `1`. No aparece un disparador escalar común entre esos rasgos. Queda abierta la dependencia de estructura interna o estado del prefijo; estos datos no identifican cuál.

El análisis reproducible `auditar_C_meseta_1s_conteos.py` genera las 21 filas con `C`, predicción disponible, residuo, rasgos de la vela entrante, hashes, errores de ajuste y reconstrucción en `resultado_C_meseta_1s_conteos.json` y `residuos_C_meseta_1s_conteos.csv`.

### Contrastes prospectivos adicionales de START/END a 1 s

Se añadieron dos contrastes preregistrados en el mismo episodio NQ ETH del 14 de octubre; no son episodios independientes ni forman parte de los 179 casos maestros. En el cruce se mantuvo END y se desplazó START un segundo. La matriz completa observada es:

| START UTC | END UTC | n | C observado | Nota |
|---|---|---:|---:|---|
| 14:04:00 | 14:04:32 | 33 | 1.9999999999999283 | control anterior |
| 14:04:01 | 14:04:32 | 32 | 1.0000000000000446 | nuevo |
| 14:04:00 | 14:04:33 | 34 | 1.0000000000000302 | control anterior |
| 14:04:01 | 14:04:33 | 33 | 1.0000000000000564 | nuevo |

Para los dos casos nuevos, las hipótesis congeladas solo por conteo predijeron `1, 2`; las hipótesis solo por END, `2, 1`. Con residuo definido como observado menos predicho, la tabla es:

| Caso nuevo | Predicción por conteo | Residuo | Predicción por END | Residuo |
|---|---:|---:|---:|---:|
| START 14:04:01, END 14:04:32, n=32 | 1 | `+4.46×10⁻¹⁴` | 2 | `−0.999999999999955` |
| START 14:04:01, END 14:04:33, n=33 | 2 | `−0.999999999999944` | 1 | `+5.64×10⁻¹⁴` |

Cada explicación acierta 1/2 en los datos nuevos y ninguna cubre las cuatro celdas observadas. La diferencia de diferencias es `−0.999999999999910`: el efecto de añadir la vela de END depende de START, así que una suma separable `f(START)+g(END)` no explica esta matriz. También hay dos ventanas de 33 velas con iguales máximos y mínimos y la misma primera ruptura posterior, pero C≈2 frente a C≈1. Es evidencia de interacción de límites o de información de trayectoria; por sí sola no selecciona una arquitectura interna.

Un segundo contraste preregistró `C=round(n/18.3)` para START 14:02:00. Midió `C≈1` tanto en `n=27` como en `n=28`; por tanto, la predicción 1→2 falla en el segundo punto. Los residuos observado menos predicho son `+1.53×10⁻¹⁴` y `−0.999999999999979`, respectivamente (1/2 aciertos). No reemplazo retrospectivamente `round` por otro cuantizador. Ambos pares de exportaciones coinciden en OHLCV y las seis curvas Lite en sus celdas compartidas; hay cobertura nativa completa y 600 segundos posteriores. Las seis estimaciones de C discrepan menos de `10⁻⁶`, los RMSE EMA son menores que `10⁻⁸`, la reconstrucción máxima es `3.64×10⁻¹¹` y no hay discrepancias de visibilidad. Los dos rangos 27/28 son prefijos exactos.

Los scripts `analizar_C_1s_cruce_START.py` y `analizar_C_1s_1402_n27_n28.py` verifican los controles, predicciones, estabilidad, ajuste de seis curvas y reconstrucción; los datos detallados y residuos están en `C_1s_cruce_START_resultados.json` y `C_1s_1402_n27_n28_resultados.json`. Estos contrastes refutan explicaciones simples por conteo, END o `round(n/18.3)` en sus condiciones, pero no identifican el operador unificado.

### Prueba preregistrada de escala de precio

El preregistro `C_ESCALA_50_PREREGISTRO.json` fija la ventana 2026-10-12 19:02–19:22 UTC a 1 m. El caso base predijo `C=50`; al duplicar precios se congelaron dos salidas rivales: invariancia `C=50` y la predicción de Gemini v4 `C=77`. La ruta original `NQ1!+0` fue normalizada por TradingView y no sirve como identidad sintética. Antes de medir C se registró la alternativa `(NQ1!+NQ1!)/2` en `C_ESCALA_50_IDENTIDAD_ALTERNATIVA.json`.

La alternativa cumple el control: su exportación `b` contiene las 21 velas preregistradas, y en las 2710 filas cerradas comunes con el caso base coinciden exactamente OHLCV y las seis curvas Lite. Las dos capturas de identidad alternativa también coinciden en sus 436 filas compartidas. La captura de retorno a `NQ1!` coincide exactamente con la base en 2710 filas. Los ajustes de seis canales sitúan C entre `49.99999999999829` y `50.00000000000038`; el máximo RMSE EMA es `4.51×10⁻¹²`.

El orden de modificación local respalda la secuencia preregistro→medición: preregistro alternativo 15:13:20 UTC, exportaciones de identidad 15:13:40 y 15:14:05, doble precio 15:14:45 y 15:15:04, y retorno 15:15:26. El auditor conserva esos tiempos junto con los hashes de cada exportación.

Tras aceptar la identidad alternativa, `2*NQ1!` se probó con dos exportaciones estables. En 2710 velas comunes, las 10 840 entradas OHLC son exactamente el doble, los 2710 volúmenes no cambian y las 15 030 celdas visibles de curvas Lite son exactamente el doble, sin discrepancias de visibilidad. El ajuste da `C=49.99999999999934`. Reconstruyendo las 540 velas siguientes desde el extremo de cierre y la primera ruptura común de 2026-10-12 19:26 UTC, el error máximo es `3.64×10⁻¹¹` y hay cero errores de visibilidad.

Las seis lanes están ocultas durante las 21 velas del intervalo seleccionado y aparecen en la primera ruptura común posterior, a las 19:26 UTC. Por eso el ajuste de C se recupera de las trazas visibles y la validación temporal se hace reconstruyendo las 540 velas posteriores a END; no se asignan valores inventados a las celdas ocultas.

| Medición | Predicción congelada | C recuperado | Residuo `C_obs−C_pred` |
|---|---:|---:|---:|
| Base `NQ1!` | 50 | 49.999999999999346 | `−6.536993168992922×10⁻¹³` |
| Identidad `(NQ1!+NQ1!)/2` | 50 | 49.99999999999934 | `−6.608047442568932×10⁻¹³` |
| Doble, invariancia | 50 | 49.99999999999934 | `−6.608047442568932×10⁻¹³` |
| Doble, Gemini v4 | 77 | 49.99999999999934 | `−27.00000000000066` |
| Retorno a `NQ1!` | 50 | 49.999999999999325 | `−6.750155989720952×10⁻¹³` |
| `C_doble−C_base` | 0 | `−7.105427357601002×10⁻¹⁵` | `−7.105427357601002×10⁻¹⁵` |

La simetría medida también se deriva de cómo recuperamos el período EMA. Para una lane con período base `b`, `α=(Y_t−Y_{t−1})/(P_t−Y_{t−1})` y `C=Δ(2/α−1)/b`. Si `P'_t=λP_t` y la salida observada `Y'_t=λY_t`, entonces `α'=α` y por tanto `C'=C`. La prueba verifica este resultado para `λ=2` en 2710 barras compartidas y 15 030 valores visibles de curva.

Esta es evidencia directa, preregistrada y reproducible de invariancia a escala positiva de precio para una ventana 1 m: `f(2O,2H,2L,2Close,V,Δ)=f(O,H,L,Close,V,Δ)` en este caso. No demuestra que la misma simetría rija todas las ventanas/temporalidades y no resuelve la transición corta/larga. `auditar_C_escala_50_completa.py` verifica las transformaciones, pares, ajuste C y recurrencia; los residuos exactos y resultados con hashes están en `residuos_C_escala_50.csv` y `resultado_C_escala_50_completa.json`. La consulta histórica de solo OHLCV queda auditada aparte por `auditar_C_escala_50_ohlcv.py`; esa auditoría solo documenta la ruta `NQ1!+0` normalizada.

### Réplica de escala congelada para 15 s, 1 m y 2 m

Para comprobar la transferencia de esa simetría a ambos regímenes, preregistré el 14 de octubre 15:23:31 UTC tres duplicaciones del conjunto de temporalidades existente. La predicción queda fijada sin refit: `C(2·OHLC,V,Δ)=C_base` en cada caso.

| Intervalo | n | Régimen | C base bloqueado | C del par base actual | C doble preregistrado |
|---:|---:|---|---:|---:|---:|
| 15 s | 81 | largo | 66.99999999999912 | 66.99999999999912 | 66.99999999999912 |
| 60 s | 21 | largo | 76.99999999999851 | 76.99999999999936 | 76.99999999999851 |
| 120 s | 11 | corto | 120.00000000000124 | 120.00000000000124 | 120.00000000000124 |

Los pares base se volvieron a verificar contra OHLCV del maestro y su RMSE EMA máximo queda bajo `2.32×10⁻¹²`. Aún no hay exportaciones dobles para estos tres casos: el auditor deja explícitamente sus predicciones pendientes y no les asigna resultado. Es una sola sesión común, no una réplica de mercado independiente. El protocolo, nombres de exportación y predicciones están en `C_ESCALA_TF_REPLICACION_PREREGISTRO.json`; `auditar_C_escala_multi_tf.py` genera `resultado_C_escala_multi_tf.json` y `residuos_C_escala_multi_tf.csv` cuando se agreguen las capturas.

### Traslación y reflexión de precios en la misma ventana

Dos pruebas adicionales preregistradas en 1 m mantienen la ventana de C=50 y conservan el volumen y los timestamps. La traslación `P'=P+10000` conserva OHLCV exactamente salvo por ese desplazamiento y desplaza las seis curvas en `+10000` con error máximo `2.91×10⁻¹¹`. En 2717 filas comunes, repetición y retorno no tienen discrepancias; la seis-fit recupera C≈50 antes, después y al volver.

La reflexión `P'=70000−P` verifica `O'=70000−O`, `C'=70000−C`, `H'=70000−L`, `L'=70000−H` exactamente en 2721 velas comunes, con volumen idéntico. Las seis curvas reflejan sus canales homólogos con error máximo `5.82×10⁻¹¹` y cero diferencias de visibilidad. La primera ruptura ocurre en el mismo instante, 19:26 UTC, y cambia de alcista a bajista; la semilla de END cambia de `30866.75` a `39133.25`, cuya suma es 70000. Las 540 velas reconstruidas tienen error máximo `3.64×10⁻¹¹` y cero errores de visibilidad.

| Prueba / condición | C recuperado | Residuo `C_obs−50` |
|---|---:|---:|
| Traslación, base fresca | 49.99999999999932 | `−6.821210263296962×10⁻¹³` |
| `P+10000` | 49.99999999999883 | `−1.1723955140041653×10⁻¹²` |
| Traslación, retorno | 49.999999999999325 | `−6.750155989720952×10⁻¹³` |
| Reflexión, base | 49.999999999999325 | `−6.750155989720952×10⁻¹³` |
| `70000−P` | 50.0000000000007 | `+7.034373084024992×10⁻¹³` |
| Reflexión, retorno | 49.99999999999932 | `−6.821210263296962×10⁻¹³` |

En esta ventana, los tres operadores medidos —`2P`, `P+10000` y `70000−P`— dejan C en 50; la reflexión además invierte el sentido de ruptura. Eso debilita Candidatos basados directamente en nivel, amplitud puntual o dirección firmada para este caso y favorece una dependencia de forma relativa, magnitudes simétricas o estructura temporal. La traslación no separa la hipótesis de Gemini v4, que también predijo 50; el contraste discriminante fue `2P`, donde predijo 77. El conjunto sigue siendo una sola ventana y rama C=50, así que no se generaliza a toda la función.

La relación formal que se contrasta es affine-equivariance de las curvas con invarianza del coeficiente EMA. Si `P'_t=aP_t+b` y `Y'_t=aY_t+b`, entonces

\[
\alpha'_t=\frac{Y'_t-Y'_{t-1}}{P'_t-Y'_{t-1}}
=\frac{a(Y_t-Y_{t-1})}{a(P_t-Y_{t-1})}=\alpha_t,
\qquad C'=\Delta(2/\alpha'_t-1)/b_0=C.
\]

Aquí `a=2`, `(a,b)=(1,10000)` y `(a,b)=(-1,70000)` se verificaron directamente sobre los canales; `b_0` denota el período base de cada lane. Los análisis reproducibles son `analizar_C_traslacion50.py` y `analizar_C_reflexion50.py`, con resultados y hashes en `C_traslacion50_resultados.json` y `C_reflexion50_resultados.json`.

### Contraste afín fuera de la rama C=50: preregistro C=62

El preregistro original conserva su texto fechado; la cobertura consecutiva quedó asentada después en `C_SIMETRIA_62_ENMIENDA_VALIDACION.json`, antes de cualquier CSV de esta prueba.

Una segunda enmienda exige cinco capturas de pantalla que documenten el símbolo y la temporalidad; el auditor calcula hashes y mantiene la validación visual pendiente hasta revisar esas imágenes: `C_SIMETRIA_62_ENMIENDA_EVIDENCIA.json`.

Para probar si la simetría sobrevive a otra salida, fijé antes de capturar transformaciones una ventana de 1 m con 26 velas, `START=18:55`, `END=19:20 UTC`, y `C_base=61.99999999999884` del caso `20261012_185500_192000_60s` del maestro. La predicción congelada para `2P`, `P+10000` y `70000−P` es `C=61.99999999999884` en cada una. La hipótesis no usa precio, umbral ni ajuste nuevo.

El registro exige pares de exportaciones nuevas por condición, comprobar OHLCV frente al maestro dentro del intervalo, verificar precio y volumen transformados exactamente, comprobar la covariancia de las seis lanes, ajustar C de forma independiente y reconstruir 540 barras futuras. El archivo `auditar_C_simetria62.py` deja la prueba como `pending_measurements` mientras falte cualquier exportación; ahora faltan los nueve CSV nombrados en `C_SIMETRIA_62_PREREGISTRO.json`, por lo que todavía no hay residuo de transformación que reportar. El estado reproducible está en `resultado_C_simetria62.json`. Como control de referencia previo, las exportaciones existentes `Lite_1855_1920_1m_a/b.csv` coinciden en 1454 filas y las seis estimaciones por lane quedan entre `61.99999999999614` y `62.00000000000135`; no se cuentan como capturas posteriores al registro.

La derivación solo predice invariancia de C si las salidas Lite obedecen la recurrencia EMA ya ajustada: con `P'_t=aP_t+b` y `Y'_t=aY_t+b`, el cociente de diferencias que estima `α` se conserva, así que también se conserva `C=Δ(2/α−1)/b_0`. Incluso si las tres condiciones pasan, el resultado cubrirá una sola ventana C=62 del mismo episodio. No decidirá si volumen entra en el generador, ni identificará la función `f(OHLCV,Δ)`.

### Transferencia sin reentrenar las candidatas de escala

Apliqué a esa secuencia los cuatro modelos `q` congelados en `resultado_C_ley_dimensionless.json`, sin volver a estimar coeficientes. Para `n=21..40`, el mejor modelo continuo (`q` lineal en `n`) tuvo MAE `0.3595`, máximo `0.6896` y `0/20` predicciones a `10⁻⁶` de `C`; los otros tres también obtuvieron `0/20`. Añadí un cuantizador al entero más cercano como diagnóstico posterior —motivado por que las etiquetas largas medidas son enteras, pero no preregistrado ni parte de la ecuación original—; el `q` lineal acierta `15/20` y falla en `n=30–32` y `n=34–35`. `q` constante, logarítmico y con OHLCV normalizado aciertan `14/20` cada uno tras ese mismo cuantizador. En `n=20`, la fórmula corta congelada conserva residuo `Ĉ−C=−5.42×10⁻¹⁴`.

La cuantización tampoco rescata la candidata en el maestro. Sin reajuste, `Ĉ=floor(Δq̂_linear_n+0.5)` da en los 110 Lite largos MAE `13.9636`, máximo `58` y `4/110` exactos dentro de `10⁻⁶`; en el holdout largo temporal son `17.7600`, `58` y `3/75`, con solo `4/75` a ±1. Solo `2/33` intervalos Character largos contienen la predicción redondeada. Un híbrido diagnóstico que conserva la relación corta para `n<21` eleva el total del holdout a `22/94` exactos únicamente porque recupera los 19 casos cortos; sus 75 largos siguen en `3/75`. No es la ley común solicitada.

La regresión larga dimensional directa extrapolada a `Δ=1` da MAE `196.33` en esos 20 puntos; como su entrenamiento solo cubre `Δ=15..120`, registro ese número como extrapolación fuera de dominio, no como holdout pertinente. Los scripts `auditar_transferencia_nativa_1s_C.py` y `auditar_C_q_redondeado_maestro.py` regeneran los residuos exactos en `residuos_C_transferencia_1s.csv` y `residuos_C_q_redondeado_maestro.csv`, respectivamente.

## Candidata explícita para `n≥21` y partición reservada

Para comprobar si una combinación sencilla de trayectoria y volumen transfiere entre resoluciones, fijé este vector de características, sin precio absoluto:

\[
\phi=(\ln n,\ln\Delta,10^4R/P_0,10^4L/P_0,E,B_V,\ln(1+\bar V),H_V),
\]

donde `P0` es el primer cierre, `R=max(high)-min(low)` en la ventana, `L=Σ|close_i-close_(i-1)|`, `E=(close_n-close_1)/L`, `B_V=10^4 Σ[V_i(close_i-open_i)]/(P0ΣV_i)`, y `H_V=Σ(V_i/ΣV_i)^2`. Si `L=0` o `ΣV=0`, el cociente correspondiente se fija en cero.

La ecuación candidata queda completamente determinada por

\[
u_j=(\phi_j-\mu_j)/s_j,\qquad
\widehat C_{\ge21}=\left\lfloor\beta_0+\sum_{j=1}^{8}\beta_j u_j+0.5\right\rfloor.
\]

Se estimó `β` por mínimos cuadrados ordinarios con 35 casos Lite largos del grupo de desarrollo. `μ`, `s` y los coeficientes exactos están en `resultado_C_modelo_independiente.json`; el script conserva el orden de las características y recalcula todos ellos desde el maestro. El redondeo al entero refleja que los 110 valores Lite largos medidos están a menos de `4.7478465603489894e-11` de un entero.

El corte se fijó por tiempo, sin mirar `C`: se reservó el episodio del 12 de octubre que intersecta 18:54–19:30 UTC y todo el 13 de octubre. La regresión se ajustó solo con Lite largos fuera de ese corte. El resultado fue:

| Partición `n≥21` | N | MAE | RMSE | Máximo | Residuo a ≤1 |
|---|---:|---:|---:|---:|---:|
| Ajuste, in-sample | 35 | 4.2571 | 5.8089 | 16 | 12/35 |
| Reservada | 75 | 41.0400 | 46.9820 | 94 | 0/75 |
| Reservada, 15 s | 37 | 57.2432 | 60.2782 | 94 | 0/37 |
| Reservada, 60 s | 38 | 25.2632 | 28.6127 | 48 | 0/38 |

La prueba reservada incluye el barrido y los tres controles de temporalidad. Las predicciones del control fueron `20, 98, 120` frente a Lite observado `67, 77, 120`, con residuos `−47, +21, ≈0`. El único acierto de 2 m usa `n=11` y, por tanto, procede de la fórmula corta; no constituye validación del régimen largo en 2 m.

El corte no es ciego en sentido estricto: los valores ya estaban recopilados y la secuencia del barrido aparece en el propio pedido. Es una evaluación reproducible que mantiene esas etiquetas fuera del ajuste del script, no una validación prospectiva ni una afirmación de ceguera humana.

## Barrido END: qué parece cambiar C

En los 16 pasos, el incremento de C no sigue de forma monotónica el rango de la vela que entra (`ρ` de Spearman `+0.165`), su rango relativo a la ventana (`+0.115`), el volumen (`−0.224`), el cuerpo firmado (`−0.310`) ni la distancia del cierre entrante al cierre START, al punto medio del rango o al VWAP (`+0.038`, `−0.047`, `−0.024`). La muestra es pequeña y esto solo contrasta hipótesis escalares simples; no descarta interacciones ni memoria.

También contrasté cuatro eventos causales simples: nuevo máximo global estricto, nuevo mínimo global estricto, pivote local high de radio 1 confirmado por la vela entrante y pivote local low equivalente. Aparecen en 9/16 transiciones; **C cambia sin ninguno en 6/16** (19:20:15, 19:21:15, 19:22:00, 19:23:00, 19:23:15 y 19:23:30). Ese conjunto no es condición necesaria de cambio. El barrido no identifica si la diferencia restante viene de otra estadística de la vela o de memoria de trayectoria.

| END UTC | C anterior → C actual | ΔC | Rango entrante | Cuerpo | Volumen | Rango / rango ventana | Distancia cierre–START / rango ventana |
|---|---:|---:|---:|---:|---:|---:|---:|
| 19:20:15 | 106 → 79 | −27 | 2.50 | +0.00 | 165 | 0.110 | +0.407 |
| 19:20:30 | 79 → 67 | −12 | 2.75 | +2.25 | 236 | 0.121 | +0.505 |
| 19:20:45 | 67 → 66 | −1 | 2.50 | +2.25 | 145 | 0.102 | +0.561 |
| 19:21:00 | 66 → 115 | +49 | 1.50 | −0.75 | 90 | 0.061 | +0.510 |
| 19:21:15 | 115 → 106 | −9 | 2.00 | +0.00 | 155 | 0.082 | +0.510 |
| 19:21:30 | 106 → 79 | −27 | 2.75 | −2.00 | 139 | 0.112 | +0.418 |
| 19:21:45 | 79 → 66 | −13 | 2.50 | +1.50 | 101 | 0.102 | +0.480 |
| 19:22:00 | 66 → 106 | +40 | 3.25 | −1.25 | 94 | 0.133 | +0.439 |
| 19:22:15 | 106 → 88 | −18 | 2.00 | +0.00 | 83 | 0.082 | +0.439 |
| 19:22:30 | 88 → 115 | +27 | 3.00 | +1.50 | 122 | 0.121 | +0.505 |
| 19:22:45 | 115 → 106 | −9 | 1.00 | −0.75 | 45 | 0.040 | +0.475 |
| 19:23:00 | 106 → 79 | −27 | 1.25 | +0.50 | 50 | 0.051 | +0.485 |
| 19:23:15 | 79 → 88 | +9 | 4.00 | −3.00 | 106 | 0.162 | +0.343 |
| 19:23:30 | 88 → 79 | −9 | 4.50 | +3.75 | 125 | 0.182 | +0.485 |
| 19:23:45 | 79 → 119 | +40 | 2.50 | −2.25 | 69 | 0.101 | +0.394 |
| 19:24:00 | 119 → 119 | 0 | 1.25 | +0.25 | 41 | 0.051 | +0.404 |

La misma salida anterior `106` va seguida por `79` o por `88`, así que `C` por sí solo no es un estado de Markov suficiente. En el barrido, 10 de los 15 incrementos no nulos son múltiplos de 3 y 9 de 15 son múltiplos de 9; los cinco `−1,+49,−13,+40,+40` no son múltiplos de 3. Hay estructura aritmética que vale contrastar, pero falla la regla estricta de que cada transición caiga en una retícula 3-ádica.

### Hipótesis de estado mínimo para las transiciones

La arquitectura compatible con las contradicciones observadas requiere un estado del prefijo que retenga información adicional a `C`. La hipótesis estructural es

\[
S_{k+1}=U(S_k,x_{k+1},\Delta),\qquad C_{k+1}=G(S_{k+1}),\qquad
x_{k+1}=(O,H,L,Close,V)_{k+1}.
\]

La evidencia obliga a que `S_k` no se reduzca a `C_k`: se observan `106→79` y `106→88`; tampoco bastan `(C_k,x_{k+1},Δ)`, porque la misma vela entrante 19:23:45, con `C_k≈67`, produce `ΔC≈+21` o `−6` según el prefijo. Una hipótesis física plausible es que `S_k` codifique el recorrido ordenado y su volumen dentro de la ventana —por ejemplo, segmentos de trayectoria relativos al ancla y su orden—, pero los datos actuales no seleccionan esa estadística frente a otros resúmenes del prefijo. No fijo `U` ni `G`: esta arquitectura expresa la restricción de memoria que indican las mediciones; el generador C sigue sin identificarse.

### Contraste de contexto con vela entrante idéntica

Además del barrido, comparé cada par Lite consecutivo disponible con el mismo START, END separado exactamente por `Δ` y prefijo OHLCV idéntico. Hay **87** pares así y **62** velas entrantes distintas. De las 10 velas entrantes repetidas, las **10** producen incrementos `ΔC` distintos según el contexto; en **4** grupos la salida anterior `C` también coincide (tolerancia `10⁻⁷`) y, aun así, cambia `ΔC`.

| Entrada UTC | `Δ` | OHLCV entrante `(O,H,L,C,V)` | `C_prev` | `n_prev→C_nuevo (ΔC)` |
|---|---:|---|---:|---|
| 15:51:00 | 60 s | `(30955.75,30957,30946.25,30950,797)` | 69.00000000000038 | `24→93.00000000000269 (+24.000000000002302)`; `22→75.00000000000047 (+6.000000000000085)`; `21→67.99999999999896 (−1.000000000001421)` |
| 15:52:00 | 60 s | `(30950.25,30957.5,30948.5,30952.75,596)` | 75.00000000000051 | `24→80.99999999999949 (+5.999999999998977)`; `23→75.00000000000058 (+1.1368683772161603×10⁻¹³)` |
| 19:23:45 | 15 s | `(30868.75,30868.75,30866.25,30866.5,69)` | 67.00000000000017 | `83→88.00000000000166 (+21.000000000001492)`; `82→88.00000000000159 (+21.00000000000142)`; `81→60.9999999999996 (−6.000000000000583)` |
| 19:24:00 | 60 s | `(30866.5,30870,30866.25,30869.5,318)` | 76.9999999999985 | `24→59.99999999999963 (−16.999999999998863)`; `23→76.99999999999822 (−2.7000623958883807×10⁻¹³)` |

El detalle fila por fila se regenera con `auditar_C_estado_escalar.py`; `residuos_C_estado_escalar.csv` conserva los diez cambios y `resultado_C_estado_escalar.json` fija los hashes del maestro y del análisis fuente.

Un ejemplo especialmente directo usa la vela 15 s de 19:23:45 UTC, idéntica en ambas selecciones: `O=30868.75, H=30868.75, L=30866.25, Cierre=30866.50, V=69`. Con `C_anterior≈67`, una ventana pasa de `67` a `88` (`ΔC≈+21`); otra pasa de `67` a `61` (`ΔC≈−6`). A la precisión de captura (`C_anterior` coincide dentro de `10⁻⁷`), esto refuta operacionalmente una transición que dependa solo de `C_anterior`, OHLCV entrante y `Δ`; esos argumentos medidos no determinan un único `ΔC`.

En estos contextos `n_anterior` es 81, 82 o 83. En los 87 pares no se repite exactamente una clave `(n_anterior, C_anterior, OHLCV_entrante)` (con `C_anterior` agrupado a `10⁻⁷`), de modo que el paquete no permite decidir si basta sumar el conteo `n` al estado o si hace falta una estadística más rica del prefijo. El resultado sí descarta que rango, volumen, cuerpo, distancia al ancla u otra propiedad escalar aislada de la vela entrante explique cada transición. La auditoría completa, con las cuatro contradicciones de estado escalar y sus entradas, queda en `context_transition_audit` dentro del JSON reproducible.

La candidata larga ajustada con partición temporal estricta produce MAE `64.7647` en las 17 posiciones del barrido. Sus predicciones y residuos completos están en la tabla CSV/JSON generado; no ajusté sus parámetros tras puntuar ese lockbox.

## Contraste de ley dimensional común

Como prueba aparte de una escala temporal común, impuse la forma `C=Δq`, donde `q=C/Δ` es adimensional. La motivación formal es que, si cambiar la resolución solo dilata linealmente la magnitud, entonces `C(aΔ)=aC(Δ)` y el cociente `C/Δ` no debe depender directamente de la unidad temporal. Esto es una hipótesis comprobable, no una identidad deducida de los datos. Comparé cuatro funciones de baja complejidad: `q` constante, lineal en `n`, lineal en `ln(n)` y una OLS en `ln(n)` más descriptores OHLCV normalizados. No incluí precio absoluto ni umbral por número de velas. Los coeficientes se estiman una sola vez en el grupo de desarrollo (51 Lite: 48 de 60 s y 3 de 120 s) y después se congelan.

El modelo dimensional que incorporó OHLCV usa `x=(ln n, R_bp, L_bp, E, B_V,bp, ln(1+V̄), H_V)`, con `R_bp=10⁴(max(H)-min(L))/P₀`, `L_bp=10⁴Σ|close_i-close_(i-1)|/P₀`, `E=(close_n-close_1)/Σ|close_i-close_(i-1)|`, `B_V,bp=10⁴Σ[V_i(close_i-open_i)]/(P₀ΣV_i)`, y `H_V=Σ(V_i/ΣV_i)²`. Si un denominador de trayectoria o volumen es cero, su cociente vale cero. Se estandariza cada entrada como `z_j=(x_j−μ_j)/s_j` usando exclusivamente el desarrollo, y la ecuación candidata queda completamente especificada por:

\[
\widehat C=\Delta\widehat q,\qquad
\widehat q=1.2273572270438204+\sum_{j=1}^{7}\beta_j z_j,
\]

| Característica `x_j` | `μ_j` desarrollo | `s_j` desarrollo | `β_j` |
|---|---:|---:|---:|
| `ln n` | 3.1008009971997743 | 0.17478792391082912 | +0.14961429751752173 |
| `R_bp` | 21.60956830457685 | 9.478667500088088 | −0.05293495460636500 |
| `L_bp` | 42.42210940573142 | 17.012979656625625 | +0.06164957304931654 |
| `E` | 0.09090952046736332 | 0.3456881114893346 | −0.08449810439083150 |
| `B_V,bp` | 0.17811351038799675 | 0.8178479927701898 | +0.12368101358798915 |
| `ln(1+V̄)` | 5.995587002091939 | 1.0292893616586258 | −0.02120083681699807 |
| `H_V` | 0.05325677464808578 | 0.008581663892773183 | −0.008858633237186248 |

El contraste temporal se fijó por timestamps antes de ajustar: 51 Lite para desarrollo y 94 Lite reservados. El lockbox contiene 39 casos de 15 s, 54 de 60 s y 1 de 120 s. No hay datos de 15 s en el desarrollo. Las predicciones exactas de las cuatro familias para los 179 casos, residuos completos para los 145 Lite y compatibilidad de los 34 intervalos Character están en `residuos_C_ley_dimensionless.csv`; los coeficientes de doble precisión y métricas están en `resultado_C_ley_dimensionless.json`.

| `q` candidata | Desarrollo MAE / RMSE | Reservado MAE / RMSE | Máximo reservado | Reservado a ≤1 | Character-only compatibles |
|---|---:|---:|---:|---:|---:|
| Constante | 9.9954 / 13.2713 | 32.6111 / 44.2383 | 104.5896 | 0/94 | 0/34 |
| Lineal `n` | 5.0400 / 6.5756 | **16.0237 / 22.2433** | 58.4937 | 5/94 | 0/34 |
| Lineal `ln n` | 4.1778 / 5.7922 | 26.4136 / 38.1842 | 143.3626 | 5/94 | 0/34 |
| `ln n` + OHLCV normalizado | 3.8433 / 5.3503 | 27.2505 / 38.8631 | 143.3645 | 5/94 | 0/34 |

La función lineal en `n`, `q̂=1.2273572270438204+0.1833299413211566(n−22.607843137254903)/4.915276033469331`, fue la de menor MAE reservado entre estas cuatro, pero sigue con MAE `16.0237`, máximo `58.4937` y solo 5/94 predicciones a ±1. El modelo con OHLCV mejora el error de ajuste y empeora la reserva frente a `q` lineal en `n`; añadir estos rasgos no dio una transferencia reproducible. La versión logarítmica, que ajusta bien las 51 observaciones de desarrollo, da MAE `26.4136` en reserva y un máximo error `143.3626`. Ninguna es ley identificada.

En el mejor contraste simple (`q` lineal en `n`), por resolución el holdout da: 15 s, 39 casos, MAE `21.1136`, RMSE `27.2557`, máximo `58.4937`, 3/39 a ±1; 60 s, 54 casos, MAE `12.1875`, RMSE `17.7049`, máximo `52.7673`, 2/54 a ±1; 120 s, un único caso, error absoluto `24.6710`. Por tamaño de ventana, los 19 reservados con `n<21` dan MAE `9.1342` y 2/19 a ±1; los 75 con `n≥21`, MAE `17.7690` y 3/75. Esto contrasta directamente la continuación de la relación empírica corta: al quitar la excepción por umbral y forzar una escala común, no se reproduce el régimen corto ni el largo. Tampoco hay validación larga de 2 m; el único holdout de 120 s es corto. El modelo completo de este apartado se reproduce con `python G:\trading\guias\analisis\probar_ley_dimensionless_C.py`.

## Validación por bloques de tiempo disjuntos

El lockbox por timestamps aún podía compartir velas con ventanas de entrenamiento que solo rozaban o conectaban el mismo episodio. Para medir cuánto afecta ese solapamiento, agrupé ventanas en un grafo: dos casos del mismo contexto se conectan si sus coberturas físicas `[primera apertura, última apertura + Δ)` se cruzan, incluso si las resoluciones difieren. Cada predicción de esta prueba se ajusta excluyendo el componente temporal entero al que pertenece el caso. La partición resultante tiene 11 componentes, 145 etiquetas Lite y 34 intervalos Character; ninguna pareja de componentes comparte tiempo cubierto. Se auditan únicamente las familias ya fijadas en los apartados anteriores; no se seleccionan rasgos nuevos con estos resultados.

El componente 6 es el episodio grande que contiene el barrido y los controles multi-timeframe: 117 casos (84 Lite y 33 Character-only), con 57 casos de 15 s, 52 de 60 s, 2 de 30 s y 6 de 120 s. Al reservarlo, el desarrollo restante son 61 Lite de **60 s solamente**. Así, el test exige transferir el modelo ajustado en 1 m a 15 s y 2 m. Para la candidata simple `q` lineal en `n`, ese bloque da MAE `17.2490`, RMSE `23.3257`, máximo `58.8656`, 3/84 a ±1; separado por resolución, MAE `21.4088` en 39 casos de 15 s, `13.9074` en 41 de 60 s y `10.9428` en 4 de 120 s. La OLS larga de ocho características, entrenada solo con largos fuera del bloque y redondeada al segundo, da MAE `43.5231`, máximo `85`, 1/65 a ±1.

Al reservar ese componente, `ln(Δ)` es constante en los ajustes OLS de `C` (rango de diseño 8/9); el coeficiente temporal no se identifica en esos folds y el mínimo cuadrático da su extensión de norma mínima. Por tanto, esos dos scores OLS no sirven para estimar el efecto de resolución. Los modelos `q` evitan ese grado degenerado al expresar `Δ` como factor dimensional explícito; sus errores también son demasiado grandes para validar la transferencia.

| Candidata con cada componente fuera de entrenamiento | Lite puntuados | MAE | RMSE | Máximo | A ±1 | Character compatibles |
|---|---:|---:|---:|---:|---:|---:|
| `q` lineal en `n` | 145 | 12.6243 | 18.7683 | 58.8656 | 5/145 | 0/34 |
| `q` lineal en `ln n` | 145 | 26.4355 | 35.0938 | 139.5991 | 4/145 | 1/34 |
| `q` + OHLCV normalizado | 145 | 41.6987 | 56.4294 | 232.3660 | 4/145 | 0/34 |
| OLS de `C` + OHLCV, sin umbral ni redondeo | 145 | 35.4395 | 50.8211 | 232.3660 | 4/145 | 0/34 |
| OLS larga de `C` + OHLCV, con redondeo | 110 | 29.3727 | 40.3912 | 85.0000 | 10/110 | 1/33 |

La tabla no se debe leer como estimación de precisión fuera de estas fechas: el componente grande concentra la única muestra de 15 s y los bloques pequeños restantes son tramos del mismo símbolo y jornada. Sí corrige la evaluación anterior por dependencia temporal. Ninguna candidata obtiene errores compatibles con un generador exacto y el modelo con rasgos OHLCV no mejora transferencia entre bloques. El script genera `resultado_C_bloques_disjuntos.json` y el CSV completo `residuos_C_bloques_disjuntos.csv` (859 filas: valores predichos y residuos de cada caso Lite apto más las comprobaciones de intervalos Character); reproduce la partición y cada ajuste con `python G:\trading\guias\analisis\auditar_validacion_bloques_disjuntos_C.py`.

### Control adicional: matriz nombrada + barrido excluidos del ajuste

Como contraste más directo, repetí el mismo vector de ocho características y la misma OLS, excluyendo del ajuste los **inputs OHLCV exactos** de `C_cruce_doble.json` (25 filas), el barrido (17) y el control 15s/1m/2m (3). Quedaron 85 casos Lite largos para estimar los coeficientes (`16` de 15 s, `68` de 60 s y `1` de 120 s). Ninguno de los 40 inputs de control únicos entró al ajuste. Esto reserva etiquetas por input; las ventanas del mismo episodio aún se solapan, así que no equivale a independencia temporal.

| Grupo reservado | Filas | Lite largo | MAE | RMSE | a ≤1 | Character-only compatible |
|---|---:|---:|---:|---:|---:|---:|
| Matriz `C_cruce_doble` | 25 | 11 | 20.0000 | 24.5875 | 1/11 | 0/14 |
| Barrido END | 17 | 17 | 17.5882 | 21.3803 | 1/17 | — |
| Temporalidades | 3 | 2 | 2.5000 | 2.9155 | 1/2 | — |
| Unión sin duplicar inputs | 40 | 25 | 16.8000 | 21.6037 | 3/25 | 0/14 |

En esta segunda partición, las predicciones para el barrido suben gradualmente de 78 a 85 mientras C observado salta entre 66 y 119; el MAE mejora frente a la partición temporal estricta, pero el candidato sigue rechazado. Los residuos exactos de las 45 filas nombradas están en `residuos_C_controles_modelo.csv`. La mejora al permitir entrenamiento con ventanas vecinas del mismo episodio confirma que esos solapamientos aportan señal, y también por qué esa puntuación no debe llamarse holdout independiente.

## Modelo de actualización con memoria: contraste adicional

Para comprobar directamente la hipótesis de estado, ajusté tres actualizaciones anidadas sobre los 87 pares adyacentes con prefijo OHLCV idéntico:

\[
\widehat{\Delta C}_k=\beta_0+\sum_j\beta_j\frac{x_{j,k}-\mu_j}{s_j},\qquad
\widehat C_k=C_{k-1}+\widehat{\Delta C}_k.
\]

El estado escalar usa `(C_anterior, ln n, ln Δ)`. El estado de prefijo agrega rango y recorrido normalizados, eficiencia firmada y tres descriptores de volumen. La tercera versión añade rango relativo, cuerpo, volumen relativo y gap de cierre de la vela entrante. Las características y coeficientes ajustados están registrados íntegramente en `resultado_C_transiciones_dinamicas.json`; los residuos por par y modelo, en `residuos_C_transiciones_dinamicas.csv`.

La misma partición temporal deja **26 pares de entrenamiento** (24 de 60 s y 2 de 120 s) y **61 pares reservados** (25 de 15 s y 36 de 60 s). No hay transiciones de 15 s en el entrenamiento. El cálculo “un paso” recibe el `C_anterior` observado; el replay recursivo propaga la predicción de C en cada cadena y usa una medición conocida solo para iniciar o reiniciar una cadena desconectada.

| Actualización | MAE de ΔC en ajuste | MAE / RMSE reservados, un paso | Dentro de ±1 | MAE / RMSE reservados, replay |
|---|---:|---:|---:|---:|
| Estado escalar `(C_anterior, ln n, ln Δ)` | 3.6373 | 37.4205 / 52.1682 | 6/61 | 31.9461 / 45.5682 |
| Estado del prefijo | 3.1724 | 73.3836 / 86.6976 | 0/61 | 54.0684 / 66.5201 |
| Prefijo + vela entrante | 2.7488 | 187.3886 / 221.7100 | 0/61 | 138.1911 / 166.4825 |

Agregar características reduce el error de ajuste y empeora drásticamente el reservado: esa familia lineal de memoria no explica las transiciones. El error de un paso de 15 s del modelo escalar es MAE `61.5470` (25 casos); en 60 s es `20.6660` (36 casos). El replay reduce algunos errores por su regresión hacia el promedio, pero no vuelve preciso al candidato. La separación se calcula por tiempo dentro del script, aunque las etiquetas ya eran conocidas; no es una validación prospectiva. Este resultado rechaza estas tres actualizaciones lineales concretas, no toda arquitectura recursiva.

## Fase modular: pista de base 3, sin ley confirmada

Para tratar la pista aritmética sin escoger solo el barrido, calculé residuos de `C` y `ΔC` en los 87 pares adyacentes; el análisis no ajusta parámetros y escanea módulos del 2 al 12. En 66 pares ambos extremos son enteros a tolerancia `10⁻⁷`; 47 de esos pares tienen `ΔC≠0`.

| Resolución | Pares enteros | `ΔC≠0` | No nulos divisibles por 3 | No nulos divisibles por 9 | Cambia `C mod 3` |
|---|---:|---:|---:|---:|---:|
| 15 s | 23 | 22 | 16/22 | 9/22 | 6/23 |
| 60 s | 43 | 25 | 10/25 | 0/25 | 15/43 |
| 120 s | 0 | 0 | — | — | — |

El barrido de 15 s conserva `C mod 3` en 11/16 pasos y `C mod 9` en 10/16. Sin embargo, la retícula de incrementos múltiples de 9 no transfiere a 60 s: los 18 incrementos divisibles por 9 de esa resolución son ceros; ninguno de sus 25 cambios no nulos es múltiplo de 9. El módulo 3 tampoco ofrece una regla común simple: 16/22 cambios de 15 s, pero solo 10/25 de 60 s, son múltiplos de 3. La exploración de módulos confirma que 3 resalta en 15 s, pero no en 60 s; por tanto no valida un armónico universal.

Una hipótesis provisional para la secuencia es que los eventos estructurales (nuevo máximo/mínimo global o pivote local de radio 1 confirmado) elevan la posibilidad de cambiar la fase `C mod 3`: 4/12 pares con evento frente a 2/11 sin evento a 15 s; 14/34 frente a 1/9 a 60 s. En conjunto son 18/46 frente a 3/20. No es una regla suficiente: muchos eventos conservan la fase y hay cambios de fase sin evento. Las ventanas se solapan y comparten velas, así que estas proporciones son descriptivas, no una prueba estadística independiente. Tampoco explican el cociente/amplitud `⌊C/3⌋`, el instante del cambio ni las salidas fraccionarias cortas.

Separé cada evento como predictor sin parámetros: “cambia la fase si ocurre el evento; si no, se conserva”, y lo comparé con predecir siempre la clase mayoritaria. Para `C mod 3`, el nuevo máximo global da 46/66 (69.7%) frente a 45/66 (68.2%) del baseline; a 15 s empata el baseline (17/23) y a 60 s mejora apenas a 29/43 frente a 28/43. La unión de los cuatro eventos baja a 35/66 (53.0%). Para `C mod 9`, la unión sube a 42/66 (63.6%) frente a 38/66 (57.6%), pero esto solo predice la fase, no `C`; el resultado de 120 s sigue sin transiciones enteras comparables. Los scores completos por evento y resolución están en el JSON.

La interpretación que queda abierta es una fase de estado con posibles disparadores estructurales, mientras el nivel completo depende de más información del prefijo. No hay todavía una función para actualizar esa fase o el nivel, por lo que esto es una hipótesis falsable y no una ecuación candidata validada. La tabla completa de residuos modulares y eventos está en `transiciones_C_fase_base3.csv`; el resumen reproducible está en `resultado_C_fase_base3.json`.

### Fase de los niveles C en los 145 Lite

Extendí el análisis desde incrementos a los propios niveles `C mod 3`, `C mod 9` y `C mod 27`, manteniendo los fraccionarios fuera del conteo modular en vez de redondearlos. Entre los 110 casos largos, los 37 de 15 s y 72 de 60 s son enteros dentro de `10⁻⁷`; el único caso largo de 120 s también es entero. La distribución mod 9 muestra una asimetría local en 15 s que no transfiere:

| Fuente | `n` | Enteros Lite | Frecuencias `C mod 9` para residuos 0..8 |
|---:|---:|---:|---|
| 15 s | `≥21` | 37/37 | `1, 1, 2, 2, 0, 0, 1, 21, 0` |
| 60 s | `≥21` | 72/72 | `3, 8, 4, 14, 1, 19, 8, 2, 13` |
| 120 s | `≥21` | 1/1 | `0, 0, 1, 0, 0, 0, 0, 0, 0` |

En 15 s, `C≡7 (mod 9)` aparece en 21/37 etiquetas; al quitar repeticiones del mismo valor quedan 6/12 niveles únicos en esa fase. En 60 s aparecen las nueve fases y `C≡7` solo 2/72 veces. El único dato largo de 120 s no permite estimar una distribución. En `n<21` hay 21/35 etiquetas fraccionarias; las enteras cortas de 60 s son 13 copias de `C=60`, por lo que su fase común `mod 9` es solo el suelo empírico de la resolución, no evidencia de armónicos.

Para el barrido 15 s, seis de las 16 transiciones cambian `C mod 9`; cinco coinciden con uno de los eventos prefijados (nuevo extremo global o pivote local radio 1) y una no. A la vez, cuatro de las nueve transiciones con alguno de esos eventos conservan la fase. La hipótesis de trabajo queda acotada así: **en ese episodio puede haber una fase latente mod 9 que algunas entradas estructurales cambian, mientras los estados dentro de una fase dan saltos múltiplos de 9**. No es una ecuación completa ni un disparador suficiente: un contraejemplo ya ocurre en 19:22:00 (`C=66→106`, cambio de fase sin evento prefijado), y la distribución de 60 s contradice que mod 9 sea una fase global común. Esta pista no permite atribuir cada transición a rango, volumen o distancia al ancla.

Las frecuencias mod 3/9/27 y los niveles exactos se reproducen con `auditar_niveles_modulares_C.py`; `residuos_C_niveles_modulares.csv` contiene una fila exacta por cada Lite, y `resultado_C_niveles_modulares.json` conserva los conteos y la secuencia completa del barrido. Las cuentas son descriptivas: el grupo de 15 s proviene de un solo episodio con ventanas solapadas.

### Contraste fuera de bloque del disparador de fase

Contrasté la regla fija “cambia la fase si entra una vela que hace nuevo extremo global o confirma un pivote local de radio 1” con un baseline que, en cada fold, predice la clase mayoritaria de los otros bloques. Los casos de ventanas temporalmente solapadas permanecen juntos: quedan 66 pares con extremos enteros repartidos en 11 componentes; los intervalos de 120 s no aportan pares enteros comparables. La exactitud agregada de los folds es:

| Fase | Resolución | Regla de evento | Mayoría de otros bloques |
|---|---:|---:|---:|
| `C mod 3` | Total | 35/66 (53.0%) | 45/66 (68.2%) |
| `C mod 3` | 15 s | 13/23 (56.5%) | 17/23 (73.9%) |
| `C mod 3` | 60 s | 22/43 (51.2%) | 28/43 (65.1%) |
| `C mod 9` | Total | 42/66 (63.6%) | 38/66 (57.6%) |
| `C mod 9` | 15 s | 14/23 (60.9%) | 13/23 (56.5%) |
| `C mod 9` | 60 s | 28/43 (65.1%) | 25/43 (58.1%) |

La regla estructural pierde con claridad en `mod 3` y solo mejora modestamente el baseline en `mod 9`. Al excluir el componente temporal grande (45 pares de prueba; 21 pares de entrenamiento en los otros bloques), `mod 9` queda en 29/45 (64.4%) frente a 25/45 (55.6%); el resultado sigue siendo una clasificación de fase, no una predicción del nivel ni de la magnitud de `C`. Toda la secuencia de 15 s pertenece a un solo episodio solapado, así que no mide transferencia entre episodios de esa resolución. Este contraste debilita la interpretación causal de los eventos y no cambia el estado del objetivo: todavía no hay operador matemático unificado.

El cálculo fijo y sus residuos por fold se reproducen con `auditar_eventos_fase_bloques_C.py`; `resultado_C_eventos_fase_bloques.json` guarda las matrices de confusión y `residuos_C_eventos_fase_bloques.csv` las 132 predicciones fase-fold.

## Arquitectura que queda como hipótesis, no como resultado

Las repeticiones y la insuficiencia de `C` como estado escalar sugieren que, si el origen es recursivo, necesita un estado que conserve información de la trayectoria:

\[
z_{k+1}=F_\theta(z_k,\varphi(OHLCV_k,\Delta)),\qquad
C_k=Q_\theta(G_\theta(z_k,\Delta)).
\]

Esto solo especifica dónde podría residir la memoria; no define `F`, `φ`, `G`, `Q` ni una regla predictiva. La regresión explícita anterior fue la candidata parametrizada y queda rechazada. El efecto de fase asociado a eventos es una pista descriptiva, pero no permite atribuir `ΔC` a rango relativo, volumen, distancia al ancla o una regla base 3 de forma predictiva e independiente. La prueba de escala añade la restricción experimental `C(2·OHLC,V,Δ)=C(OHLC,V,Δ)` para una ventana 1 m; cualquier ajuste futuro debe preservarla y replicarla fuera de ese episodio.

## Residuos reproducibles y límites

`residuos_C_modelo_independiente.csv` contiene los 179 casos con la partición temporal estricta: predicción separada de observación, residuo de cada uno de los 145 Lite y compatibilidad por intervalo para los 34 Character-only. `residuos_C_controles_modelo.csv` contiene los residuos de los controles nombrados con el segundo ajuste. `residuos_C_ley_dimensionless.csv` guarda cuatro filas por caso (716 filas), `C_hat` y residuo numérico de las 145 etiquetas Lite, además de compatibilidad de Character. `transiciones_C_barrido_independiente.csv` contiene las 16 velas entrantes, sus variables, eventos causales y `ΔC`. `resultado_C_modelo_independiente.json` guarda métricas, coeficientes, límites de ambas particiones y hashes. La auditoría dinámica genera `resultado_C_transiciones_dinamicas.json` y 183 residuos (`3 modelos × 61 pares reservados`) en `residuos_C_transiciones_dinamicas.csv`. La auditoría modular genera `resultado_C_fase_base3.json` y una fila por cada uno de los 87 pares en `transiciones_C_fase_base3.csv`. La auditoría de eventos por componentes genera `resultado_C_eventos_fase_bloques.json` y 132 residuos fase-fold. `residuos_C_niveles_modulares.csv` contiene los 145 valores Lite exactos junto con sus fases enteras aplicables; el CSV de 1 s suplementario añade 21 conteos de una única ancla y sus residuos disponibles. Las extensiones de transferencia congelada generan residuos para 21 puntos nativos de 1 s y los 179 casos del maestro sin refit. Los contrastes de START/END y `n=27/28` guardan C, predicciones congeladas y residuos explícitos en sus JSON de resultados. La auditoría de escala genera seis residuos numéricos en `residuos_C_escala_50.csv` y métricas, residuos, errores de recurrencia y hashes en `resultado_C_escala_50_completa.json`. Los análisis se regeneran sin modificar los datos fuente con:

```powershell
python G:\trading\guias\analisis\analizar_modelo_C_independiente.py
python G:\trading\guias\analisis\probar_ley_dimensionless_C.py
python G:\trading\guias\analisis\auditar_validacion_bloques_disjuntos_C.py
python G:\trading\guias\analisis\auditar_actualizacion_C_transiciones.py
python G:\trading\guias\analisis\auditar_fase_base3_C.py
python G:\trading\guias\analisis\auditar_niveles_modulares_C.py
python G:\trading\guias\analisis\auditar_eventos_fase_bloques_C.py
python G:\trading\guias\analisis\auditar_C_meseta_1s_conteos.py
python G:\trading\guias\analisis\auditar_transferencia_nativa_1s_C.py
python G:\trading\guias\analisis\auditar_C_q_redondeado_maestro.py
python G:\trading\guias\analisis\analizar_C_1s_cruce_START.py
python G:\trading\guias\analisis\analizar_C_1s_1402_n27_n28.py
python G:\trading\guias\analisis\auditar_C_escala_50_ohlcv.py
python G:\trading\guias\analisis\auditar_C_escala_50_completa.py
python G:\trading\guias\analisis\auditar_C_escala_multi_tf.py
```

Límites que sí quedan comprobados:

- 35/35 casos Lite cortos coinciden numéricamente con la relación corta descrita, pero el factor `10/183` sigue sin derivación física.
- La candidata de trayectoria larga falla 75/75 pruebas reservadas a tolerancia ±1 y solo 1/34 intervalos Character-only es compatible.
- Las 37 observaciones Lite de 15 s del corte están en un único episodio; no hay una segunda sesión de 15 s para validación por grupos.
- El maestro ofrece cuatro casos Lite de 120 s y solo uno tiene `n≥21`; no hay prueba reservada larga de 2 m.
- La invariancia a escala positiva queda validada en una sola ventana 1 m; falta replicarla en nuevas ventanas y resoluciones antes de tratarla como simetría universal.
- Los casos conocidos son finitos y solapados. Dado cualquier interpolador `F₀` de estas entradas, se puede sumar `λ·Πᵢ‖x−xᵢ‖²`: esa familia mantiene todos los valores observados y cambia las predicciones fuera del conjunto. Por ello, sin estructura impuesta o mediciones prospectivas, el paquete no determina un único `f(OHLCV,Δ)`.

Para aceptar un generador común hace falta registrar el algoritmo completo y sus predicciones antes de medir episodios nuevos, con Lite decimal en cada temporalidad y una serie 2 m larga. Hasta entonces, el resultado correcto de esta auditoría es **ley unificada no identificada**, con una regla corta empírica y una candidata larga rechazada.
