# Predicciones previas: relación local de C con el conteo

Hipótesis local, no generador descubierto: C=max(60, n*200/61) para fuente1m, con n igual al conteo inclusivo de velas. Motivación: los dos C decimales medidos con START19:00 y END19:18/19 coinciden con3800/61 y4000/61. Ya existe un contraejemplo al uso universal: START19:00 END19:20, n21, predice68.852459 pero da77.

Antes de medir los siguientes controles del12 de octubre de2026, se fijan estas predicciones para probar si el tramo decimal depende del conteo cuando se cambia START y se conserva END:

| START | END | n | Predicción C |
|---|---|---:|---:|
| 18:59 | 19:18 | 20 | 65.5737704918 |
| 18:58 | 19:18 | 21 | 68.8524590164 |
| 19:01 | 19:19 | 19 | 62.2950819672 |
| 18:59 | 19:19 | 21 | 68.8524590164 |

NQ1!, ETH, UTC, BADJ apagado; Lite fuente1m, Character perfilB Manual fuenteChart, gráfico1m. Se exige pareja repetida de16 curvas cerradas, OHLC completo y C Lite dentro del intervalo Character. Tolerancia de concordancia numérica con predicción1e-7 segundos.

Si falla una predicción, no modificar la pendiente ni añadir excepciones por caso. Registrar el contraejemplo. Coincidir en algunos controles apoya solo una relación local condicionada; deben identificarse sus condiciones y contrastarse en otro episodio antes de generalizar.

## Contraste posterior en episodio bajista, predicciones fijadas antes de medir
START04:45 END05:03, n19: C esperado62.2950819672. START04:45 END05:04, n20: C esperado65.5737704918. Mismas fuente/gráfico1m y fecha12 de octubre. No ajustar pendiente según resultado.

## Fuente15s: predicciones previas de normalización
Hipótesis a contrastar: C=max(dt,n*dt*10/183). START19:00 END19:04:30 n19: C15.5737704918; END19:04:45 n20: C16.3934426230; END19:05:00 n21: C17.2131147541 si continúa la pendiente. Hipótesis alternativa de frontera por conteo:21 podría abandonar la relación. No se predice valor concreto para esa rama. NQ1!,12 octubre2026 UTC, fuente/gráfico15s.

## Otra jornada: predicciones previas13 octubre2026
Fuente/gráfico1m, START19:00 END19:18 n19: C62.2950819672; END19:19 n20: C65.5737704918. La regla se fija antes de medir. Se conserva modoManual/perfilB,ETH,UTC,BADJoff.

## Fuente120s: predicciones previas12 octubre2026
NQ1!, fuente/gráfico2m, START18:00 END18:36 n19: C124.5901639344; END18:38 n20: C131.1475409836. END18:40 n21: continuación de relación137.7049180328; la hipótesis de cambio de rama predice abandonar la relación, sin predecir C concreto. Se registra antes de medir.

## Matriz rama larga: predicción local previa
Los C50/52/55 de START19:02 para n21/22/23 son compatibles con floor(2.4*n), sin identificar coeficiente único ni algoritmo. Predicción para END19:25 n24: C57. Para ventana desplazada START19:03 END19:24 n22: C52 si esa relación depende solo del conteo dentro de este tramo. Fecha12 octubre2026 fuente60s. Si falla, no reajustar2.4 por caso; comparar OHLC completos.

## Control de máximo global suficiente, antes de medir END19:26–28
START19:04 fijo, fuente1m,12oct. OHLC ya disponible muestra nuevos máximos19:26 y19:27;19:28 no supera el máximo19:27. Hipótesis restringida C=f(maxglobal,minglobal) predice igualdad C27=C28 si se confirman extremos iguales. No se predice C absoluto. Variar END cambia también conteo y OHLC; refutar igualdad descarta esa regla restringida, no toda selección de extremos.

## Invariancia al intervalo visible, predicción previa
12oct2026 UTC,NQ1!,ETH,BADJoff,START18:55 END19:20. LiteyCharacter con fuente explícita15s. Gráfico15s debe reproducirC106. Cambiar solo gráfico a1m debería conservar proceso nativo si las entradas son independientes delintervalovisible. Comparación principal:valor1m de aperturaT con15s enT+45s (última vela fuente delminuto); comparar tambiénT,T+15,T+30 como alternativas de muestreo predefinidas. No inferir períodos native15s contra cierres1m ni elegir desfase arbitrario por mejor ajuste. Volver a15s sin cambiarfuente para verificarperiodos.

### Control dirigido adicional: gráfico 30s, fuente explícita 15s (13 octubre)
Tras observar Lite C66 en gráfico1m y C106 en gráfico15s con mismas anclas, hipótesis exploratoria: Lite extiende END al final de la vela del gráfico, mientras Character conserva el END fuente. Predicción antes de medir: gráfico30s dará Lite C79 (incluye END19:20:15) y Character C106. Comparación de dos actualizaciones15s entre muestras30s; no ajustar contra cierre agregado. Esta prueba confirma o refuta esta predicción puntual, no demuestra código ni regla universal.

