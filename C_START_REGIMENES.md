# C con END fijo: barrido de START en alcista y lateral

13 octubre2026. Doce selecciones nuevas de NQ1!,12oct, ETH, UTC, BADJ apagado y Replay apagado. Fuente y gráfico1m, Lite v1.2 fuente1m, Character Tree v6.5.36 perfilB Manual fuenteChart. Se usan dos bases21velas previamente medidas:15:30–15:50 C69 y07:00–07:20 C75.

## Predicciones y mediciones

Antes de medir se registraron dos hipótesis en `C_DECIMALES_PREDICCIONES.md`: ventanas18/19/20 siguen regla corta; si las últimas21velas fueran la única entrada del generador, ampliar START hacia atrás conservaría C69 o75.

| Velas inclusivas | START con END15:50 | C alcista | START con END07:20 | C lateral |
|---|---|---:|---|---:|
|18|15:33|60|07:03|60|
|19|15:32|62.29508197|07:02|62.29508197|
|20|15:31|65.57377049|07:01|65.57377049|
|21, base anterior|15:30|69|07:00|75|
|22|15:29|69|06:59|78|
|23|15:28|81|06:58|78|
|24|15:27|69|06:57|87|

Las seis predicciones cortas pasan. La hipótesis exclusiva de últimas21velas falla en el alcista23velas y en todas las extensiones laterales. Las últimas21OHLC y END son idénticos a la base en cada extensión22..24; se comprueba por igualdad exacta de datos, no por similitud visual.

Además, todos los rangos22..24 conservan los extremos globales de la base: alcista high30965.50/low30877.75 y lateral high31194.50/low31157.00. Por tanto, **END, últimas21velas y extremos globales no bastan para determinar C en estos controles**. Esto no descarta una fórmula que también reciba conteo total, START, prefijo, un segmento interno elegido u otra serie. Añadir prefijo cambia simultáneamente conteo y precios iniciales; la causa exacta todavía no está aislada.

El alcista muestra69→81→69 al ampliar22→23→24velas. No asumir una relación monótona entre duración yC. En lateral el valor75 de21velas pasa a78/78/87, pese a extremos constantes. Los controles cortos laterales también conservan los extremos globales; el alcista18velas cambia extremos y se documenta sin usarlo como control de extremos iguales.

## Repetición del salto81

Tras medir los rangos laterales se volvió a15:28–15:50 y se exportaron e/f. Ambos indicadores recuperan C81 y los16plots coinciden exactamente con la primera medición d en39,920celdas comunes cerradas. Esto reproduce el pico desde un estado de anclas distinto. La repetición se acepta como comprobación del dato, no como predicción nueva del generador.

## Auditoría y archivos

Las12selecciones aceptadas pasan coberturaOHLC completa, estabilidad exacta de16curvas por pareja (479,296celdas en total), seis ajustes Lite concordantes, residuos compatibles con EMA de cierre, y C Lite dentro del intervalo Character. Se excluye la última fila del CSV; tolerancia1e-8segundos para límites de intervalos y1e-7 para comparación de C. C81 usa pareja e/f; demás casos c/d. pending y la pareja inicialc/d de81 se conservan.

Script `analizar_C_START_regimenes.py`; resultados `C_START_regimenes.json`, con OHLC completo, extremos, conteo, predicción, coincidencia del sufijo y pareja aceptada. Bases tomadas de `C_21_regimenes.json`. CSV/capturas en `manual/C_START_barrido_alcista_*` y `manual/C_START_barrido_lateral_*`.

Layout restaurado y guardado: START12oct18:55, END19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado. Captura `manual/C_START_regimenes_restaurado.png`.

## Qué falta y siguiente contraste

No se recuperó la fórmula generalC. El resultado acota las entradas necesarias: una hipótesis de ventana fija final necesita explicar estos cambios por información adicional.

Siguiente contraste dirigido: conservar el conteo23 y desplazar simultáneamente ambos extremos cerca del pico81, para distinguir una dependencia genérica de23velas de una estructura concreta; después comparar esas ventanas con el lateral23C78. Una hipótesis que proponga segmento interno debe especificar cómo lo selecciona y producir valores exactos en controles reservados. No ajustar factores después de observar cada nuevo C.
