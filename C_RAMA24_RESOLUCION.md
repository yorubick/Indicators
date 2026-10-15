# Control de resolución de la posible rama duración/24

13 octubre2026. Mediciones sobre12octUTC. Preregistro: `C_rama24_resolucion_predicciones.json`, generado por `predecir_C_rama24_resolucion.py` antes de medir. Análisis reproducible: `analizar_C_rama24_resolucion.py` y `C_rama24_resolucion_resultados.json`.

## Pregunta y cobertura

Dos casos originales de21velas1m daban C50: START19:02/END19:22 y START19:03/END19:23. Se repitieron con fuente y gráfico15s, CharacterManual/sourceChart/perfilB y Litefuente15s.

Un END1m incluye todo ese minuto. Para cubrir exactamente su intervalo físico, END15s debe ser :45, cuya vela termina al final del mismo minuto. También se midió END:00, que excluye las tres últimas velas nativas. START permanece :00. La agregación de cada grupo de cuatro OHLC15s coincide exactamente con los OHLC1m de los dos casos originales; no se mezclan fuentes ni series de precios distintas.

Predicción de la fórmula candidata `floor((END-START)/24)`:50en:00,51en:45. La hipótesis solo tiene sentido si esa rama se conserva entre resoluciones, algo que todavía no estaba demostrado.

## Resultado

|START UTC|END nativo15s|Velas15s|Predicción/24|C15s|C1m con minuto END completo|
|---|---|---:|---:|---:|---:|
|19:02:00|19:22:00|81|50|67|50|
|19:02:00|19:22:45|84|51|67|50|
|19:03:00|19:23:00|81|50|67|50|
|19:03:00|19:23:45|84|51|88|50|

Las dos filas:45 tienen cobertura completa equivalente a los respectivos casos1m. Por tanto, la diferencia entre resoluciones no desaparece al incluir todas las velas del minuto END.

Las cuatro parejas aceptadas tienen492512celdas de16curvas repetidas. Todos los OHLC seleccionados coinciden con el preregistro, los seis C de Lite concuerdan dentro de1e-7, las recurrencias tienen residuos<1e-8 y Character admite el mismo C en su intervalo de períodos redondeados. Parejas:1902:00c/d,1902:45c/d,1903:00g/h,1903:45c/d. No quedan fallos en esas parejas.

1903:00c/d y e/f fueron inestables durante recálculo y se preservaron sin aceptarlas. Se volvió a:00 desde:45 y se descargó g/h, estable y compatible. Capturas de fechas/minutos para:00 y capturas de anclas exactas:45 de ambos indicadores se conservaron en `manual/C_rama24_res_*`. Los segundos se fijaron arrastrando las anclas y se comprobaron en las etiquetas del eje, pues los campos de hora del diálogo solo muestran minutos. No se reaplicó el diálogo sobre las anclas:45.

## Qué restringe

1. Esta regularidad/24 observada en1m no se conserva automáticamente en15s. No debe incluirse como rama universal del generador.
2. La duración física del rango no basta para determinar C en estos casos: agregación/resolución y la estructura que conserva pueden importar. Cambiaron conjuntamente la resolución, el conteo y los OHLC por barra; estas mediciones no distinguen por sí solas entre una condición explícita de resolución y un cálculo sobre esas barras.
3. Los dos casos completos15s tienen el mismo dt15,84velas,H30870.75,L30849.00 y duración, pero C67 y88. Conteo, duración y extremos globales tampoco bastan juntos.
4. Con START19:03, añadir las tres velas19:23:15/30/45 cambia C67→88 sin cambiar H/L globales. Con START19:02, añadir19:22:15/30/45 conserva C67 aunque sí aparece un nuevo máximo30870.50→30870.75. Nuevo máximo no explica por sí solo la respuesta.

No se ha identificado la fórmula larga, ni demostrado una máquina de estados, ni aislado qué dato de15s utiliza el autor. Los controles1m se toman de las mediciones verificadas anteriores; en este turno no se volvió a medir su C. Los cuatro controles nuevos siguen siendo del mismo episodio, no réplicas de mercado independientes. La validación reservada no se usó.

## Próximo contraste dirigido

Mantener START19:03:00 y fuente/gráfico15s y medir END19:23:15 y19:23:30. Así se localizará cuál de las tres velas hace pasar67→88. Registrar antes sus OHLC y eventos causales y contrastar modelos explícitos sin introducir un umbral después de ver C. Es un barrido para localizar una transición, no una predicción de la fórmula general.

Se restauró y guardó fuente/gráfico1m, Lite1m, CharacterChart, ambas anclas12oct18:55–19:20UTC y el precio auxiliar original de Point2. No se actualizó Character. Captura: `manual/C_rama24_resolucion_restaurado.png`.
