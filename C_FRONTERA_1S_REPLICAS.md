# Dos réplicas prospectivas de la frontera 20→21 en 1 segundo

14 octubre 2026. Lite v1.2 cargado, sin aplicar la actualización disponible; NQ1!, ETH, UTC, ajuste de contratos apagado. Gráfico y fuente explícita de 1 segundo. Copia de trabajo: https://www.tradingview.com/chart/xqM5dZIf/

## Predicciones y resultado

Antes de configurar las anclas se guardó C_FRONTERA_1S_REPLICAS_PREREGISTRO.json. Se eligieron dos inicios posteriores por hora, sin consultar sus valores C. Predicciones: C20=200/183 y C21=1 como hipótesis local de réplica, no como regla larga universal.

| START UTC | END20 / END21 | C20 medido | C21 medido | Predicciones |
|---|---|---:|---:|---|
|14:02:00|14:02:19 /14:02:20|1.0928961749|1|2/2|
|14:04:00|14:04:19 /14:04:20|1.0928961749|1|2/2|

Cuatro predicciones acertadas. Junto al primer caso de 14:00, la transición se repite en tres rangos disjuntos cortos de la misma sesión. Los nuevos casos rompen hacia abajo, mientras el primero rompía hacia arriba. Esto amplía el contraste direccional observado, pero no sustituye una intervención de Direction mode.

Ambas réplicas conservan sus extremos al añadir la vela21:

|START|Máximo|Mínimo|AperturaSTART|CierreEND20|CierreEND21|
|---|---:|---:|---:|---:|---:|
|14:02|30509|30497.25|30502.75|30502|30501.75|
|14:04|30529.25|30510.75|30526.5|30511.25|30513|

La vela añadida no amplía el máximo/mínimo; los cierres cambian en sentidos distintos y la transición C es la misma. Esto es compatible con cambio de cálculo por conteo, pero no identifica la fórmula de la rama posterior.

## Verificación

- Todos los timestamps del rango y los siguientes600segundos están presentes como datos nativos1s en ambas exportaciones. Los20OHLCV son prefijo exacto de los21 en cada réplica.
- Anclas exactas comprobadas en las etiquetas del eje; capturas manual/C_1s_r1402_n20_anchor.png y las tres restantes con los identificadores correspondientes.
- Dos exportaciones cerradas repiten OHLCV y6curvas:103246celdas entre los cuatro controles, cero discrepancias. Se conserva una exportación pending por caso como diagnóstico.
- Las6estimaciones deC coinciden dentro1e-6; cada ajuste de recurrencia tieneRMSE<1e-8.
- Reconstrucción desde ENDseed y cierres nativos a lo largo de600segundos: error máximo3.64e-11puntos y cero discrepancias de visibilidad frente a primera ruptura por cierre.
- No se usóCharacter para corroborarC: conserva anclas de la referencia original y no tiene cobertura de ese rango en1s.

Datos,OHLC,hashes y ajustes en C_frontera_1s_replicas_resultados.json; analizador analizar_C_frontera_1s_replicas.py. No se modificó el dataset maestro ni el layout principal.

## Qué significa y qué queda abierto

La regla corta se sostiene en nuevos controles1s y la transición21 aparece de nuevo. C21=1 puede ser resultado de saturación, cuantización o de una regla de la rama larga; las tres coincidencias no distinguen esas posibilidades. No afirmar que el precio nunca influye ni que se descubrió un warmup universal.

La siguiente pregunta útil es encontrar el primer rango1s de la rama larga que dé un C informativo distinto de1. Una expansión acotada del conteo, con criterios y predicciones previos, puede separar una meseta por cuantización de un comportamiento dependiente del recorrido. No se ejecutó esa expansión en esta tanda.

## Tests de Gemini pendientes

1. Recortar el viewport para que empiece enSTART no demuestra pérdida de historial interno enPine. SiCpermanece igual, no prueba que sea100%autocontenido; si cambia, tampoco identifica por sí solo variablesvar acumuladas desde la sesión. Deben verificarse datos disponibles y conservar todas las demás entradas. Los controles deReplayprevios establecieron estabilidad observable, sin eliminar todas las entradas anteriores o posteriores posibles.
2. Auto/Bull/Bear ya se contrastó para la dirección deFlowBands en el rango original1m deC62: mantuvo períodos y curvas. Script analizar_C_orden_direccion.py y C_orden_direccion.json. El propio analizador aclara que no es Setup direction deAutoBalanced. Antes de repetir el test hay que identificar el parámetro exacto. Un cambio de dirección forzada no cambia la presión de mercado ni losOHLC: cambia una entrada del indicador.

Ambos tests se conservan como trabajo posterior según pidió el usuario. No se hicieron nuevas pruebas deReplayniDirectionenesta tanda.
