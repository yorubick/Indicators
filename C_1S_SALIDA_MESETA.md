# Salida de la meseta C=1 en una ventana nativa de1s

14 octubre2026. Litev1.2 cargado, sin actualizar; NQ1!, ETH, UTC, sin ajuste de contratos. Fuente y gráfico1s. START fijo14oct14:04:00UTC, copia de trabajo https://www.tradingview.com/chart/xqM5dZIf/ . No se modificó el layout principal.

## Resultado completo

Se midió cada conteo21..40, sin huecos. n21 se hereda de la réplica anterior;19selecciones nuevas:

|Conteo|ENDUTC|C|
|---|---|---:|
|21–32|14:04:20–14:04:31|1|
|33|14:04:32|2|
|34–35|14:04:33–14:04:34|1|
|36–40|14:04:35–14:04:39|2|

El primer C distinto de1 dentro de21..40 aparece en33velas. No es un escalón monotónico en estos datos: regresa a1y luego a2. No demuestra una máquina de estados ni queCsea siempre entero; puede existir una estimación continua cuantizada.

## Preregistros y criterios

C_1S_SALIDA_MESETA_PREREGISTRO.json congeló mediciones iniciales25/30/40con predicción1/1/1. Resultado1/1/2:2de3aciertos, hipótesis de meseta hasta40rechazada. Regla adaptativa registrada: completar los conteos31..39entre el último1 confirmado y el primer valor distinto.

Tras observar el pico33se añadió C_1S_MESETA_HUECOS_PREREGISTRO.json: completar TODOS los conteos no medidos22/23/24/26/27/28/29. Se registró1para esos siete y acertaron7/7. Es una extensión posterior al primer resultado, no parte del preregistro original. Fue necesaria para localizar el primer cambio dentro de21..40, en vez de asumir que los huecos anteriores eran1.

No se reestimó ninguna fórmula ni se omitieron conteos discordantes. Las mediciones intermedias de acotación no tenían prediccionesnuméricas registradas y no se cuentan como aciertosprospectivos.

## Restricción útil: mismos extremos y primera ruptura

Todos los conteos32..40 conservan:

- Máximo30529.25, mínimo30487.75 y tiempo de esos extremos.
- Primera ruptura posterior por cierre a14:05:26UTC, hacia abajo.
- START14:04:00 y fuente1s.

PeroCda1,2,1,1,2,2,2,2,2. Esos extremos, su antigüedad absoluta y esa primera vela de ruptura no bastan por sí solos. END,conteo,distancia temporal y últimoOHLCsí cambian; no se atribuye el cambio a una variable aislada.

La vela añadida para llegar33no crea un mínimo globalnuevo. El mínimo global se estableció en la vela de14:04:31, incluida en32velas. El Ccambia al añadir14:04:32y regresa al añadir14:04:33. Esto permite formular pruebas muy pequeñas de confirmación de pivote, estado y procesamiento del recorrido, pero el mero alineamiento temporal no demuestra causalidad de un pivote.

## Verificación

Se verificó cobertura nativa1sconsecutiva en cada rango y600segundos posteriores, OHLCV repetidos y6plotsLite repetidos, acuerdo de los6C<1e-6s yRMSEde recurrencia<1e-8. Todos los rangos son prefijos exactos del40.

La reconstrucción desde la mecha deEND conC suministrado reproduce curvas yvisibilidad; error máximo<6e-11puntos. El pico33se volvió a medir desde el rango29; sus nuevas parejasc/drepiten todos los plots yOHLCVcerrados comunes de los originales a/b. Se conservan las exportaciones iniciales y las de retorno con nombres diferentes.

El cálculo usa Lite solamente; Character no corrobora esta tanda porque conserva anclas de otra fecha sin cobertura1s. Se mantiene abierta la información previa aSTARTy entreENDy ruptura. No se realizóReplayni cambioDirection.

DatosOHLC,fits,hashes y métricas: C_1s_salida_meseta_resultados.json. Analizador: analizar_C_1s_salida_meseta.py. Capturas de anclas enmanual/C_1s_plateau_n*_anchor.png. La copia final queda en33velas para mostrar el primerpico.

## Siguiente contraste acotado

Cruzar START14:04:00/14:04:01conEND14:04:32/14:04:33. Primera fila ya medida:33velasC2 y34velasC1. Dos nuevas mediciones permitirían comparar un conteo32 y otro33 con los mismos finales. Una hipótesis basada solo enconteo predice1/2; una basada solo enENDpredice2/1. Deben registrarse antes de medir. Ambas son hipótesislocales incompletas; un fallo no permite simplemente introducir una excepción. Verificar los extremos porque moverSTARTpuede cambiar el máximo.

Estas dos mediciones NO se hicieron en esta tanda. Se propone este cruce para separar mecanismos con el caso pequeño ahora localizado.
