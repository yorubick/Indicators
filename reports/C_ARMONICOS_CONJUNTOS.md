# Armónicos conjuntos 1–3–9: prueba acotada

14 octubre 2026. Trabajo del segundo chat con los nueve controles conocidos de C_matriz_frontera15s_volumen.json. No hubo nuevas mediciones del indicador ni cambios en TradingView. Etiquetas ya conocidas, ventanas solapadas de un episodio: exploración, no validación ciega.

## Hipótesis distinta del ensayo FFT anterior

El ensayo previo buscaba un pico o descriptor de potencia y lo convertía aCcon una escala común. Aquí se ajusta simultáneamente al cierre:

`precio(t)=a+b*t+sum_h[A_h*cos(2*pi*h*t/P)+B_h*sin(2*pi*h*t/P)]`

Modelo principal h=1,3,9; controles h=1 y h=1,2,4. Amplitudes/fases y período se eligen por mínimo residuo de precio; la función de ajuste no recibeC. La tendencia se ajusta conjuntamente. Pse busca entre18.000001 y4nvelas, usando el mismo dominio para los tres modelos. La cota inferior permite resolver el noveno armónico por debajo deNyquist. No se afirma que el autor use este modelo, ese dominio o mínimos cuadrados.

Se congeló el protocolo antes de ejecutar el contraste inicial: C_armonicos_conjuntos_preregistro.json. Script probar_C_armonicos_conjuntos.py. Mallas721/2161 logarítmicas, refinamiento de todos los mínimos locales observados con60iteracionesgolden-section. Estos resultados numéricos estables no son una demostración de optimización global sobre todo el continuo.

## Conversión numérica puesta a prueba

`C=K*dt*P`, con Kpositivo común a los nueve casos. Se permiteCobservado+/-1segundo: cubre generosamente los redondeos usuales al entero. No hay piso universalC>=dt en la rama larga.

Ninguno de los tres modelos admiteKcomún:

|Modelo|Máximo límite inferiorK|Mínimo límite superiorK|
|---|---:|---:|
|Una componente|0.0813232|0.0497168|
|Componentes1,3,9|0.0684720|0.0168287|
|Control1,2,4|0.0951576|0.0605716|

Un intervalo admisible necesitaría límite inferior<=superior. Aquí son incompatibles.

En el par END19:23:45:

|START|C observado|Pajuste1,3,9,velas|
|---|---:|---:|
|19:03:15|88|84.706103|
|19:03:30|61|245.612768|

El estimador cambia de período aproximadamente3veces mayor, peroCdisminuye. Esto puede reflejar ambigüedad de fundamental/armónico del propio ajuste. No es evidencia de que el indicador cambie de armónico y no permite obtener88/61con una escala común.

## Extensión explícitamente posterior al primer resultado

Se comprobó después si elegir libremente una componente podía rescatarlo:

`C=K*dt*P/h`, hpertenece a1,3,9.

Se permite elegir cualquierhpor caso, incluso sin exigir una regla de selección. Cada caso aporta una unión de tres intervalosK; su intersección para los nueve es vacía. Por tanto tampoco hay una selección entre esas tres componentes que haga compatible la conversión con el estimadorPcalculado. No se vuelve a seleccionarPusandoC.

La extensión está etiquetada como suplementaria en elJSON; no se presenta como parte del preregistro inicial.

## Comprobaciones y límites

Todos los datos tienen conteo y timestamps consecutivos compatibles con fuente15s. LosPde las dos mallas difieren relativamente menos de1.36e-8; para el modelo1,3,9, menos de3.63e-9. Una señal sintética con fundamentalP36 y componentes1,3,9 recupera36dentro1e-5; sumar10000y multiplicarpor2conserva eseP.

No comparar menores residuos de un modelo con más parámetros como prueba de armónicos del mercado. No se auditó de nuevo la extracción originalCen esta tanda: se usa la matriz verificada existente. No se probó fase de filtrosEMA, ondas geométricas no sinusoidales, otras fuentes, armónicos fuera del dominio, selección de subrango ni precios posteriores aEND.

## Siguiente contraste que sigue abierto

La transformación de precio propuesta permite contrastar la invariancia esperada de este tipo de cálculo armónico normalizado. El modeloGemini v4predice50→77al duplicar todos los precios del caso1m19:02–19:22; un mecanismo exclusivamente invariante aescala predice50→50. Antes de interpretarlo deben pasar los controles de compatibilidad,OHLCyvolumen del protocolo de símbolos sintéticos. Esas mediciones no se hicieron aquí.

Resultados completos, períodos y testigos: C_armonicos_conjuntos_resultados.json. No se identificó la fórmula generalC ni se descartó toda hipótesis armónica.
