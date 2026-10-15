# C antes de la ruptura: auditoría de salidas disponibles

13 octubre 2026. Pregunta: ¿hay una salida que permita observarC entreEND y la primera ruptura, sin inferirlo de curvas que todavía no existen?

## Configuración y revisión de interfaz

NQ1!, gráfico1m, ETH, UTC, BADJ apagado. Character Tree v6.5.36 perfilB Manual fuenteChart; Lite1.2 fuente1m. Anclas12octSTART18:55 END19:20, mantenidas fijas. No se actualizó Character ni se cambiaron sus parámetros. Se revisaron Inputs y Style de ambos indicadores:

- Character ofrece etiquetas de temporalidades sobre sus EMA, pero no se encontró un campo C o una tabla diagnóstica. Las diez curvas principales están habilitadas.
- Lite no ofrece una opción de C/tabla en las pestañas examinadas.
- En replay antes de la ruptura, la ventana de datos muestra diez curvas Character vacías y Bull/Bear delivery active=0. Lite no expone allí un escalarC adicional.

La revisión es de las salidas accesibles en estas versiones/configuración. No equivale a inspeccionar variables internas del código protegido ni todos los indicadores recibidos.

## Nueva prueba: todas las columnas y avance secuencial

Se inició replay solicitando12oct19:24 y se avanzó dos veces con Forward, sin mover las anclas. No se repitió una extracción deC posterior a ruptura; se buscaron salidas anteriores, incluidos plots de resplandor y las columnas de actividad que no formaban parte de las16curvas usadas para inferirC.

Se exportaron dos veces los tres estados. Se excluyó siempre la última fila, por el estado parcial/desfase ya registrado. Timestamp real de losCSV, no inferido del corte pedido:

| Estado | Última apertura exportada, excluida | Última apertura usada | Celdas de las26curvas no vacías desdeEND |
|---|---|---|---:|
| Inicio, corte19:24 | 19:23 | 19:22 | 0 |
| Forward1 | 19:24 | 19:23 | 0 |
| Forward2 | 19:25 | 19:24 | 0 |

Cada exportación tiene34columnas: timestamp, cuatroOHLC, seiscurvasLite, diezcurvasCharacter, diezresplandoresCharacter, dosflagsdeactividad yVolume. No hay una columna escalarC.

Las parejas coinciden exactamente en **44,472 celdas** de todas las columnas para timestamps cerrados comunes. LosOHLC deSTART..END están completos y coinciden con la referencia histórica; también se verifican losOHLC comunes posteriores. Las26curvas permanecen vacías desdeEND en todos los estados, incluidos los resplandores. Las dosflags valen0, que describe actividad de entrega, noC.

La referencia previa identifica primera ruptura/publicación en19:26. No se volvió a extraer C62 después de esa ruptura en esta tanda: hacerlo no resolvería la pregunta previa.

## Conclusión y límites

**No se encontró una salida observable deC antes de la ruptura en los canales examinados.** La prueba queda inconclusa sobre cuándo se calcula internamente y sobre si usa las velas entreEND y ruptura. Ausencia de curvas no significa C=0 ni queCnoesté calculado.

La recomendación del otro chat es correcta como control de supuestos; ahora queda documentada su limitación concreta con las salidas adicionales. No usar la estabilidad posterior como prueba de independencia de datos posteriores aEND.

La siguiente tanda debe volver a la frontera20→21 en vez de ampliar la matriz80velas. Primero reunir los controles21 ya medidos en15/60/120s y exigir a una regla explícita valores numéricos conjuntos. Si necesita un estado posterior aEND, debe declararlo y confrontarlo con los datos de ruptura disponibles. No asumir que las únicas entradas son losOHLCV del rango.

## Artefactos y restauración

Script analizar_C_salidas_prebreak.py y salida C_salidas_prebreak_resultados.json. SeisCSV manual/C_prebreak_salidas_1924_a/b.csv, step1_a/b.csv y step2_a/b.csv. EvidenciaUI manual/C_prebreak_ventana_datos_1923.txt y .png.

Se salió de replay, se cerró el panel de datos y se conservaron fuente/gráfico1m, anclas18:55–19:20, preciosauxiliares y versión del indicador. El layout indicó All changes saved. Evidencia final manual/C_prebreak_restaurado.png. No se modificó el dataset maestro ni se ajustaron modelos usando validación reservada.