### 13 octubre: límite efectivo y semilla Lite
END nativo19:20:15 reproduce exactamente Lite gráfico30s END19:20:00; END nativo19:20:45 daC66 pero no mismos niveles que gráfico1m. Residuo inicial retroproyectado equivale a3.5puntos en seis curvas: low nativoEND45=30868 y low vela1mEND20=30864.5. Hipótesis antes de reconstrucción completa: C66, actualización15s después de19:20:45, semilla30864.5 reproduce curva1m. Control adicional predeclarado: START18:55, END19:21:00, fuente15s/gráfico1m LiteC66 (incluye última subvela21:45); gráfico15s END21:45 tambiénC66; semilla de minuto completo explica cualquier diferencia de niveles. No cambiar anclaCharacter ni extrapolar al generador general.

### START dentro de un minuto: contraste dirigido (13 octubre)
Lite fuente15s, END12oct19:04:45 fijo. Controles nativos: START19:00:00 incluye20velas -> C16.393442623; START19:00:15 incluye19velas -> C15.573770492. Cambiar solo gráfico15s a1m conservando START19:00:15 y END19:04:45. Hipótesis excluyentes: inicio minuto completo19:00 ->20velas/C16.393442623; respeta subvela15s ->19velas/C15.573770492; empieza en siguiente vela del gráfico19:01 ->16velas/C15. No usar igualdad de C para afirmar rango efectivo sin comparar OHLC, primeras muestras, curvas y semillas.

### 13 octubre: nuevas fronteras18–24 en dos tramos independientes
NQ1!,12oct2026,fuente/gráfico60s, Lite1m y CharacterChart perfilB Manual. START06:00 y14:00 fijos; END START+(n-1)min, n18..24. Predicción cuantitativa corta: n18C60,n19C62.2950819672,n20C65.5737704918. Para21..24 solo contrastar continuación corta (68.8524590164,72.1311475410,75.4098360656,78.6885245902); no predecir valor alternativo desconocido. Hipótesis umbral21: primera divergencia en21, pero ninguna universalidad demostrada. Medir curvas, coberturaOHLC, repetición16curvas, acuerdoLiteCharacter; preservar exportaciones obsoletas y repetir hasta tener pareja compatible. Tramos se eligieron antes de observar C; no seleccionar por resultado.

### Desplazamientos21 de dos nuevos tramos
Tras aceptar14controles18..24, medir ventanas12oct06:01–06:21 y14:01–14:21 (21velas) contra06:00–06:20 C77 y14:00–14:20 C62. Es diagnóstico de sustitución de primera vela por última, no predicción numérica de C desconocido. Contrastar conteo fijo, extremo global, cierre final y cambio de estructura; conservarOHLC para futuras hipótesis. No seleccionar ni descartar medición por valor obtenido.

### START barrido con END fijo en nuevos regímenes21
12oct, fuente/gráfico1m. Alcista END15:50, START15:27/28/29/31/32/33 (n24/23/22/20/19/18). Lateral END07:20, START06:57/58/59/07:01/02/03 (mismos conteos). Bases21:15:30C69 y07:00C75. Predicciones rama corta20C65.57377049,19C62.29508197,18C60. Hipótesis específica para refutar: si C depende exclusivamente de últimas21velas con END fijo, las extensiones22..24 conservan69/75 porque ese sufijoOHLC no cambia. No es una hipótesis completa del generador ni excluye conteo/prefix/externas. No predecir C largo por regla general desconocida. Preservar todos los controles; verificar estabilidad16curvas y acuerdoLiteCharacter.

### 13 octubre: conteo23 fijo alrededor del pico81
Fuente/gráfico1m,12oct. Base15:28–15:50 C81,23velas. Medir15:26–15:48,15:27–15:49,15:29–15:51 y15:30–15:52, siempre23velas. Contraste registrado: hipótesis local de que el conteo23 por sí solo produce el pico predice81 en las cuatro; no hay predicción de la fórmula general. Inspeccionar cambiosH/L yOHLC entrantes/salientes; no atribuir causalidad a extremos si varias entradas cambian. Todoscontrolesaceptados deben acordarLiteCharacter, repetir16curvas y cubrir23OHLC. Base81 ya repetidaindependientemente e/f.

### Cruces START/END tras deslizamiento23
NuevosC23:15:28–50C81,15:29–51C75,15:30–52C68; mismosH/L en esos3. Completar15:30–15:51 (22velas) y15:29–15:52 (24velas). Mediciones diagnósticas sin predicción exacta de generador; cruzar con existentes15:29–50C69,15:30–50C69 para separar cambios de un límite. No interpretar barrido como modificación causal del precio: cambian selección y conteo.

