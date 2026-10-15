# Matriz completa de la frontera local en15s

13oct2026. Fuente/gráfico15s, fechas12octUTC. En este turno se midieron dos selecciones nuevas conEND19:23:15. Se registraron predicciones61/61 en `C_cruce1915_predicciones.json` antes de medir. Resultado54/61:1/2; la hipótesis local completa falla.

|START|END19:23:15|END19:23:30|END19:23:45|
|---|---:|---:|---:|
|19:03:00|61|67|88|
|19:03:15|54, nuevo|67|88|
|19:03:30|61, nuevo|67|61|

Se conservan los fallos y no se sustituye la predicción original por54. Los demás valores son mediciones verificadas anteriores, no nuevos aciertos prospectivos.

## Qué aporta la columna

Excluir la vela19:03:00 manteniendoEND:15 cambia61→54, aunque ambas selecciones incluyen el mínimo local19:03:15. ConEND:30y:45excluir esa misma vela no cambiaC. Por tanto, la inclusión binaria de ese mínimo inicial no basta para decidir el valor.

Excluir después19:03:15 produce54→61conEND:15,67→67conEND:30 y88→61conEND:45. La misma modificación deSTART tiene respuestas distintas segúnEND. Se mantienen las restricciones de no separabilidad de la matriz anterior, pero no se identifica una ecuación ni el algoritmo del autor.

Todos los rangos tienenH30870.75,L30849.00. En cada columna coincidenENDOHLC y los datos posteriores. Conteo/duración/prefijo/inicialización cambian juntos al desplazarSTART. No permite atribuir causalidad solo a un pivote, solo a un precio inicial o solo a una vela.

## Verificación y dataset local

`analizar_C_cruce1915.py` aplica el mismo auditor parametrizado de `analizar_C_cruce1903.py`. Comprobó OHLC contra preregistro,16curvas estables en parejasc/d, dispersión de los seis C de Lite<1e-7,residuos<1e-8 e intervaloCharactercompatible. Nuevos controles255264celdas repetidas;sinfallos. Ajustes e intervalos en `C_cruce1915_resultados.json`.

`consolidar_C_matriz_frontera15s.py` reunió las nueve selecciones verificadas,OHLC completos,estado causal yprocedencia en `C_matriz_frontera15s.json`. No modifica el datasetmaestro93 ni sus particiones. Los nueve comparten la primera ruptura por cierre posterior aEND en19:26:45UTC, según el OHLC15s exportado. Esa coincidencia no excluye que el cálculo original use información entreEND y la primera publicación; esas entradas siguen sin aislarse.

Anclas exactas verificadas en el eje y guardadas en `manual/C_cruce1915_*_anchor.png` paraambosindicadores. No se reaplicaron diálogos sobre los segundos. No se actualizaron indicadores ni se volvió a puntuar la validación reservada.

## Dirección de investigación

La matriz es ahora un conjunto mínimo obligatorio para cualquier propuesta: debe producir61/54/67/88 sin introducir precios o timestamps específicos como excepciones. El siguiente trabajo útil es formular y contrastar una regla matemática conjunta de inicialización/procesamiento del rango, revisando las familias ya descartadas para no repetirlas. Seguir ampliando únicamente este mismo barrido no demostrará generalización.

Si un candidato supera estos controles, debe mantenerse congelado y predecir otra selección de otro episodio antes de medir. Ajustar una tabla de nueve entradas no constituye descubrirC.

Se restauró y guardó gráfico/sourceLite1m,CharacterChart/Manual/B, anclas12oct18:55–19:20UTC y ambos preciosauxiliaresoriginales. Captura `manual/C_cruce1915_restaurado.png`.
