# Barrido empírico de C con exportaciones oficiales

Este procedimiento mide la salida del indicador desde los plots que TradingView muestra y exporta. No consulta objetos privados del navegador, código protegido ni WebSocket.

## Configuración de referencia

- Símbolo: **CME_MINI:NQ1!** (equivalente al futuro continuo NQ1! en el layout).
- Fecha y zona: **2026-10-12, UTC**.
- Sesión: ETH.
- Gráfico: 15 segundos.
- Source data resolution: 15 segundos.
- END: 19:33:00 UTC.
- START: 19:00:00 a 19:14:00 UTC, un punto por minuto (15 mediciones).

La resolución del gráfico se mantiene igual a la fuente para que la inversión EMA no confunda una actualización nativa de 15 s con una barra agregada de 1 minuto.

## 1. Crear el manifiesto de 15 casos

Desde la raíz del repositorio:

    python tools\barrido_start_1933.py --init

Esto crea data\barrido_start_1933.json y asigna a cada fila un nombre de CSV esperado dentro de data\exports\.

## 2. Exportar cada caso desde TradingView

1. Abre los ajustes del **PoiSzn EMA Origin Lite v1.3 oficial** desde el árbol de objetos.
2. Conserva la fecha 2026-10-12, END 19:33, Source data resolution 15 seconds; cambia solo 1. START.
3. Pulsa **Ok**. Verifica en la leyenda/árbol que el estudio oficial visible es PS EMA LITE / PoiSzn EMA Origin Lite, y mantén UTC y ETH.
4. Abre **Manage layouts > Download chart data**.
5. Verifica que el diálogo indique CME_MINI:NQ1!, 15S y Time format (UTC) UNIX timestamp; pulsa **Download**.
6. Guarda o mueve el CSV resultante al nombre correspondiente en data\exports\. Los nombres exactos están en el manifiesto. No combines datos de las copias locales ni del Panel Lab.

### Evitar mezclar indicadores

Antes de exportar, confirma en el árbol de objetos que **PS EMA LITE (15S, Dark)** es la fuente oficial seleccionada. Si otros estudios activos también publican plots con nombres `Lane 3 A/B`, `Lane 2 A/B` o `Lane 1 A/B`, ocúltalos temporalmente para la exportación. El analizador rechaza encabezados de Lane duplicados: no elige silenciosamente una serie cuando no puede identificar su procedencia. Conserva el original sin renombrar columnas.

Repite para START 19:14, 19:13, ..., 19:00. El CSV debe incluir time, close y las seis columnas Lane 3 A/B, Lane 2 A/B, Lane 1 A/B. Los valores de plot en la exportación oficial son la evidencia; no rellenes faltantes con la predicción.

## 3. Resolver C y los períodos

Después de copiar los CSV:

    python tools\barrido_start_1933.py --analyze

Para cada barra con plots consecutivos, el programa calcula:

    u = ((Lane 2 A[k-1] + Lane 2 A[k]) - (Lane 3 A[k-1] + Lane 3 A[k]))
        / (24 * ΔLane 3 A - 8 * ΔLane 2 A)
    C = u * Δt_chart
    N_3A = 24 * C / Δt_source
    N_2A = 8 * C / Δt_source

C_resuelto es la mediana de las estimaciones O(1) estables. measurement conserva la dispersión entre pares, el ajuste independiente de las seis lanes, el paso inferido del CSV y SHA-256 del archivo. Si faltan plots o no coincide la resolución de fuente y gráfico, el caso queda pendiente o falla explícitamente; no se inventa una medición.

## 4. Resumir cambios y comparar hipótesis

    python tools\solve_start_sweep_1933.py

El reporte lista saltos de C y compara fórmulas sencillas ya predefinidas. No ajusta una ecuación para forzar residuo cero. Este barrido usa un único END y una fecha; sirve para describir sensibilidad a START, no como validación independiente de una ley universal.

## Integridad de los datos

- Conserva un CSV original por ancla y no lo edites.
- No cambies la fuente ni la resolución a mitad del barrido.
- No mezcles CSVs de distintas copias del indicador.
- Si el exportador entrega nombres de columnas distintos, detén el análisis y registra el encabezado; no cambies alias a ciegas.

## Resultados del barrido oficial (2026-10-15)

Se completaron las 15 anclas con el estudio oficial **PS EMA LITE (15S, Dark)** visible, NQ1!, ETH, zona UTC, gráfico 15 s y resolución fuente 15 s. Cada CSV se descargó con **Manage layouts > Download chart data**; el diálogo confirmó CME_MINI:NQ1!, 15S y timestamp UNIX UTC. Los CSV tienen una sola serie de las seis Lane del oficial y OHLCV. Se conservaron sin editar en data/exports/.

C_resuelto se invirtió de pares consecutivos Lane 3 A / Lane 2 A en cada exportación. Los seis ajustes independientes de Lane coinciden con la inversión: la diferencia máxima entre C resuelto por pares y la mediana de los seis ajustes fue 0.0031 s. Cada caso aportó al menos 16,629 pares; la dispersión máxima entre estimaciones por pares fue 0.000209 s.

| START UTC | T transcurrido (s) | C resuelto (s) | N_3A = 24C/15 | N_2A = 8C/15 |
|---|---:|---:|---:|---:|
| 19:00 | 1980 | 87 | 139.2 | 46.400 |
| 19:01 | 1920 | 119 | 190.4 | 63.467 |
| 19:02 | 1860 | 88 | 140.8 | 46.933 |
| 19:03 | 1800 | 72 | 115.2 | 38.400 |
| 19:04 | 1740 | 106 | 169.6 | 56.533 |
| 19:05 | 1680 | 106 | 169.6 | 56.533 |
| 19:06 | 1620 | 87 | 139.2 | 46.400 |
| 19:07 | 1560 | 73 | 116.8 | 38.933 |
| 19:08 | 1500 | 70 | 112.0 | 37.333 |
| 19:09 | 1440 | 66 | 105.6 | 35.200 |
| 19:10 | 1380 | 66 | 105.6 | 35.200 |
| 19:11 | 1320 | 66 | 105.6 | 35.200 |
| 19:12 | 1260 | 69 | 110.4 | 36.800 |
| 19:13 | 1200 | 66 | 105.6 | 35.200 |
| 19:14 | 1140 | 78 | 124.8 | 41.600 |

C quedó entre 66 y 119 s (mediana 73 s). Con END fijo, los saltos al mover START incluyen +32, −31, −16, +34, 0, −19, −14, −3, −4, 0, 0, +3, −3 y +12 s. Esta secuencia no sigue un paso uniforme de 9 s.

Para los 15 casos, T/18.3 tuvo MAE 11.376 s y error máximo 26.361 s; round(T/18.3) tuvo MAE 11.333 s y solo 2/15 coincidencias exactas. La duración por sí sola no predice este barrido.

La misma ancla START 19:14 / END 19:33 dio C=78 en el gráfico 15 s con fuente 15 s. La verificación visual anterior en gráfico 1 min con fuente 15 s había coincidido con C manual=66. No se deben mezclar esas lecturas: la resolución del gráfico también altera el resultado observado.

Los nueve valores de un manifiesto previo procedían de telemetría de DevTools, no de estos CSV. Se conservaron aparte como data/barrido_start_1933_telemetria_legacy_no_csv.json y se excluyeron del manifiesto oficial.