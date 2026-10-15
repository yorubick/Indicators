# Comparación numérica de las nueve posiciones de END

Análisis exploratorio con C ya conocido. No se ajustaron longitudes ni umbrales a sus valores y no se produjo una predicción ciega. Especificación: C_END15_COMPARACION_ESPECIFICACION.json.

Se calcularon ocho EMAs de referencia con periodos en velas [24, 89/3, 8, 89/9, 72/27, 89/27, 72, 89]. También se calculó esa familia multiplicada por cuatro, para conservar los tiempos de suavizado de las referencias anteriores de un minuto. Ninguna familia se presenta como las longitudes del autor; no se utilizaron periodos derivados del C observado para explicar ese mismo C.

## Contradicciones verificadas

| Familia de referencia | END comparados | C | Señales iguales |
|---|---|---|---|
| Periodos fijos en velas de 15s | 19:18:00 y 19:18:15 | 67 y 106 | Signos, pendientes, orden de ocho EMAs, tres posiciones de nube, orden de sus pares y ocho conteos de cruces desde START |
| Tiempos equivalentes a las referencias de 1m | 19:17:15, 19:17:30 y 19:17:45 | 67, 67 y 106 | La misma firma discreta completa descrita arriba |

La firma de la primera contradicción tiene precio debajo de las dos EMAs lentas y encima de las cuatro más rápidas; los cruces desde START son [22,14,27,25,40,38,8,14]. La firma de la segunda tiene precio debajo de las ocho EMAs y cruces [10,4,12,8,22,20,0,0]. Las distancias y anchuras continuas sí cambian y se conservan en el JSON.

Los signos de pendiente de una EMA estándar y de precio menos EMA actual son algebraicamente redundantes; no se cuentan como pruebas independientes. Los cruces y la ordenación añaden información, pero tampoco evitan estas contradicciones.

El color de la vela final y la dirección de su cierre respecto al anterior también tienen colisiones. Por ejemplo, 19:17:45, 19:18:00, 19:18:30 y 19:18:45 cierran al alza respecto al anterior y dan C=106,67,64,152. Por sí sola, la dirección local no selecciona C.

N módulo 3 también tiene colisiones: n=102,105,108 da C=67,67,152. En este barrido de nueve posiciones, N módulo9 y módulo27 no repiten valores, así que **no son identificables**: ausencia de colisiones aquí no valida esas reglas. No se ajustó una tabla de restos a los nueve C conocidos.

## Controles y alcance

Hay 535 velas de 15s anteriores a START cargadas en la exportación. Todo el historial desde su primer timestamp hasta el último END es contiguo. Cada ventana coincide exactamente en OHLCV con su exportación medida. Recalcular las EMAs partiendo del primer cierre más100 o menos100 conserva las firmas completas de las nueve posiciones en ambas familias. Es una prueba de sensibilidad, no un límite sobre el estado real anterior a la historia disponible. Los periodos más largos de la segunda familia todavía retienen parte de la inicialización.

Esta comparación descarta **estas firmas discretas de estas familias como explicación suficiente**. No descarta otras longitudes, EMAs en varias resoluciones, características continuas, el camino de precios completo, acumuladores ni una selección armónica más general. No se ha encontrado una regla defendible de C.

## Próxima prueba discriminante

La inspección nativa localiza el mínimo de origen30844.25 en **18:52:30**, dentro de la vela de un minuto marcada anteriormente como18:52. A las18:52:00 el mínimo es30847.75 y a las18:52:15 es30847.00. Por ello, seleccionar START18:52:00 incluye dos subvelas anteriores al mínimo real de esa vela.

La siguiente prueba concreta será fijar END19:17:45 y fuente15s, y barrer START18:51:45,18:52:00,18:52:15,18:52:30,18:52:45,18:53:00. Las primeras cuatro ventanas conservan el mínimo de origen y el mismo extremo/semilla de END; las siguientes lo excluyen. Se verificará la geometría de cada caja antes de interpretar C. Esto permitirá separar cambios anteriores a excluir el mínimo de cambios que coincidan con su exclusión. No se presupone que elegir exactamente el mínimo produzca un C especial ni que el borde sea el ancla oculta del autor.

La dependencia exclusiva de N ya quedó descartada en los controles anteriores de igual n y distintos C. Repetir pruebas de resto sin otras variables no es una nueva explicación suficiente. Otra vía queda abierta: comparar las distancias y anchos continuos con más controles independientes antes de proponer un umbral. Escoger un umbral que separe estos nueve C sería un ajuste retrospectivo.

Datos detallados: C_END15_comparacion_resultados.json. Código: comparar_C_END15.py. La comparación es local y no cambia el gráfico de referencia restaurado.
