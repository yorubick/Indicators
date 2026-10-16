# Secuencia de C al completar19:23 en15s

13oct2026. Fuente/gráfico15s, START12oct19:03:00UTC fijo. Los END:00 y:45 se habían medido en el turno anterior; en este turno se midieron:15 y:30.

| END UTC | Velas | C | Cuerpo END | Confirmación de mínimo radio1 al END |
|---|---:|---:|---:|---|
|19:23:00|81|67|+0.50|No|
|19:23:15|82|61|−3.00|No|
|19:23:30|83|67|+3.75|No|
|19:23:45|84|88|−2.25|Sí, mínimo de:30|

En los cuatro rangos H30870.75 y L30849.00 se conservan. No hay nuevo extremo global ni confirmación de máximo en estos END. En:15 y:30 tampoco hay confirmación de mínimo bajo nuestra definición causal radio1.

## Preregistro y resultado

`predecir_C_transicion1923.py` guardó `C_transicion1923_predicciones.json` antes de medir. Se registraron dos explicaciones locales calibradas solamente en los extremos conocidos67 y88:

- Confirmación de mínimo al END selecciona88; sin ella selecciona67: predicciones:15=67,:30=67. Acertó1/2; falla en:15.
- Cuerpo END rojo selecciona88; en otro caso67: predicciones:15=88,:30=67. Acertó1/2; falla en:15.

Ninguna explica la secuencia completa. No se retocaron las reglas después de ver C61. La necesidad general de estos cuatro eventos ya había sido refutada en pruebas anteriores; este experimento solo evaluó explicaciones locales del salto final.

El salto67→88 aparece al incluir:45, donde se confirma el mínimo local de:30. Ambos hechos coinciden; no prueba que esa confirmación sea la causa. La caída67→61 ya ocurre una vela antes del rebote sin ninguno de los cuatro eventos definidos. Conteo, edades, cierre y otros componentes del precio sí cambian; no significa que no haya cambiado ninguna entrada del indicador.

## Verificación

`analizar_C_transicion1923.py` verificó OHLC exactos contra el preregistro,16curvas repetidas, seis estimaciones Lite con dispersión<1e-7/residuos<1e-8 y compatibilidad del intervalo Character. Parejas aceptadas:15=e/f,:30=c/d,248944celdas repetidas en total; no quedan fallos. Las anclas exactas:15/:30 de ambos indicadores se comprobaron en el eje y se guardaron en `manual/C_transicion1923_*_anchor.png`. Los campos de diálogo no muestran segundos y no se reaplicaron sobre esas anclas.

El resultadoC61 se repitió después de pasar por:30 y volver a:15. Las123664celdas comunes a la primera medición d y la repetición f son exactamente iguales. Primera pareja:15c/d también fue estable y se conserva. Preregistro/resultados: `C_transicion1923_predicciones.json` y `C_transicion1923_resultados.json`.

No se consultaron los27largos de validación reservada. Estas observaciones son del mismo episodio, no una réplica independiente del mercado.

## Un contraste adicional observado

END:00 y:30 tienen el mismo cierre30868.75 y C67, pese a sus distintos cuerpos/mechas y conteos. Eso merece revisar el papel del cierre, pero no convierte C en función exclusiva del cierre. Auditoría local de los32largos de entrenamiento: START19:00,dt60,END19:21/22 tienen el mismo cierre30868.50 pero C102/77. Sus máximos difieren, por lo que ese contraejemplo tampoco descarta una función conjunta del cierre y otros datos.

## Próximo experimento

Para separar la respuesta de la vela:45 de la historia previa, mantener END19:23:45,dt15 y desplazar START19:03 a19:02. La secuencia terminal y su confirmación de mínimo no cambian, mientras cambia el prefijo/conteo. Si una explicación depende solo del estado terminal que conserva, debería conservar88; si cambia, hay que identificar qué entrada del prefijo/conteo modifica la respuesta. Esa es una hipótesis local de suficiencia, no la fórmula general. Registrar OHLC y predicción antes de medir, sin seleccionar START en función del C nuevo.

Se restauró y guardó gráfico/sourceLite1m, CharacterChart/Manual/B, fechas12oct18:55–19:20UTC y precio auxiliar Point2 original. Captura `manual/C_transicion1923_restaurado.png`. No se actualizó Character.
