# Cruce START/END alrededor del primer pico C=2 en1s

14 octubre2026. Litev1.2 cargado, sin actualizar, NQ1!, ETH, UTC, sin ajuste de contratos. Fuente y gráfico1s. Dos mediciones nuevas, con predicciones registradas antes de medir en C_1S_CRUCE_START_PREREGISTRO.json. Misma sesión y episodio; no validación entre mercados.

## Matriz verificada

|START|END14:04:32|END14:04:33|
|---|---:|---:|
|14:04:00|2,33velas,control anterior|1,34velas,control anterior|
|14:04:01|1,32velas,nuevo|1,33velas,nuevo|

Hipótesis solo conteo: predicciones1/2 para los nuevos casos; acierta1/2. Hipótesis soloEND: predicciones2/1; acierta1/2. Ninguna explica los cuatro controles completos.

## Qué se conservó

Las cuatro selecciones tienen máximo30529.25 y mínimo30487.75. La primera ruptura posterior por cierre es la misma vela,14:05:26UTC,haciaabajo. Cada columna conserva además END,OHLCdeENDy semilla de laEMA. Las nuevas selecciones contienen exactamente el sufijo original al quitar la primera vela; OHLCVy datos de mercado posteriores coinciden.

MoverSTARTunsegundo reduceC2→1conEND32y dejaC1→1conEND33. La respuesta aSTARTdepende delEND. Un modelo aditivo C=f(START)+g(END) requeriría igual efecto en ambas columnas; la diferencia de diferencias aquí es−1segundo, incompatible con él. También falla la separabilidad multiplicativa: la filaSTART01tiene valores iguales y la filaSTART00distintos.

Comparación de igual conteo: START00/END32ySTART01/END33tienen33velas, fuente1s, mismosH/L y primera ruptura, peroC2vs1. La tupla(dt,n,H,L) tampoco basta en este caso pequeño. Esto no excluye funciones conjuntas de todo el rango ni información interna anterior/posterior.

## Verificación

Anclas exactas comprobadas en etiquetas del eje, guardadas enmanual/C_1s_start01_end32_anchor.png y C_1s_start01_end33_anchor.png. Parejasa/bcerradas repitenOHLCV y6plots. Cobertura nativa1scompleta en cada rango y600segundos posteriores. Todas las seis estimacionesCcoinciden dentro1e-6segundos;RMSEde recurrencia<1e-8.

Reconstrucción con semillaEND y cierres nativos hasta600segundos: error máximo3.28e-11puntos, sin diferencias de visibilidad. No se usóCharacter como corroboración. Se conservan exportacionespending como diagnóstico, sin usarlas para sustituir las parejas estables.

Resultados,OHLC,hashes y controles: C_1s_cruce_START_resultados.json. Script analizar_C_1s_cruce_START.py. El layout principal permanece intacto; la copia se guarda enSTART01/END33.

## Alcance de la conclusión

Tenemos una interacción START/END observada con apenas32–34velas de1s, incluida una duplicación de longitudesLite al pasarC1→2. No demuestra una arquitectura binaria interna, un selector de pivotes, armónicos, memoria recursiva ni un ancla anterior aSTART. Dos valores enteros también son compatibles con cuantización de un cálculo continuo.

El mismo patrón de interacción se había observado en los rangos15sdeC54/61/67/88. Este caso reduce el número de datos que un candidato debe procesar, pero no identifica por sí solo la fórmula. Debe incorporarse como control obligatorio a cualquier candidato explícito nuevo, en lugar de añadir excepciones para sus cuatro valores.
