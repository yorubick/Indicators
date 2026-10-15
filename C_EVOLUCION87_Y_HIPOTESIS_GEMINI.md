# Evolución87→84 y contraste de las tres hipótesis

13 octubre2026. Se revisaron las hipótesis compartidas y se extendió la selección START13oct06:25 en gráfico/fuente1m, manteniendo START fijo. Lite1m, Character v6.5.36 perfilB Manual fuenteChart,ETH,UTC,BADJapagado yReplayapagado. CuatroEND nuevos, más dos controles anteriores. No se obtuvo la fórmula generalC.

## De dónde obtener una regla específica

Una regla debe especificar variables, cálculo y dominio antes de medir nuevosC. Los dos datos87/84 permiten calibrar una pendiente local−3, pero no elegir cuál variable la causa: en esa transición aumentan por1 el conteo y todas las edades. Se definieron cuatro modelos distintos,C=A−3×edad, sobrehigh/low global yúltimohigh/low local confirmado. Sus interceptos se fijaron usando únicamenteC87y84:120,102,90y93 respectivamente. La extrapolación por conteo predice81/78/75/72.

Los cuatro modelos coinciden en los dos datos de calibración, pero las confirmaciones posteriores separan sus predicciones. Eso es una forma comprobable de transformar una observación en hipótesis, no una identificación del algoritmo original. No se reajustaron pendientes ni interceptos después de observar los resultados.

## Evolución medida con START fijo

| ENDUTC | Velas | C | Eventos principales |
|---|---:|---:|---|
|06:45,control previo|21|87|Confirmaciónhigh local|
|06:46,control previo|22|84|Ninguno de los cuatroeventos|
|06:47,nuevo|23|84|Confirmaciónlow local|
|06:48,nuevo|24|83|Nuevohigh global|
|06:49,nuevo|25|84|Confirmaciónhigh local|
|06:50,nuevo|26|84|Ninguno de los cuatroeventos|

La bajada87→84 no continúa−3 por vela. La extrapolación por conteo falla4/4. Los modelos de edadglobalH/globalL fallan4/4; edadpivotH yedadpivotL aciertan1/4cada uno. Ninguno explica la evolución completa. No se afirma que edades no puedan intervenir en una función distinta,no lineal o por estados.

Las edades ylos cuatroeventos se calculan con la misma definición de la base experimental:extremos globales estrictos y pivote radio1 estricto a izquierda, empate permitido a derecha. Otra definición necesita registrarse como candidato distinto.

## Hipótesis1: duración dividida entre24

La fórmula `floor((n−1)*Δ/24)` reproduce los siete casos seleccionados de consolidación anterior. Esto ya se corroboró en `GEMINI_ESTADOS_V2_BASE.md`. Falta una condición que identifique esa rama sin observarC; el clasificador R<=22.25/sin nuevohigh produce tanto aciertos como falsos positivos. La identidad24=72/3 en la familia de períodos no prueba que esa sea la operación usada para generarC.

No se rechaza esta fórmula para un dominio aún por definir. Tampoco se puede convertir su acierto en siete casos seleccionados en una regla universal de compresión.

## Hipótesis2: todo retroceso expandeC20–57segundos

Se fijó una definición precisa antes de los nuevos ensayos: tendencia neta previa=close de vela anterior−close de START; colorEND=close−open. Retroceso si tienen signos opuestos. La hipótesis exige deltaCentre+20y+57.

Entre los datos ya medidos existen contraejemplos con STARTfijo:12octSTART15:30,END15:50→15:51,C69→68pese avela roja contra avancealcista;12octSTART06:00,END06:20→21y21→22,velas verdes contra caída, C77→77. El salto69→93 existe con START15:27,pero no representa la respuesta de todas las selecciones al mismoEND.

En las cuatro nuevas mediciones aparecen tres retrocesos según la definición registrada:

| END13oct | Tendencia previa | CuerpoEND | CambioC | Predicción+20..+57 |
|---|---:|---:|---:|---|
|06:47|−10.25|+19.50|0|Falla|
|06:49|+16.25|−3.50|+1|Falla|
|06:50|+13.25|−6.50|0|Falla|

La regla universal queda refutada,3/3fallos prospectivos. Otra definición de tendencia o retroceso es posible, pero debe fijarse antes de medir yproducir la magnitud delC,no solo una etiqueta.

También distinguir color devela y cambio respecto al cierre anterior:19:22del12oct tieneopen30868.75yclose30868.50,cuerpo−0.25 y nuevohigh por mecha. Describirla como verde por su máximo mezcla variables distintas.

## Hipótesis3: escala en potencias de3

En el conjunto consolidado,17de59valores largos son múltiplos de3; en el subconjunto1m son17de57. Hay82,68,77,83,128y134,entre otros,no divisibles por3. Los valores75=3×25,87=3×29y93=3×31no son potencias de3:son algunos múltiplos. En la secuencia citada82→81es−1 y75→68es−7.

Esto refuta una rejilla universal de múltiplos de3,pero no toda fórmula que use factores3o divisores3/9/27. La arquitectura de períodos ya usa esos divisores; no demuestra el origen deC. Para una hipótesis armónica útil hay que definir cómo obtiene los coeficientes o desplazamientos de precios/tiempos y predecirC,fijando las excepciones antes.

## Verificación y reproducción

Las cuatro parejas nuevas son estables en174,288celdas de16plots cerrados. CoberturaOHLC completa eidéntica al preregistro,seisC Liteconcordantes,pertenencia al intervaloCharacter,sin fallas pendientes. La última fila se excluye.

El casoC83END06:48 se repitió desdeEND06:50; parejae/fcoincide exactamente con la primerad en43,552celdas yrecupera83. Se conserva la primera pareja c/d ylos pending. Las calibraciones87/84usan sus parejas repetidasprevias, no se cuentan como nuevos aciertos.

`predecir_C_evolucion87.py` ->`C_evolucion87_predicciones.json`; `analizar_C_evolucion87.py` ->`C_evolucion87_resultados.json`. Protocolo en `C_DECIMALES_PREDICCIONES.md`; CSV/capturas `manual/C_evolucion87_END0647/0648/0649/0650_*`.

Layout restaurado yguardado en12oct18:55–19:20,gráfico1m,Lite1m,CharacterChart,Replayapagado. Captura `manual/C_evolucion87_restaurado.png`.

## Qué orienta el siguiente candidato

AquíCse estabiliza alrededor de84 después de bajar87→84,pese a cambios de edad,confirmaciones,nuevohigh ycolores contrarios. Esto es compatible con una estimación numérica redondeada o una salida cuantitativa de estados,pero no distingue ambos mecanismos. No se puede concluir que la fórmula sea continua ni discreta solo por mesetas.

Conservar el candidato de duración/24 para una rama,pero su siguiente mejora debe explicar la clasificación yel valor de otra rama con una operación observable. Las otras dos hipótesis,como reglas universales,tienen contraejemplos. Cambiar umbrales o elegir solo los casos que encajan no aportaría esa operación. Los27controles largos reservados no se usaron para ajustar estos candidatos locales.
