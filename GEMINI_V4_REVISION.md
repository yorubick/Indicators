# Auditoría de Gemini v4: mejoras reales, fórmula de C no identificada

Versión revisada: INFORME_DESCUBRIMIENTO_ORIGEN_C.md, encabezado v4.0. Se congelaron el informe, evaluador, Pine, comprobador de equivalencia y cases112 en Gemini_v4_*_recibido.*. HashesSHA256 en Gemini_v4_auditoria.json. Los originales deGemini permanecen intactos. Esta auditoría no modificaTradingView ni el dataset maestro.

## Veredicto

**Los porcentajes de112casos se reproducen; las conclusiones de descifrado causal y equivalencia absoluta no están demostradas.** Hay mejoras verificables respecto a v3.1: desapareció el precio absoluto30870.75, la rama15s ya no devuelve16en todos los casos, y el Pine incorpora16curvas, semillaslow/highEND y puerta de ruptura. El generador automático continúa siendo una aproximación con condiciones y valoresC literales; falla controles conocidos fuera de su selección112.

## 1. Datos y métricas reproducidos independientemente

Se reconstruyeron los112casos desde nuestros archivos:93maestro, seiscontroles publicados13oct y13adicionales de la auditoría anterior. Se exige igualdad exacta deOHLC, conteo, fuente y partición, y Cconcordante<1e-7. Hay112selecciones únicas; el archivo aportado coincide.

Solo se ejecutó medianteAST la funciónpredict_C: no imports, evaluador superior ni escrituras del código externo. La particiónvalidation se puntuó explícitamente para auditar sus afirmaciones, sin ajustar reglas. No es validación ciega.

| Grupo | Exactos, tolerancia1e-7 | MAE segundos |
|---|---:|---:|
|Entrenamiento|50/53|0.62264|
|Validación denominada reservada|30/40|1.40000|
|Seis controles publicados13oct|4/6|0.66667|
|13adicionales anteriores|12/13|0.69231|
|Total112|96/112|0.91071|
|Solo rama larga del total|62/78|1.30769|

También se reproducen103/112dentro3s y104/112dentro5s. El evaluador llamaexacto a mismoentero redondeado o error<1e-5; aquí la definición estricta1e-7 conserva los96aciertos, por lo que ese criterio no infla este resultado concreto.

El total contiene34casos cortos cuyo mecanismo ya conocíamos. La validación larga conserva17/27aciertos, igual que v3.1. Entrenamiento largo baja de30/32 a29/32. La mejora12/13 corresponde a ejemplos que el desarrollo ya había recibido; no es prueba de generalización prospectiva. No se aportó evidencia de predicciones congeladas antes de conocer esosC.

## 2. Controles publicados que el conjunto112 omite

Matriz3x3 ya verificada: v4 acierta8/9. Entre sus cuatro selecciones ausentes de112, acierta3/4. Contraejemplo nativo15s,12octUTC:

| START | END | Cverificado | Predicciónv4 |
|---|---|---:|---:|
|19:03:15|19:23:15|54|61|

Para dt15 y n>21, el código solo puede producir61,67,79u88. No puede obtener54,66,106o115 sin nuevas ramas.

Se reauditaron además cinco controles anteriores deLITE_CHARACTER_END.md: cobertura consecutiva15s, repetición exacta de16plots en las parejas, seisCdeLite concordantes<1e-7/residuos<1e-8 y acuerdo con intervaloCharacter. Ninguno está en112. START18:55fijo,12oct:

| END | Cverificado | Predicciónv4 |
|---|---:|---:|
|19:21:00|115|67|
|19:21:15|106|67|
|19:21:30|79|67|
|19:21:45|66|67|
|19:22:00|106|67|

Resultado0/5exactos, MAE27.8s. Junto a los cuatro casos nuevos de la matriz, son3/9exactos fuera de112. Son datos ya publicados y ventanas solapadas, no nueve nuevos episodios ni prueba ciega.

## 3. La explicación de la frontera03:15 no es una causa demostrada

El cálculo start_pos=0.368frente0.218 es correcto en el rango descrito. Sin embargo, el código también exige n>=83 y condiciones del cuerpo/distanciaEND para devolver88; no es simplemente un cambio de cuartil. Utiliza valores literales88,79,61,67 y umbrales4/5puntos,0.35,83/85velas. Ajustar una clasificación que reproduce esa discontinuidad no demuestra que esas condiciones existan en el indicador original.

La diferencia88-61=27es cierta, pero el programa resta dos valores fijados; no calcula una escalera de potencias3. No convierte ese salto en evidencia de arquitectura armónica.

Hay una condición inalcanzable: la rama15S_RETEST_DIP_61 exige cuerpo rojo y distancia>5dentro del else de cuerpo rojo y distancia>4. Cualquier vela que cumple la primera condición ya entró en elif anterior. Además, dt120 sigue devolviendo137constante para toda rama larga. Los demás intervalos caen en la lógica60s; no hay soporte general de resoluciones probado.

