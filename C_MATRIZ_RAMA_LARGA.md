# Matriz de START/END para la rama posterior a20 velas

13 de octubre de2026. Seis nuevas selecciones de NQ1!,12 octubre, ETH, UTC, BADJ apagado. Gráfico/fuente60s. Lite v1.2 fuente explícita1m y Character v6.5.36 perfilB Manual fuenteChart. Se verificaron OHLC completos y16 curvas cerradas repetidas por pareja. El informe integra17 selecciones actuales/anteriormente comprobadas.

## Matriz

START en filas y END en columnas. — significa que esa combinación no se midió; no hay interpolación. C coincide entre seis curvas Lite y el intervalo de Character con tolerancia numérica1e-8.

| START / END | 19:20 | 19:21 | 19:22 | 19:23 | 19:24 | 19:25 |
|---|---:|---:|---:|---:|---:|---:|
| 19:00 | 77 | 102 | 77 | 77 | 60 | — |
| 19:01 | — | 77 | 77 | 77 | 77 | — |
| 19:02 | — | 65.57377049 (20 velas) | 50 | 52 | 55 | 71 |
| 19:03 | — | — | — | 50 | 52 | — |
| 19:04 | — | — | — | — | 50 | — |

Los seis controles nuevos son19:01–19:23/24,19:02–19:23/24/25 y19:03–19:24. Las restantes celdas se tomaron de exportaciones ya verificadas; no cuentan como nuevas mediciones.

## Qué distingue

Para22 velas,19:01–19:22 da77 y19:02–19:23 da52. Comparten máximo30870.75 y mínimo30849.00; tener el mismo conteo y extremos globales no basta para obtener C. Sus END y OHLC interiores difieren, por lo que no se atribuye el cambio únicamente a START.

Con START19:01, C77 se mantiene al incorporar finales19:22,19:23 y19:24 con cierres diferentes. Con START19:02, cambia50→52→55→71. La primera vela por sí sola no determina un C que permanezca fijo hasta cualquier END.

Las ventanas19:02–19:22,19:03–19:23 y19:04–19:24 tienen21 velas, los mismos extremos y C50. Las ventanas19:02–19:23 y19:03–19:24 tienen22 velas, los mismos extremos y C52. Esa repetición motiva una prueba por conteo **local**, sin probar una regla universal.

## Dos predicciones prefijadas

Se registraron antes de medir en C_DECIMALES_PREDICCIONES.md. La secuencia50/52/55 para21/22/23 velas era compatible con floor(2.4*n); no determinaba un coeficiente único ni el algoritmo.

| Selección | n | C predicho | C medido | Resultado |
|---|---:|---:|---:|---|
| 19:03–19:24 | 22 | 52 | 52 | Acierta |
| 19:02–19:25 | 24 | 57 | 71 | Falla |

La segunda falla al añadir19:25, una vela O30869.25,H30871.25,L30867.00,C30868.75 que eleva el máximo global desde30870.75 a30871.25. El cierre no rompe ese máximo previo. Se añadieron simultáneamente una vela, nuevos OHLC y un nuevo máximo: la coincidencia no demuestra que el máximo sea la causa del salto.

No se reajusta la pendiente2.4 para recuperar71. La regla proporcional local no explica el siguiente punto y no debe incorporarse como generador general.

## Implicación

La búsqueda debe explicar tanto los tramos que repiten escalas por conteo como las transiciones a otras escalas. Una posible selección de estructura o solución sigue abierta, pero no se identificó el selector. El mínimo de fuente no se aplica universalmente; C50/52/55 siguen siendo resultados válidos en fuente60s.

Un siguiente control útil es conservar conteos22/23 y desplazar las ventanas para incluir o excluir19:25, registrando los cambios de extremos, dirección de END y C. Comparar además finales posteriores sin nuevo extremo. Eso evalúa una condición definida de máximo nuevo sin suponer retrospectivamente que todo salto debe ser un nuevo setup.

## Archivos

Script analizar_C_matriz.py; resultado C_matriz.json, con17 rangos y todos sus OHLC. El script comprueba curvas repetidas, cobertura e intervalo de C para cada celda. CSV manual/Lite_1901_192300/192400_1m_[a/b].csv; Lite_1902_192300/192400/192500_1m_[a/b].csv; Lite_1903_192400_1m_[a/b].csv. Los pendientes se conservan como diagnóstico.

Capturas C_matriz_*_anclas.jpg. Referencia18:55–19:20,12 de octubre, fuente/gráfico1m restaurada y layout guardado; C_matriz_referencia_final.jpg. No se identificó todavía el generador general de C.
