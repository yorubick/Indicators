# Controles bajistas y nuevas mediciones de C

13 de octubre de 2026. NQ1!, ETH, B-ADJ desactivado, Character Tree v6.5.36, perfil B, Manual, fuente Chart y gráfico de un minuto. Anclas del 12 de octubre, horas UTC. Sin actualizar el indicador.

| START | END | C entero compatible | Intervalo C en segundos |
|---|---|---:|---|
| 04:45 | 05:15 | 116 | [115.972222,116.067416) |
| 04:45 | 05:25 | 113 | [112.921348,113.146067) |
| 04:45 | 05:30 | 110 | [110.000000,110.138889) |
| 04:50 | 05:25 | 113 | [112.921348,113.146067) |

Los primeros dos C reproducen mediciones antiguas cuyos archivos carecían de todo el historial inmediato de END. Los otros dos son nuevos controles. Un entero compatible único no prueba que el C interno siempre sea entero.

## Verificación

Se exporta cada selección dos veces sin cambiar inputs y después de permitir el recálculo. Se comparan las diez curvas en los timestamps comunes, excluyendo las dos últimas filas comunes: 21,000 / 21,010 / 21,010 / 21,020 valores respectivamente coinciden exactamente. Todos los archivos contienen el OHLC del rango y los primeros 90 minutos posteriores a END.

La primera ruptura en los cuatro casos es un cierre inferior al mínimo global del rango, a las 05:36 UTC. Las diez curvas comienzan en esa misma vela. En todos los rangos, los extremos globales son 31,259.75 y 31,227.25, pero los OHLC de END difieren entre las tres horas finales.

El procedimiento `FlujoManual` recibe C, inicia ambas ramas en los extremos de END y las actualiza con cada cierre posterior. Selecciona la rama iniciada en el máximo de END al romper por abajo. No ajusta esa semilla a los plots originales.

Las cuatro reconstrucciones coinciden: 700, 800, 850 y 800 valores respectivamente (3,150 en total), con error máximo `2.9104e-11` puntos. No hay valores originales antes de la publicación prevista ni valores ausentes después en la ventana comprobada.

Esto fortalece el control bajista de la regla de primera aparición/semilla. Son rangos superpuestos de una misma jornada, no cuatro episodios independientes de mercado. No valida señales, alertas, cambios de modo ni Auto Balanced y no identifica el generador de C.

## Información nueva para investigar C

- START 04:45 y 04:50 con END 05:25 conservan C113 y los extremos globales. En este par, eliminar cinco velas del principio no cambia el C compatible. No demuestra que START sea irrelevante en general.
- Con START 04:45, ampliar END de 05:15 a 05:25 y 05:30 reduce C116 → C113 → C110. Una regla universal creciente basada solo en duración queda contradicha también en este episodio bajista.
- Los cuatro archivos completos permiten comprobar hipótesis posteriores sin recurrir a un OHLC de apoyo de otra exportación. Los CSV antiguos se conservan y no se sobrescriben.

CSV: `C_bear_0445_0515_a/b.csv`, `C_bear_0445_0525_a/b.csv`, `C_bear_0445_0530_a/b.csv`, `C_bear_0450_0525_a/b.csv` (a/b indica dos archivos separados). Datos detallados: `C_bajistas.json`. Script: `analizar_C_bajistas.py`. Evidencia visual de 04:45–05:30: `C_bear_0445_0530.jpg`.

La configuración final vuelve a START 18:55, END 19:20, fuente/gráfico de un minuto, con C esperado 62.
