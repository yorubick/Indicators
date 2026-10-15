# Localizar el cambio al retirar velas iniciales

13oct2026. Fuente y gráfico15s, END12oct19:23:45UTC fijo. Nuevas mediciones START19:03:15/:30/:45. START19:03:00C88 y19:04:00C61 son controles verificados de turnos anteriores.

|START UTC|Velas|C|Predicción interpolación local|
|---|---:|---:|---:|
|19:03:00|84|88|Baseline|
|19:03:15|83|88|81.25|
|19:03:30|82|61|74.50|
|19:03:45|81|61|67.75|
|19:04:00|80|61|Baseline|

La transición aparece entre START:15 y:30, al excluir la vela19:03:15. Excluir antes la vela19:03:00 no cambiaC. Excluir después la vela19:03:30 tampoco cambiaC. La interpolación numérica registrada antes de medir falla3/3; no se ajustaron coeficientes después.

## Qué cambió en esa frontera

Vela excluida19:03:15: O30857.00,H30857.00,L30852.75,C30854.50. La vela posterior19:03:30: O30853.75,H30857.00,L30853.00,C30857.00. El mínimo:15 es local, no el mínimo global30849.00, que sigue incluido. Cambia conjuntamente el conteo83→82, la duración y el estado/semilla que pueda iniciarse en START. No identifica por separado qué variable provoca la transición.

La vela:15 forma un mínimo local frente a:00 y:30 si se utiliza el vecino izquierdo. En START:15, ese vecino queda fuera del rango, peroC88 se conserva. Esto no exige que el autor use esa definición de pivote ni que restrinja su contexto a START; no demuestra una máquina de estados.

En todos los controles H30870.75,L30849.00,ENDclose30866.50 y la secuencia terminal son iguales. El conteo solo tampoco explica el conjunto observado: dt15,n83,H/Liguales da C67 en START19:03:00–END19:23:30 yC88 en START19:03:15–END19:23:45. Ese par cambia otras características; únicamente refuta una función de(dt,n,H,L) sin otras entradas.

## Verificación

Preregistro: `C_recorte1903_predicciones.json` y `predecir_C_recorte1903.py`. Auditoría: `analizar_C_recorte1903.py` y `C_recorte1903_resultados.json`. OHLC seleccionados idénticos al preregistro; seis C de Lite coinciden dentro de1e-7, residuos de recurrencia<1e-8; Character admite los mismosC en sus intervalos redondeados. Tres parejasc/d estables,381328celdas de16curvas repetidas; sin fallos.

Las curvas de START:30 y:45 son idénticas en127104celdas comunes. Las de START:30 y el control previo START19:04 también son idénticas en125680celdas. C61 es una misma familia publicada en esos tres controles, no una lectura aislada de una etiqueta.

AnclasSTARTsubminuto yEND:45 verificadas en etiquetas del eje para ambos indicadores, guardadas en `manual/C_recorte1903_*_anchor.png`. No se reaplicó el diálogo sobre los segundos exactos. No se actualizaron indicadores ni se usó la validación reservada. Sigue siendo investigación del mismo episodio.

## Próximo contraste específico

Cruzar esos START con END19:23:30, justo antes de la confirmación terminal conocida. Medir START19:03:15/END19:23:30 y START19:03:30/END19:23:30. Completa una comparación entre incluir/excluir el mínimo inicial y añadir/no añadir la última vela. Antes de medir se deben fijar predicciones de un modelo local explícito; no basta clasificar después los resultados como pivotes.

Se restauró y guardó gráfico/sourceLite1m, CharacterChart/Manual/B, anclas12oct18:55–19:20UTC y los dos precios auxiliares originales (arrastrar START había cambiadoPoint1). Captura `manual/C_recorte1903_restaurado.png`.
