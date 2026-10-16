# C: conteo23 fijo y cruce de límites

13 octubre2026. Seis selecciones nuevas y una base reutilizada de NQ1!,12oct, ETH, UTC, BADJ apagado y Replay apagado. Fuente/gráfico1m, Lite v1.2 fuente1m y Character Tree v6.5.36 perfilB Manual fuenteChart. No se cambió precio ni código protegido.

## Desplazamientos de23velas

La hipótesis local predeclarada de que23velas produce81 en las ventanas vecinas falla en las cuatro mediciones nuevas. No era una fórmula general propuesta, sino un contraste para separar conteo de selección.

| START–END UTC | Velas | C | High global | Low global |
|---|---:|---:|---:|---:|
|15:26–15:48|23|82|30964.00|30877.75|
|15:27–15:49|23|82|30964.00|30877.75|
|15:28–15:50,base repetida anterior|23|81|30965.50|30877.75|
|15:29–15:51|23|75|30965.50|30877.75|
|15:30–15:52|23|68|30965.50|30877.75|

Cada ventana vecina comparte exactamente22OHLC con la anterior. Los tres últimos casos tienen el mismo conteo y ambos extremos globales, pero C81/75/68. Esto refuta una función que use únicamente conteo, fuente y amplitud/extremos globales en estos controles. No separa por sí solo START de END porque al deslizar cambian ambos.

## Cruces dirigidos

Se añadieron dos mediciones diagnósticas:15:30–15:51 y15:29–15:52. No se predijo su C por una fórmula desconocida. Con selecciones anteriores de END15:50 se completa esta matriz:

| START | END15:50 | END15:51 | END15:52 |
|---|---:|---:|---:|
|15:29|69 (22velas)|75 (23velas)|75 (24velas)|
|15:30|69 (21velas)|68 (22velas)|68 (23velas)|

Los seis rangos comparten high30965.50 ylow30877.75. La vela añadida15:51 es idéntica en ambas filas: O30955.75,H30957.00,L30946.25,C30950.00. Sin embargo, añadirla produce cambios distintos, +6 y−1 en C. El contraste no modifica velas: cambia qué rango se selecciona, incluyendo su conteo total.

La vela15:50 tiene H30965.50,C30955.50;15:51 retrocede sin nuevo extremo global.15:52 (O30950.25,H30957.50,L30948.50,C30952.75) revierte parcialmente el cierre y tampoco crea un extremo global; añadirla conserva C75/68. Esto es compatible con un evento interno o selección de segmento, pero no prueba un pivote particular ni su fórmula.

En esta matriz tampoco puede describirse C como contribuciones independientes aditivas de los límites, C=f(START)+g(END): la misma modificación de END debería sumar lo mismo en ambas filas. Una separación multiplicativa C=f(START)*g(END) tampoco explica ambas filas: en END15:50 su razón es1 y en END15:51 es75/68. Son exclusiones algebraicas específicas; no descartan funciones conjuntas no lineales, de duración, OHLC interno o estado.

## Verificación

Las seis parejas nuevas repiten exactamente240,224celdas de16curvas cerradas. Todos los rangos tienen coberturaOHLC completa, seis C Lite concordantes, EMA de cierre con residuo menor1e-8 y C Lite dentro del intervalo de las diez curvas Character. Última fila de CSV excluida. C81 usa la base e/f verificada anteriormente; no se cuenta como medición nueva. Sin fallas pendientes.

Script `analizar_C_23_desplazamientos.py`; salida `C_23_desplazamientos.json`, con OHLC, altas/bajas entre selecciones, intervalos, parejas y conteos. CSV/capturas en `manual/C_23_shift_1526/1527/1529/1530_*`, `manual/C_23_cross_1530_1551_*` y `manual/C_23_cross_1529_1552_*`. Los pending se conservan. Las celdas anteriores de END15:50 están en `C_START_regimenes.json` y `C_21_regimenes.json`.

Layout restaurado y guardado en12oct18:55–19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado. Captura `manual/C_23_desplazamientos_restaurado.png`.

## Siguiente contraste

Fijar END15:51 y barrer START hacia atrás alrededor de15:28–15:30, para ver si C cambia al incluir un segmento concreto sin modificar la vela final. Para un algoritmo candidato se requiere definir qué segmento conserva y una operación numérica que explique75/68, no solo identificar un máximo o retroceso. Reservar otra ventana para su predicción. No se recuperó aún el generador de C.