### 13oct: END15:51 fijo y extensión de START
12oct fuente/gráfico1m. Ya medidosSTART15:29 C75,n23 y15:30 C68,n22. NuevosSTART15:26,n26;15:27,n25;15:28,n24;15:31,n21. Contraste específico: si los datos anteriores a15:29 son irrelevantes para este rango, las tres extensiones darán75. Es predicción de irrelevancia del prefijo, no fórmula general ni convicción; registrar y preservar fallos. ParaSTART31 no predecir valor desconocido. ComprobarH/L iguales antes de atribuir diferencias a prefijo/conteo; coberturaOHLC, estabilidad16curvas, acuerdoLiteCharacter.

### Control de estabilidad al añadir15:52 con START fijo
Tras aceptarEND15:51:START15:27C93 y15:28C75, probarEND15:52 con ambosSTART. Predicción limitada de continuidad del estado:93 y75, respectivamente, porque añadir15:52 ya conservóCenSTART29/30. No es fórmula general ni garantía; falla si esos anclajes reaccionan distinto. Fuente/gráfico1m,H/L verificables; comparar además conteo25del nuevoSTART28 con conteo25START27END51C93. Repetir pico93desdeotra selección antes de incorporarlo como evidencia.

### Familia numérica explícita sobre dataset consolidado93
Partición fijada por consolidar_C_verificado.py antes de ajustar constantes:32largosentrenamiento/27validación,21cortosentrenamiento/13validación. Cortos usan max(dt,n*dt*10/183). Largos: C=quantize(K*(n*dt*10/183)*g(r,ER)); r=correlaciónPearson(precio,índice), ER=recorrido neto absoluto/suma cambios absolutos. Preciosclose/hl2/hlc3/ohlc4, ventana completa oúltimas21. g explícitas:1,1±abs(r),1±r²,1/(1±abs(r)),1/(1±r²),sqrt(1-r²),1/sqrt(1-r²),1±ER,1/(1±ER),ER,r². cuantizaciónnearest/floor/ceil. K único soloentrenamiento; necesariointerseccióndeintervalos paraaciertoexactodecadaC. No seleccionar/reglarporvaloresvalidación. Ningúnsuelo globaldt enramalarga. Familia exploratoria definida por nosotros, no inferidacomo códigooriginal. No actualizar constantespararescatarfallos.

### Familia nueva de volumen antes de ejecutar ajuste
ExtraerVol1m existente, repetirCSV y exigirOHLCidénticosal dataset antes de unirvolumen. Mantenermisma particiónpor episodios. C largo=quantize(K*n*dt*10/183*F). F:participación n/Neff e inversa,VolEND/mean e inversa,VolSTART/mean e inversa,EMA20Vol/END e inversa,EMA20/mean e inversa,1+CV/inversa,1±abs(corr(close,volume)),1±corr² y sus inversas,1+desvíoVWAPnormalizado por rango ostdprecio. EMA20se iniciaenmedia20 yactualiza2/21post20; definicióncandidata,nocódigodemostrado. nearest/floor/ceil;Kcomún soloentrenamiento e intersecciónnecesariadeintervalos. Noajustarvalidación;nofloor largo. Se excluyefuentes15/120paravolumennoexportado.

### Nuevos controles prospectivos sin eventos definidos
C_sin_evento_predicciones.json fija selecciónOHLC-onlyde13oct,dosrangosno solapadosno usados en93.1:START06:00 END06:20->06:21;2:START06:25 END06:45->06:46, fuente/gráfico1m,n21->22. No nuevosH/L ni nuevo pivoteH/Lradio1al añadir última vela;rangos61.00 y30.75pts. PredicciónregistradaantesmedirambosC:deltaC=0 si estos cuatroeventos soncondiciónnecesariadecambio. Hipótesisoperacional,no generadorCcompleto; cualquierdiferencia >1e-7refuta paraesedefinido detector. Ventanas no formanpartedel ajuste ni de27validaciónreservados; no calibrarconellas.

### Evolución87->84: predicciones locales antes de nuevosEND
C_evolucion87_predicciones.json fija START13oct06:25 y END06:47/48/49/50 fuente/gráfico1m. Calibración únicamente en87a06:45 y84a06:46: pendiente-3 por paso; cuatro hipótesisC=A-3*edad conAglobalH120,globalL102,pivotH90,pivotL93. Predicciones respectivas:END47=(81,81,81,90);48=(120,78,78,87);49=(117,75,87,84);50=(114,72,84,81). Extrapolaciónlinealporconteo81/78/75/72. No retocarinterceptos ni pendiente trasmedir. Son hipótesislocales no generador universal. HipótesisGemini de retroceso cuantificada: tendencia=closeanterior-closeSTART,cuerpoEND=close-open; si signosopuestos exigirdeltaCentre20y57. Para47/49/50esretroceso conesa definición;48no. Regla18??n>20todos. Conservarfallos,pivotes/extremos/OHLC completos.
