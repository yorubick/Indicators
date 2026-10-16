# Registrar experimentos y mediciones

## Antes de medir

- Revisa `docs/RESEARCH_STATUS.md`, `reports/MODELOS_REFUTADOS_PARA_GEMINI.md` y los resultados existentes en `manual/`.
- Escribe la hipótesis, el resultado predicho y los controles antes de abrir la lectura oficial. Marca si la predicción es ciega o retrospectiva.
- Confirma versión/nombre del indicador oficial, símbolo/contrato, fecha, sesión, timezone, timeframe y fuente de barras.

## Ficha mínima por selección

Registrar para cada fila/caso:

1. Identificador del caso y referencia a archivo CSV/captura sin cambiar el original.
2. START y END en UTC; regla de inclusión de la barra END.
3. Timestamp y OHLCV de la barra de semilla y de cada barra de evaluación.
4. Barra de ruptura y condición usada para habilitar las curvas.
5. Valores oficiales de las seis curvas o columnas exportadas, con precisión original.
6. Método de ajuste de C, candidatos, tolerancia y residuo máximo; indicar si C se midió directamente o se infirió.
7. Predicción previa, resultado observado y estado: confirmado, refutado, ambiguo o pendiente.
8. Script/commit, versión de Python/Pine y comando reproducible.

## Reglas para evitar falsos positivos

- No mezclar timeframe del gráfico con timeframe/fuente efectiva del indicador.
- No declarar coincidencia por redondeo a centavos si el ajuste requiere precisión subyacente; reportar ambos.
- No usar los mismos casos para inventar una regla y presentarlos después como controles prospectivos.
- No extrapolar una refutación más allá de la familia y el dominio que se probaron.
- Separar claramente observación del mercado, salida del indicador oficial, simulación del emulador e interpretación causal.

## Archivos

Dejar los originales de TradingView en `manual/`. Guardar scripts nuevos con nombre descriptivo y notas de ejecución junto a ellos, o en una futura carpeta de experimento con enlace desde `docs/PROJECT_MAP.md`. No sobrescribir la evidencia anterior: crear una nueva versión y actualizar el catálogo con `python tools/build_file_catalog.py`.
