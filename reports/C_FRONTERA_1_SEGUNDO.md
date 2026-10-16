# Frontera de 19–20–21 velas con fuente y gráfico de 1 segundo

14 octubre 2026. Mediciones nuevas de Lite en la copia creada por el usuario:
https://www.tradingview.com/chart/xqM5dZIf/

## Resultado

NQ1!, sesión ETH, UTC, ajuste de contratos apagado. START fijo 14oct14:00:00 UTC. Gráfico1s y fuente explícita1s. Se conservó Litev1.2 cargado, con aviso de actualización; no se aplicó la actualizaciónv1.3. El layout principal no se modificó.

| Velas incluidas | END UTC | Predicción corta registrada | C medido |
|---|---|---:|---:|
|19|14:00:18|1.0382513661|1.0382513661|
|20|14:00:19|1.0928961749|1.0928961749|
|21|14:00:20|1.1475409836, solo control de continuación|1.0000000000|

La regla corta `C=max(dt,n*dt*10/183)` acertó los dos casos preregistrados. Con21velas el indicador abandona esa continuación, como en fuentes15/60/120s de los controles anteriores.

Veintiuna velas de1s tienen20segundos entre aperturas inicial/final, frente a5/20/40minutos en fuentes15/60/120s. Esto respalda una transición por conteo de muestras en estas observaciones. No identifica una operación concreta de20velas, un calentamiento universal ni el uso de armónicos. El descenso1.092896→1 recuerda que añadir una vela puede reducirC.

## Verificación

- Preregistro C_FRONTERA_1S_PREREGISTRO.json guardado antes de las mediciones.
- Anclas START y END exactas verificadas por etiquetas del eje; capturas C_1s_19_anchor.png, C_1s_20_anchor.png y C_1s_21_anchor.png.
- OHLC y volumen nativos completos/consecutivos en19/20/21velas. Los rangos19y20 son prefijos exactos del21, sin reconstruir velas a partir de otro intervalo.
- Parejas CSV estables en11columnas: OHLC,volumen y6plotsLite. Comparaciones18,469 /19,118 /20,350celdas respectivamente, sin diferencias.
- Las6estimaciones deC coinciden dentro1e-6segundos; residuos de recurrencia menores1e-8.
- Reconstrucción desde la mecha deEND, pasando por los cierres invisibles hasta la ruptura y600segundos posteriores: error máximo4.01e-11puntos, sin diferencias de visibilidad. No demuestra cuándo se calculóCinternamente.
- Se volvió de21a20 y de20a21. El retorno20 repite sus curvas, y las parejas c/d de21 coinciden con el primer caso21 en todos los timestamps cerrados comunes. Los archivos pending se conservan como diagnóstico y no sustituyen las parejas aceptadas.
- Hashes,OHLC,fits y métricas en C_frontera_1s_resultados.json. Analizador: analizar_C_frontera_1s.py.

Character conservaba anclas del12oct y carecía de cobertura1spara ese rango; emitió un error de cobertura. No se usó para corroborar estas mediciones. Se ocultó en esta copia. No confundir la coincidencia de6canalesLitecon una comparación independiente entre ambos indicadores. La copia quedó guardada en21velas; captura final manual/C_1s_final.png.

## Contraste de la fórmula nueva de Gemini

Propuesta recibida: `C=round(n*dt/18.3)+offset`, con offsets{-27,-18,-9,0,9,18,27}.

Se comprobó sobre los9controles anteriores de15s, permitiendo elegir cualquier offset por caso, sin exigir un selector. Resultado:1/9exactos;4/9dentro de1segundo. La propuesta literal falla aun sin discutir cómo selecciona el estado.

|n|dt|C conocido|Base redondeada|Offset necesario|
|---|---:|---:|---:|---:|
|82|15|61|67|-6|
|81|15|54|66|-12|
|83|15|88|68|+20|

Los offsets necesarios no pertenecen al conjunto propuesto. Es un rechazo de esa fórmula, no de toda relación armónica. Script probar_C_gemini_offset9.py, resultados C_gemini_offset9_resultados.json.

## Historial anterior a START y Replay

Sigue abierta la posibilidad de que la rama larga use información anterior aSTART. La nueva prueba no la excluye. Pero lasdosalternativas propuestas porGemini no son exhaustivas: también permanecen posibles otras operaciones del rango, series internas, selección de soluciones y datosEND→ruptura.

ArrancarReplayenun punto no basta para demostrar que el script perdió su historial anterior. Un protocolo que invoque un «corte de historial» debe verificar realmente qué datos deja disponibles, no asumirlo por la posición delcursorReplay. Los controles deReplayprevios ya establecieron estabilidad delresultado publicado, sin eliminar todas las entradas internas posibles.

## Siguiente contraste acotado

La frontera1sreduce el caso a21velas. Antes de ampliar barridos, repetir la transición20→21enotrosdosrecorridos1s elegidos solo por coberturaOHLC, conprediccionesC20=200/183 registradas antes de medir. No imponerC21=1 como ley: distinguir si es una transición que se repite y si el valor posterior depende ya del precio. Elegirlos después de conocer este resultado los convierte en réplicas prospectivas nuevas; conservar el fallo si lo hay.
