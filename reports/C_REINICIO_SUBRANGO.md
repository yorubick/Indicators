# Selección de subrango: reglas explícitas y límites

13 octubre 2026. Datos: nueve controles15s conocidos del 12 octubre, con OHLCV verificado. Análisis local, sin nuevas mediciones ni cambiosTradingView, sin entrenamiento32 o validación reservada. No se encontró una fórmula de C.

## Etapa1: ¿el reinicio distingue los controles?

52 configuraciones: primer/último evento, reinicio en vela del evento/confirmación. Eventos: pivotes H/L de radios1/2/3, nuevos máximos/mínimos estrictos, máximo volumen, cruce ascendente de volumen sobre1/1.5/2/3 veces su EMA20. EMAvol inicializada en volumenSTART, alpha2/21; el cruce se evalúa frente a la media anterior. Pivotes confirmados solamente con velas dentro deEND.

El estado seleccionado contiene evento completoOHLCV, todos losOHLCV desde reinicio hastaEND, dt, END y extremosglobales. Omite la historia anterior y conteo total. Dos estados iguales conCdistinto refutan cualquier cálculo exclusivo de ese estado. También se contrasta C=n*f(estado), admitiendo +/-1segundo de cuantización.

Resultados:

- **44/52** configuraciones tienen contradicciones, tanto para f(estado) como para n*f(estado).
- Cuatro configuraciones de umbralvolumen3 no generan eventos en estos datos: ausencia de contradicciones no las valida.
- Cuatro configuraciones restantes corresponden a dos selectores distintos: **primer cruce sobre1 o1.5 veces EMAvol**. Evento y confirmación coinciden, por eso están duplicados. Estos estados distinguen los nueve casos; no proporcionan una fórmula.
- C=K*duración inclusiva del tramo, conKpositivo común y +/-1segundo: **ninguna configuración explica los nueve controles**.

### Contraejemplo concreto, END19:23:45 UTC

START19:03:15 daC88 y START19:03:30 daC61.

El primer pivoteL radio1 en ambos rangos está en19:05:00. Reiniciar allí selecciona exactamente las mismas76velas OHLCV; también son iguales susH/Lglobales. Por tanto un reinicio que olvide el prefijo salvoH/L no explica88vs61. Si conserva una semilla o estado calculado antes del evento, esta prueba no lo excluye.

El primer nuevo mínimo estricto en ambos rangos está en19:09:45 y selecciona las mismas57velas; tampoco basta por sí solo.

Los dos selectores de volumen que distinguen los casos son:

| Umbral | START19:03:15, C88 | START19:03:30, C61 |
|---|---|---|
| 1xEMAvol | evento19:05:00, 76velas | evento19:04:00, 80velas |
| 1.5xEMAvol | evento19:09:45, 57velas | evento19:04:30, 78velas |

La media de volumen parte de valores diferentes (138 frente64). Esa inicialización hace variar el primer evento. No demuestra que el indicador use este mecanismo: varias reglas pueden producir estados distintos sin calcularCcorrectamente.

## Etapa2: cálculo de C sobre los tramos seleccionados

Se registró una segunda prueba después de la auditoría de estados, conservando los dos selectores anteriores. Sobre cada tramo se recalcularon las22características de volumen ya definidas (concentración, relativosSTART/END/media/EMA20, dispersión, correlaciónprecio-volumen y desvíoVWAP). FórmulaC=K*n_seleccionado*dt*10/183*característica, unKpositivo compartido y +/-1segundo.

**0/44** modelos tienen un intervaloKcomún factible. Seleccionar un tramo mediante esos cruces no rescata esa familia de fórmulas. No se afirma una refutación de todas las funciones posteriores al selector.

## Qué queda concretamente abierto

No hay aún una regla completa validada. Los candidatos de reinicio deben especificar si conservan una semilla calculada desdeSTART; los dos primeros cruces de volumen son selectores concretos no refutados por colisión, pero su mapeo simple aCfalló. Antes de medir más anclas, un nuevo mapeo debe explicar la matriz entera, incluida C67/67 conEND19:23:30 frente88/61 conEND19:23:45. No elegir reglas por número de estados distintos ni añadir valoresCcomo excepciones.

Artefactos: probar_C_reinicio_subrango.py, C_reinicio_subrango_preregistro.json, C_reinicio_subrango_resultados.json; probar_C_subrango_volumen_mapeo.py, C_subrango_volumen_mapeo_preregistro.json, C_subrango_volumen_mapeo_resultados.json. Ambos scripts aceptan --spec antes de ejecución. Las etiquetas ya eran conocidas: preregistro de reglas de cálculo, no validación ciega.
