# Paquete consolidado para trabajo simultáneo sobre C

Preparado14oct2026. Directorio: G:\trading\guias\analisis. TradingView quedó restaurado: referencia12oct18:55–19:20, gráfico1m, Litefuente1m, Character6.5.36fuenteChart/perfilB/Manual,PDarraysoff,Showrangetrue,Replayoff,preciosauxiliaresoriginales. No se modificaron los archivos deGemini ni el maestro93anterior.

## 1. Entrada principal y cómo leerla

**master_all_C_cases.json**:179selecciones únicas, todas conOHLCVcompleto y timestampsUnix/ISO8601UTC. Incluye los112anteriores, los9controles externos al112, los25controles deC_cruce_doble.json, otrosrangoshistóricos y lasmedicionesnuevas. Estos grupos se solapan: no sumar susconteos para obtener eltotal.

- **145casos tienen C_Lite medido**, con precisión de la extracción de las seiscurvas. Para ajuste exacto usarC_Lite.
- **34casos son Character-only**: C_Lite=null. C es su único entero compatible y C_Character_interval conserva límites. No afirmar que ese entero sea una medición decimalLite; puntuar compatibilidad con el intervalo. ObtenerLiteparaesos34 sería una adquisición adicional, no una operación de consolidación.
- OHLC conserva precios/timestamps; OHLCV añadevolume. Volumen enlazado en pares deCSVnativos conOHLCidéntico; cuando se agrega hacia30s/120s, se exige tambiénOHLCagregadoexacto. Nunca se repartióvolumen1mpara fabricar15s ni se sustituyeron faltantes por0.
- START/END son anclas solicitadas exactas. effective_START/effective_END son aperturasfuente realmenteincluidas. Pueden diferir en anclas subvela: no redondearlas silenciosamente ni deduplicarlas por losprecios solamente.
- dt,source_seconds,chart_seconds describen el conjunto nativo. profileB,Manual,NQ1!,ETH,UTC,BADJoff. Otras configuraciones y controles sinCexactoasignado se conservan en **auxiliary_reports**, con el alcance original; no mezclarlos en entrenamiento como casos homogéneos.
- provenance y hashes identifican fuentes. blind_or_prospective=false: las etiquetas ya estaban disponibles; muchosrangos se solapan. prior_split conserva el origen, no garantiza independencia/ciegas para un modelo que ya los leyó.

**master_all_C_cases_index.json** es un índice compacto. **PAQUETE_GEMINI_QA.json** confirma deduplicación, cobertura112+9/25,datos yOHLCV. **master_all_C_cases_exclusions.json** registra referenciasCSVantiguas sin toda la cobertura: sus tres casos decrucedoble sí están incluidos desde otras fuentes completas, comprobado25/25.

Reproducción: preparar_mediciones_Gemini.py, consolidar_master_all_C.py yverificar_paquete_Gemini.py. No ejecutarlos simultáneamente con un proceso que edite estas salidas; paraGemini basta leer el snapshot y guardar propuestas en supropioscratch.

## 2. Barrido continuoEND solicitado

**C_barrido_END_1855_1920_1924_15s.json**:START12oct18:55:00UTC, fuente/gráfico15s.17posiciones contando ambos extremos,16incrementos. Cada medición tiene dosCSVaceptados,OHLCV, seisajustesLite, repetición deplots, verificación desemillaEND/primera publicación y capturadeancla. Characterpermaneció fijo enEND19:20: no usar sus columnas delCSVpara inferirCde cada paso.

|END UTC|C Lite, redondeado para lectura|
|---|---:|
|19:20:00|106|
|19:20:15|79|
|19:20:30|67|
|19:20:45|66|
|19:21:00|115|
|19:21:15|106|
|19:21:30|79|
|19:21:45|66|
|19:22:00|106|
|19:22:15|88|
|19:22:30|115|
|19:22:45|106|
|19:23:00|79|
|19:23:15|88|
|19:23:30|79|
|19:23:45|119|
|19:24:00|119|

Lospasos22:45y23:30a/b fueron inestables; se conservaron y se aceptaronc/dtras repetir. No se interpoló ningúnC. Cada rango es el anterior más una velaOHLCV; verificado. Valoresdecimales completos enJSON, no solo los enteros de esta tabla.

## 3. Mismas anclas, tres temporalidades

**C_test_timeframes_1900_1920.json**,12oct19:00:00–19:20:00UTC, fuenteigualalgráfico, ambosindicadores:

|Fuente/gráfico|Velas inclusivas|C Lite|
|---|---:|---:|
|15s|81|67|
|1m|21|77|
|2m|11|120|

Esto **no aísla invariancia del intervalovisible manteniendo lafuente fija**. CambianOHLC,conteo y cobertura de la velaEND: terminan19:20:15,19:21:00y19:22:00respectivamente (límitesexclusivos). El caso2m entraenramacorta. Noatribuirladiferenciaaunfactortiempo sin considerar esos cambios. Los estudios de fuente fija/otrográfico están preservados enauxiliary_reports.

Se conservaron los primerosCSVsinOHLCdelrangooCharacterobsoleto; se aceptaron15sg/h,1ma/b,2mc/d. Los archivosdiagnósticos no entran como nuevas mediciones independientes.

## 4. Familias ya contrastadas

Leer **MODELOS_REFUTADOS_PARA_GEMINI.md** antes de repetir búsquedas. Cada rechazo tiene una definición acotada y una referencia a scripts/resultados. No declarar refutadas todas las funcionescontinuas, todos losvolúmenes o todos lospivotes.

## 5. Etiquetas del oficial

**ETIQUETAS_OFICIALES_PARA_GEMINI.md** y capturasmanual/C_pack_PD_prebreak.png yC_pack_PD_postbreak.png:

- ShowPDarrays imprimeFVG,IFVG,VI; se observaron antes de la ruptura.
- Showrange representa elrango; no se encontró una tablaC oestadísticadelgenerador.
- **ShowEMA timeframe labels** es otra opción. Tras la ruptura aparecenC/27 2.3s,C/9 6.89s,C/3 20.67s, además de temporalidadaproximadaTV/SYN. Son salidas derivadas deC62redondeadas, no la ecuación que lo genera. No estaban disponibles antes de publicarEMAen el control observado.

## Encargo sugerido para Gemini

Lee este paquete y congela una copia/hash del maestro que uses. Trabaja en tu scratch, sin modificarG:\trading\guias\analisis ni sus datasets. Separa C_Litemedido de Character-only y sus intervalos, y separa configuracionesnativas de los informes auxiliares.

Propón **un algoritmo concreto**: entradas,fuente,tratamiento de anclas,estado inicial,actualización y operaciónnumérica final. Devuelve para cada caso una predicción y una traza de estado separadas deCobservado. Explica lafrontera20→21 y loscontraejemplos de la matriz, incluidosC54y88/61, sin excepciones basadas en fecha,precio absoluto ovalorCya conocido. Las constantes o umbrales ajustados deben declararse como ajustes, no como descubrimientos.

Antes de una nuevamedición, registra el código completo congelado, lascondiciones de rechazo y laspredicciones de un episodio distinto. Si no pasa losdatos conocidos, informa el contraejemplo y detén ese candidato; añadirotraexcepción no es validación. Los179casos compartidos son conocidos ysolapados: no llamarlos un holdout ciego. La búsqueda no garantiza recuperar una ecuación única; el objetivo es producir una hipótesis comprobable que explique las salidas.
