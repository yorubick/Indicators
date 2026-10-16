# END fijo y extensión/recorte de START en15s

13oct2026. END12oct19:23:45UTC fijo, gráfico y fuente15s. Baseline previo: START19:03 C88. Preregistro `C_prefijo192345_predicciones.json` generado antes de las dos mediciones nuevas por `predecir_C_prefijo192345.py`.

Se predijo88 en START19:02 y19:04 bajo una hipótesis local de suficiencia: conservar las últimas21velas, extremos globales, edades de extremos/pivotes radio1 y cierreEND conservaríaC. El criterio general de sufijos ya había fallado en otras pruebas; aquí se comprobó específicamente si explicaba el pico88 y su pivote terminal.

| START UTC | END UTC | Velas15s | C | Predicción |
|---|---|---:|---:|---:|
|19:02:00|19:23:45|88|79|88|
|19:03:00|19:23:45|84|88|Baseline conocido|
|19:04:00|19:23:45|80|61|88|

La predicción falla en2/2 nuevos casos. La suficiencia local queda refutada.

## Entradas conservadas

Los tres rangos comparten las últimas80velas completas desde19:04:00 hasta19:23:45, no solo las21 del criterio preregistrado. Sus timestamps y OHLC son idénticos. Descriptor común:

- H30870.75,L30849.00,cierreEND30866.50.
- Edad del máximo global5velas; del mínimo54velas.
- Edad del último pivote alto radio1:5velas; del último pivote bajo:1vela.
- Mismo END y mismas velas de la secuencia67→61→67→88 observada con START19:03.

Lo que cambia entre selecciones es el prefijo incluido, el conteo y la duración, además de cualquier estado/semilla inicializado desde START. No se puede atribuir el resultado a los precios del prefijo por separado: estos controles no mantienen el conteo constante. Tampoco identifican entradas externas al rango.

La diferencia79→88 es9 y88→61 es−27; esos números por sí solos no demuestran un algoritmo en base3. No se ha ajustado una fórmula de offsets para rescatar los fallos.

## Verificación

`analizar_C_prefijo192345.py` verificó OHLC exactos frente al preregistro,16curvas estables en parejasc/d, dispersión de los seis C de Lite<1e-7, residuos de recurrencia<1e-8 y acuerdo con Character. Nuevos controles:251296celdas de curvas repetidas. No quedan fallos. `C_prefijo192345_resultados.json` conserva ajustes e intervalos.

Anclas exactas END:45 verificadas en el eje y guardadas para ambos indicadores en `manual/C_prefijo192345_*_anchor.png`. No se reaplicó el diálogo sobre:45. El baselineC88 se toma de su medición verificada anterior, no se contabiliza como nueva réplica. No se usaron los27largos de validación reservada. Los tres controles siguen siendo del mismo episodio de mercado.

## Dirección siguiente

El pico no se puede explicar solo por el pivote terminal y los80OHLC finales. El contraste siguiente más localizado es retirar individualmente las cuatro velas19:03:00/:15/:30/:45 con END fijo: START19:03:15,19:03:30 y19:03:45. Permite localizar dónde cambia88→61. Debe registrarse antes de medir, sin convertir una transición observada después en una regla predictiva. Incluso ese barrido cambia a la vez conteo y precio incluido; no identifica por sí solo la fórmula general ni separa la contribución de ambos.

La configuración de referencia se restauró y guardó: gráfico/sourceLite1m,CharacterChart/Manual/B, anclas12oct18:55–19:20UTC yPoint2preciooriginal. Captura `manual/C_prefijo192345_restaurado.png`. No se actualizó Character.
