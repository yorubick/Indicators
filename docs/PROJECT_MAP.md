# Mapa del proyecto

## Directorios

| Ruta | Contenido | Nota de uso |
|---|---|---|
| `manual/` | CSV, capturas y notas descargados manualmente de TradingView | Evidencia primaria cuando el archivo contiene columnas y contexto necesarios. No renombrar ni sustituir originales. |
| `imports/gemini/c_discovery/` | Copia del scratch de Gemini `antigravity/scratch/c_discovery` | Fuentes y notas de esa línea de trabajo; revisar rutas configuradas antes de ejecutar scripts. |
| `imports/gemini/brain_0d7f3bfd/` | Copia del scratch asociado al Brain `0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27` | Copia de preservación, no implica que cada archivo sea vigente o canónico. |
| `imports/codex/` | Adjuntos pegados a chats de Codex | Material con procedencia conversacional; no equivale a exportación oficial por sí solo. |
| `docs/` | Índices y guía de trabajo añadidos para centralizar el proyecto | Mantener aquí el resumen durable y enlazar documentos fuente en vez de duplicarlos. |
| `experimentos/` | Carpetas estructuradas de experimentos reproducibles | Contienen README con ficha técnica, telemetría JSON y scripts de inversión/auditoría. |
| `tools/` | Herramientas de mantenimiento del catálogo | El catálogo no ejecuta el análisis del indicador. |

La prueba de paridad histórica de Seven Cloud del 16-oct-2026 está documentada en [`docs/SEVEN_CLOUD_AUDIT_2026-10-16.md`](SEVEN_CLOUD_AUDIT_2026-10-16.md), con sus nueve CSV originales en la raíz y el comparador reproducible `tools/audit_seven_cloud_exports.py`.

La prueba M5 de Character Tree Auto Balanced del 16-oct-2026 está resumida en [CT_auto_M5_resultados.md](../CT_auto_M5_resultados.md), con CSV, snapshots y capturas anotadas en la raíz; la auditoría reproducible está en [`auditar_CT_auto_M5.py`](../auditar_CT_auto_M5.py) y el estado estructurado en [`experimentos/CT_auto_balanced_M5_2026-10-16/`](../experimentos/CT_auto_balanced_M5_2026-10-16/README.md).

## Archivos clave en la raíz

- `master_all_C_cases.json`: conjunto maestro consolidado.
- `GEMINI_V4_REVISION.md`: auditoría de v4 y sus controles.
- `PAQUETE_PARA_GEMINI.md`: síntesis y archivos vinculados al traspaso a Gemini.
- `MODELOS_REFUTADOS_PARA_GEMINI.md`: familias de modelos ya evaluadas y límites de sus refutaciones.
- `C_DATASET_Y_FORMULAS.md`: descripción del dataset y ecuaciones de curvas.
- `INFORME_MODELO_C_INDEPENDIENTE.md`: análisis de modelos alternativos.
- `C_PRUEBAS_15_SEGUNDOS.md`: investigación de controles en 15 s.
- `COMO_CONTINUAR_MANUALMENTE.md`: pasos operativos de continuación.
- Archivos `*.py`, `*.pine`, `*.json`, `*.csv` y documentos Markdown históricos: permanecen en sus ubicaciones originales para conservar sus rutas relativas.

## Regla para elegir fuente

Para una medición concreta, preferir el CSV original de `manual/` y documentar la revisión del indicador oficial, símbolo, timeframe, zona horaria, anclas y vela de lectura. Las tablas o cifras de conversaciones son contexto secundario hasta enlazarlas con la exportación que las respalda. El nombre “maestro” describe la consolidación actual; no elimina la necesidad de revisar cobertura y procedencia de cada caso.