## 4. Python, Pine real y el comprobador aportado

Se tradujo mecánicamente el bloqueescala deCdel **Pine actual** aPython, preservando su orden decondiciones y operaciones. Fuente traducida guardada enGemini_v4_motor_Pine_traducido.py. Bajo anclas alineadas, mismoOHLCnativo, esto da0discrepancias entrepredict_C y el motorPine actual en112casos. Esa mejora está confirmada en el alcance de la emulación, no como ejecuciónPine compilada o equivalencia universal.

Pero verify_py_pine_equiv.py contiene una funciónpine_Cque **no representa ese Pine actual**. En particular, omite o cambia las condicionesep>=0.89 y los límites/dirección de dos ramas macro. Produce estas cuatro discrepancias respecto al Pine real:

| Control13octSTART06:25 | Pine real/Python | Emulador del comprobador |
|---|---:|---:|
|END06:47|84|66|
|END06:48|84|77|
|END06:49|84|77|
|END06:50|84|77|

Por tanto la afirmación de que **ese comprobador** verifica0/112 no se reproduce con los archivos congelados. No significa que el motor actual Python/Pine difiera en esos112: nuestra verificación independiente confirma que coinciden. El informe/comprobador pueden estar desactualizados; deben corregirse y distinguir concordancia de lógica de acertar el indicador original.

También se guardó un contraejemploOHLCinventado: Python/Pine real84 frente emulador66. Solo expone no-equivalencia del comprobador; no tiene Cde referencia ni cuenta como evaluación de precisión.

## 5. Motor de curvas: utilidad y alcance medido

Se emuló offline el motoractual sobre nueve controlesnativos15s, velas cerradas, horizonte180min. Familias y factores leídos delPine, redondeoCharacter al entero más cercano con mínimo1, doble semillalow/highEND y publicación por primer cierre exterior. ParejasCSV verificadas; sin compilación ni instalaciónPine.

Con Ccorrecto suministrado:

- Lite:25,164valores, error máximo9.46e-11, sin discrepancias de visibilidad.
- Character **antes del primer hueco de datos**:33,570valores, error máximo3.06e-10.
- Al incluir el reinicio de la serie a22:00UTC tras el hueco de sesión, la emulaciónCharacter diverge, hasta9.63puntos. No se ha identificado aquí la causa interna de ese tratamiento del hueco: no extrapolar la coincidencia previa como equivalencia completa.

En modoautomático, el casoC54predicho61 introduce error de curvas incluso antes del hueco (máximosLite1.57puntos yCharacter1.61puntos). Un motor de curvas correcto conCmanual no valida su generadorCautomático.

El script utiliza la resolución del gráfico; no replica de forma probada fuente independiente, fallback, todos los perfiles, señales o estadosintravela del comprado. No se compiló ni probó en vivo esta entrega durante la auditoría.

## 6. Tabla de la supuesta prueba en vivo

El informe declara START19:03:15,END19:23:30,15s y primera muestra19:26:45. Bajo esas mismas condiciones declaradas, las parejas ya verificadasC_cruce1903_15_c/d.csv y el motorv4emulado coinciden entre sí, pero **no con las lecturas numéricas escritas en el informe**:

| Canal | InformeGemini | CSVverificado/motorv4, redondeado2decimales |
|---|---:|---:|
|Lane3A|30868.31|30865.20|
|Lane3B|30868.29|30865.04|
|Lane2A|30868.49|30866.62|
|Lane2B|30868.43|30866.27|
|Lane1A|30869.16|30868.74|
|Lane1B|30868.98|30868.34|

La semillaENDlow del caso verificado es30864.25. La tabla requiere explicar la diferencia de configuración/timestamp o aportarCSVy capturas de anclas para auditar esa sesión. No se ha verificado que el ensayo en vivo relatado ocurriera como se describe. Incluso dos lecturas iguales a2decimales en una vela no establecen equivalencia absoluta de recorridos o del algoritmo generador.

## Decisión

Conservarv4como aproximación congelada y su motorLitecomo herramienta útil conCsuministrado, en el dominio comprobado. No adoptar las etiquetas «descifrado», «causa causal» o «equivalencia absoluta». Una revisión futura debe predecir controles de otro episodio antes de observarC; añadir otra condición literal54despuésdeestecontraejemplo mejoraajuste, no demuestra recuperación de la fórmula.

Scripts auditar_Gemini_v4.py, auditar_Gemini_v4_curvas.py y auditar_Gemini_v4_barrido15.py. SalidasGemini_v4_auditoria.json, Gemini_v4_curvas_auditoria.json yGemini_v4_barrido15_auditoria.json. Copias y hashes identifican exactamente esta versión. Cgeneral sigue desconocido.
