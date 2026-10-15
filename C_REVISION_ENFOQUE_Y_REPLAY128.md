# Revisión del enfoque: selectores iniciales y control de ejecución

13 de octubre de2026. Dos pruebas nuevas: auditoría local de selectores iniciales y control de replay en TradingView. Generador general de C pendiente.

## Evaluación del enfoque

La metodología de caja negra ha producido resultados verificables: familia de EMA, semillas/publicación con C suministrado y relación corta que predice19/20 velas en fuentes15/60/120s y fechas12/13 de octubre. Eso no implica proximidad demostrada al generador general.

La debilidad ha sido dedicar muchas tandas a familias propuestas sin evidencia positiva del criterio interno del autor. Descartar familias estrechas no mide cuánto falta. Los casos nuevos refutaron supuestos de C siempre entero y C>=fuente; por eso conviene priorizar validación de entradas, observabilidad y predicciones registradas antes de nuevas mediciones.

## Selectores iniciales

Se extendió probar_C_selectores_pivotes.py con argumento `first`, conservando el comportamiento anterior `last`. Se probaron primer máximo/mínimo, primer par opuesto y primer pivote, sobre mechas/cierre y radios1/2. Se conservan los tres alcances: estructura, todos los OHLC hasta END y ese tramo más extremos globales. Solo velas del rango confirman los pivotes.

En23 ventanas de al menos21 velas, las36 definiciones presentan entradas seleccionadas idénticas con C distintos. También se contradice C=n×F(entrada) usando una tolerancia conservadora±1 segundo para permitir redondeos. No se impone mínimo global de fuente.

Ejemplo:19:01–19:22,C77 frente a19:02–19:22,C50. El primer par opuesto de mechas radio1 es el mismo mínimo19:03 (30852.75) y máximo19:05 (30864.50). Todos los OHLC desde19:03 hasta19:22 y los extremos globales son idénticos. El prefijo omitido y conteo total cambian; siguen siendo posibles entradas. No se descarta toda función conjunta no lineal ni otro selector.

Datos: C_selectores_iniciales.json, que conserva los testigos completos. No se sobrescribió C_selectores_pivotes.json, correspondiente a últimos pivotes.

## Replay directo frente a avance secuencial

NQ1!, ETH, UTC, BADJ apagado;12 de octubre START19:04 END19:28. Fuente/gráfico60s, Lite1m explícito; Character v6.5.36 perfilB Manual fuenteChart. Histórico de referencia Lite_1904_192800_1m_b.csv, C128.

1. Arranque directo de replay en corte19:32. Última apertura exportada19:31. Excluyéndola por el desfase conocido, se comparan muestras cerradas hasta19:30.
2. Arranque independiente en corte19:28, antes de disponer de la vela END. Última apertura19:27; no hay curvas utilizables y no se asigna C=0.
3. Cuatro pasos Forward de una vela llevan al mismo timestamp final19:31. Se repiten las exportaciones y se compara con el arranque directo y el histórico.

| Estado | Última fila incluida | Pares consecutivos por curva Lite | C observable | Valores no vacíos de16 curvas idénticos al histórico |
|---|---|---:|---:|---:|
| Antes de END | 19:26 | 0 | No observable | 0 |
| Directo | 19:30 | 1 | 128 | 32 |
| Secuencial | 19:30 | 1 | 128 | 32 |

Ambas parejas repetidas son idénticas en sus curvas cerradas comunes. Los OHLC incluidos también coinciden con el histórico. Las seis estimaciones de C van aproximadamente de127.9999999985 a128.0000000006 en ambos modos. Con un solo par por curva el residuo no valida una recurrencia por sí mismo; el acuerdo de las seis estimaciones, niveles históricos y repetición aporta corroboración.

No hay ninguna diferencia entre curvas cerradas de arranque directo y secuencial. En este caso el camino de ejecución no explica C128. No se afirma invariancia universal de replay ni ausencia de series internas futuras. La primera publicación se produce19:29; sigue abierta dependencia del período END→ruptura. Este experimento no hace C observable al cierre de END.

Script analizar_C_replay128.py; datos C_replay128.json. CSV manual/C_replay128_directo/antes_END/secuencial_[a/b].csv y pendientes. Capturas C_replay128_directo.jpg y C_replay128_secuencial.jpg. Replay finalizado y referencia12 octubre18:55–19:20 fuente/gráfico1m restaurada y guardada.

## Prioridad siguiente

Mantener la caja negra y cambiar la selección de experimentos: confirmar qué entradas recibe el cálculo general y exigir predicciones numéricas antes de medir. Los selectores simples primero/último swing no bastan; no conviene encadenar otro selector solo porque el anterior falló. Una ventana completa procesada desde START o una selección que conserve estado son posibilidades, no mecanismos identificados.

Para acotar dependencias de contexto, comprobar la misma fuente explícita y anclas bajo otro intervalo de gráfico compatible y repetir un episodio bajista en replay. Si no se observa C antes de ruptura, registrar la limitación de identifiabilidad y evitar presentar una fórmula de OHLC del rango como universo ya demostrado.
