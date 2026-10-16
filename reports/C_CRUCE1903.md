# Cruce START/END alrededor de la frontera de C

13oct2026. Fuente/gráfico15s,12octUTC. Preregistro `predecir_C_cruce1903.py` y `C_cruce1903_predicciones.json`. Dos mediciones nuevas conEND19:23:30. Las columnasEND:45 son resultados verificados del barrido anterior.

|START|END19:23:30|END19:23:45|Cambio al añadir la misma vela final|
|---|---:|---:|---:|
|19:03:15|67, nuevo|88, previo|+21|
|19:03:30|67, nuevo|61, previo|−6|

Predicciones congeladas:67paraSTART:15 y61paraSTART:30. Resultado1/2; el modelo local completo falla. No se cambió su regla después de medir.

## Restricción matemática nueva en este cruce

Un modelo aditivo `C=f(START)+g(END)` exige que cambiar el mismo END tenga el mismo efecto en las dos filas. Aquí+21≠−6. Su diferencia de diferencias es27segundos. El modelo aditivo es incompatible con estos cuatro controles.

Un modelo separable multiplicativo `C=f(START)*g(END)` también falla: ambos START dan67conEND:30, pero dan distintos valores conEND:45. Se requiere una interacción en una explicación determinista de estos controles, no contribuciones independientes de cada límite.

Esto no demuestra que el indicador clasifique explícitamente un mínimo inicial y un pivote final. Al cambiar START cambian prefijo,conteo,duración e inicialización; al cambiar END cambianOHLCúltimo,conteo,duración y confirmaciónlocal. Un cálculo sobre el rango completo o sobre variables conjuntas podría producir la misma matriz. No identifica el generador ni una máquina de estados.

Todos los controles conservan H30870.75 yL30849.00. En una misma columna elENDOHLC es idéntico. EnEND:30ambas selecciones cierran30868.75; enEND:45cierran30866.50. Con los82datos deSTART:15/END:30C67 ySTART:30/END:45C61, ni(dt,n,H,L)sinotrasentradas basta.

## Verificación

`analizar_C_cruce1903.py` verificó OHLC exactos contra el preregistro,16curvas repetidas en parejasc/d, seis C de Lite dentro1e-7,residuos de recurrencia<1e-8 e intervaloCharactercompatible. Nuevos controles254336celdas repetidas;sinfallos. Ajustes e intervalos completos en `C_cruce1903_resultados.json`.

Anclas exactasSTART:15/:30 yEND:30 comprobadas en etiquetas del eje y guardadas para ambos indicadores en `manual/C_cruce1903_*_anchor.png`. No se reaplicó el diálogo sobre esas anclas. No se entrenó convalidación ni se actualizaron indicadores. Los controles todavía pertenecen al mismo episodio y no validan generalización a otro mercado/día.

## Siguiente prueba acotada

Completar otra columna END19:23:15 para los mismos START:15/:30. Preregistrar como hipótesis local que la primera vela de caída determinaC61en ambos rangos, antes de la recuperación:30 y la confirmación:45. Dos predicciones61/61, sustentadas en el control conocidoSTART19:03:00/END19:23:15C61. Si falla, conservar el fallo: no deducir una fórmula nueva solo reetiquetando los estados después.

En paralelo conviene usar esta matriz como prueba obligatoria de cualquier propuesta matemática. Añadir condiciones para acertarla no constituye descubrir el algoritmo; el candidato necesita predicciones en otro episodio conreglas congeladas.

Se restauró y guardó gráfico/sourceLite1m,CharacterChart/Manual/B, anclas12oct18:55–19:20UTC y ambospreciosauxiliaresoriginales. Captura `manual/C_cruce1903_restaurado.png`.
