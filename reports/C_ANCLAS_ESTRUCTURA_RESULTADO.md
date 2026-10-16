# Primera prueba de anclas estructurales

14octubre2026. NQ1!,12octubreUTC,Litev1.2sinactualizar,fuente/gráfico1minuto,copiaxqM5dZIf. Eventos identificados conOHLCsinusarCcomo selector;datos históricos y otras etiquetas ya eran conocidos,no es descubrimiento ciego. Interpretación operativa de la demostración pública,no implementación confirmada del detector privado.

## Eventos registrados

| Vela UTC | Evento operativo | Nivel |
|---|---|---:|
|18:45|High anterior al descenso|30886.50|
|18:47|Pausa/insidebar antes de nuevos mínimos;FSprovisional|L30875.25|
|18:52|Nuevo mínimo/origen candidato|30844.25|
|18:54|Primer máximo confirmado de recuperación|30861.50|
|19:05|Primera vela con cierre estrictamente sobre ese máximo|30863.00|
|19:07|Primer mínimo local tras ese cierre|30857.75|
|19:10|Retroceso más profundo de esa fase|30849.00|
|19:17|Último mínimo local antes de nueva expansión de cierre|30851.50|
|19:19|Cierre supera high19:05(30864.50)|30866.50|

Pivotsestrictosconfirmadosporunaveladecadalado;igualdad no cuenta como toma del extremo. La primera identificación llamó19:10primerpivot,lo cual fue incorrecto. Se conservó el registro original y se creó corrección separada antes de medir19:07. No se reemplazó un candidato por otro buscando C. El candidatoFSde18:47es una interpretación de la pausa de dos velas, no una definición confirmada del autor.

## Cajas y mediciones

| Interpretación | START | ENDincluido | n | C |
|---|---|---|---:|---:|
|Origen→primerpivot|18:52|19:07|16|60|
|Origen→retroceso profundo|18:52|19:10|19|62.29508197|
|Origen→últimopivot|18:52|19:17|26|62|
|PausaFSprovisional→mínimo|18:47|18:52|6|60|

Cada caja tiene4controles:START−/+1minuto yEND−/+1minuto.20configuraciones,40exportaciones. Las tres cajasAcompartenH30864.50,L30844.25yprimera ruptura alcistaenlavela19:19,pero duración,semilla y selección de eventos cambian.

Para la cajaAúltima:

| Control | Rango | C |
|---|---|---:|
|START−1|18:51–19:17|134|
|Base|18:52–19:17|62|
|START+1|18:53–19:17|107|
|END−1|18:52–19:16|109|
|END+1|18:52–19:18|125|

El C62 es mínimo frente a estos vecinos, pero eso no demuestra una alineación armónica ni que el software reconozca esas etiquetas estructurales. La identificación fue retrospectiva con una regla operativa provisional. La similitud62.295→62entre las dos mitigaciones no basta para inventar una conversión temporal: la primera está en rama corta y la segunda en rama larga.

Todos los15casos cortos se explican exactamente por la regla previa C=max(60,n×60×10/183),n<21. Primerpivot yFSprovisional y sus vecinos dan60;el retroceso profundo da62.295yvecinos60/65.574. Esta parte del experimento no discrimina el generador desconocido de la rama larga. Una réplica posterior a15s puede evitar ese mínimo,conservando cobertura de minutos completos y controles de resolución. No se efectuó aún esa réplica.

## Auditoría y limitación de datos

Dosexportaciones por configuración coinciden sobreOHLCVycursasLitecerradas. Se validó cobertura completa del rango y hora posterior,seisCindependientes concordantes(dispersión<10⁻⁶,RMSE<10⁻⁸),semillaENDlow/paradirecciónalcista yrecurrencia durante la primera hora,error<10⁻⁸. Visibilidad coincide con primera ruptura. Última fila excluida.

La igualdad global de volumen con elCSVhistórico anterior falló:la vela12octubre22:00tenía547yahora548,conOHLCidéntico. Es posterior a todos los horizontes experimentales;OHLCVyvolumendelrango/hora posterior coinciden exactamente. Ese fallo global se conserva enJSON,la interpretación por tramo se realizó después de detectarlo. No se atribuye la discrepancia a una causa confirmada ni se usa para afirmar independencia de todo el historial.

Regreso18:55–19:20reproduce exactamenteOHLCyseiscurvas/C62;conserva la discrepancia tardía de volumen. Fuente,versión yparámetros no se actualizaron. El indicadorCharacter no se usó como medida. Gráfico guardado y restaurado,NQ1!,1m;layoutprincipal sin cambios.

## Próximo paso

No surgió una regla predictiva defendible para un segundo setup. Suponer que otro anclaje correcto debe dar62sería extrapolar una etiqueta. Primero conviene repetir los tramos cortos con fuente/gráfico15s,usandoENDenlaúltimasubveladelminuto(XX:45) para cubrir los mismos minutos completos;distinguir ese cambio de resolución del cambio de ancla. Una regla nacida de esa comparación necesita luego predicción explícita en un setup nuevo.

Artefactos:identificación,preregistroycorrección separados;auditar_C_estructura.py/C_estructura_resultados.json;CSVmanual/C_estructura_*;capturas de precio sinLite y de las4cajas. Gráfico vectorialC_estructura_eventos.svggenerado desdeOHLCconeventos registrados,sin seleccionar conC;XMLverificado,previewSVGnoinspeccionado visualmente. CapturasTradingViewsíinspeccionadas.
