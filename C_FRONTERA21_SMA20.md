# Frontera20→21: primera variación de una media20

13 octubre 2026. Investigación local con el dataset maestro existente, sin nuevas mediciones ni cambiosTradingView. Se usaron exclusivamente los11 controles de exactamente21velas de entrenamiento: nueve de60s, uno15s y uno120s. No se puntuaron los siete controles21 reservados ni se modificó el maestro.

## Parejas20→21 existentes y verificadas

Se buscaron casos20 de entrenamiento con mismoSTART/fuente y exactamente los primeros20OHLC del caso21. Se encontraron seis. Todos son del12octubre y los horarios son UTC:

| START | Fuente segundos | C20 medido | C21 medido |
|---|---:|---:|---:|
|06:00|60|65.57377049|77|
|18:00|120|131.14754098|137|
|18:59|60|65.57377049|77|
|19:00|15|16.39344262|16|
|19:00|60|65.57377049|77|
|19:02|60|65.57377049|50|

La transición no es una corrección siempre positiva ni un redondeo único de la continuación corta. La regla corta se conserva como referencia empírica, no se aplica a21 para fabricar predicciones.

## Hipótesis explícita

Una media móvil simple20 produce su primera muestra dentro del rango en la vela20 y su primera variación en la vela21. Eso propone un motivo comprobable para el umbral, sin afirmar que sea el motivo real.

Sea y0 la media de las velas0..19, y1 la media1..20 y x20 el precio impulsor de la última vela. Ajustar una sola actualización exponencial requiere:

`alpha=(y1-y0)/(x20-y0)`

`N=2/alpha-1`

`C=K*dt*N`

Se fijaron cuatro fuentes para el objetivo y el impulsor (close,HL2,HLC3,OHLC4), y dos políticas del coeficiente (positivo o valorabsoluto):32modelos. Se exige0<alpha<=1 y denominador no nulo, sin clipping ni fallback para rescatar casos. UnKpositivo común debe explicar los11C, permitiendo generosamente +/-1segundo por cuantización.

Este modelo es diferente del ensayo anterior de una EMA inicializada con una media y ajustada al precioEND: aquí la trayectoria objetivo esSMA20 y se ajusta su primera variación. No se ejecutó una nueva búsqueda de raíces.

## Resultado y contraejemplo

**0/32 modelos pasan los11controles.** Veinte variantes tienen coeficientes admisibles en todos ellos, pero sus intervalosKcomunes son vacíos. Las otras fallan cobertura.

En la variante close→close, positiva, dos casos de la misma fuente60s bastan:

| Caso | C medido | Período bruto dt*(2/alpha-1) | IntervaloK con +/-1s |
|---|---:|---:|---|
|06:01–06:21|80|160|[0.49375,0.50625]|
|19:04–19:24|50|2438.82352941|[0.02009165,0.02091172]|

Los intervalos son disjuntos. No se arregla esa variante eligiendo otra escala para15s o120s. Se verificó algebraicamente la actualización reconstruida conalpha sin valorabsoluto; la aritmética usa precios centrados para reducir cancelación numérica.

## Interpretación

Los controles mantienen la evidencia de un cambio al disponer de21velas, pero no identifican su operación. La hipótesis de ajustar la primera variaciónSMA20 queda rechazada en la familia definida. No se excluyen otras operaciones de ventana20, inicializaciones, series externas ni estado posterior aEND. Tampoco se demuestra que el original contenga una media20.

El siguiente candidato necesita explicar valores distintos deC21 con el mismoC20, y permitir tanto65.57377→77 como65.57377→50. Un relato de calentamiento sin cálculo numérico no basta. No abrir validación para ajustar excepciones ni considerar que acumular rechazos mide cercanía a la fórmula.

Reproducción: probar_C_frontera_sma20.py --spec; después sin argumentos. ReglasC_frontera_sma20_preregistro.json; datosC_frontera_sma20_resultados.json incluyen los11casos, seispares, coeficientes e intervalos. Etiquetas conocidas: exploratorio, no validación ciega. Fórmula generalC sigue desconocida.
