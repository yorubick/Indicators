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
| `tools/` | Herramientas de mantenimiento (catálogo, auditoría Seven Cloud, reorganización), el [evaluador de reglas de C](EVALUADOR_C.md) y scripts de análisis añadidos desde el 15-oct | Se ejecutan desde la raíz del repositorio: `python tools/<script>.py`. |
| `reports/` | Los 97 informes Markdown históricos que estaban en la raíz | Registro de la investigación. Las conclusiones vigentes están en `docs/RESEARCH_STATUS.md`; si un informe y ese documento no coinciden, manda `RESEARCH_STATUS`. |
| `pine/` | Clones Pine de código abierto (`PoiSzn_*`) y versiones recibidas de Gemini (`Gemini_*_recibido.pine`) | Las versiones recibidas son instantáneas con SHA-256 registrado: no editarlas. |
| `media/` | Capturas JPG/PNG y gráficos SVG generados | `media/audio/` guarda los audios de las guías y sus transcripciones automáticas. |
| raíz | Scripts `.py` históricos y sus datos `.json`/`.csv` | Siguen en la raíz a propósito; ver [Reorganización del 16-oct-2026](#reorganización-del-16-oct-2026). |

## Reorganización del 16-oct-2026

[`tools/reorganizar_raiz_2026-10-16.py`](../tools/reorganizar_raiz_2026-10-16.py) movió con `git mv` los informes, los Pine y los medios, y reescribió las referencias en enlaces Markdown y en literales de los scripts. La correspondencia completa está en [`REORGANIZACION_2026-10-16.csv`](REORGANIZACION_2026-10-16.csv). No se modificó el contenido de `imports/`, `manual/` ni de los archivos `*recibido*`.

Los scripts y datos de la raíz **no se movieron**. Más de 100 scripts definen `ROOT = Path(__file__).parent`, varios se importan entre sí (`from obtener_C import recover`) y otros construyen los nombres de datos en tiempo de ejecución (`ROOT/f'C_barrido_15s_start{s}_estabilizado.csv'`). Separarlos rompería scripts sin que fuera fácil detectarlo. El trabajo nuevo debe ir en `experimentos/<id>/` o en `tools/`, con rutas relativas a la raíz del repositorio y nunca rutas absolutas `G:\…`.

En una copia local antigua basta con `git pull`: git mueve los archivos. Las rutas absolutas `G:\trading\guias\analisis\<archivo>` que algún script tenga a un archivo movido se actualizaron a la nueva subcarpeta.

La prueba de paridad histórica de Seven Cloud del 16-oct-2026 está documentada en [`docs/SEVEN_CLOUD_AUDIT_2026-10-16.md`](SEVEN_CLOUD_AUDIT_2026-10-16.md), con sus nueve CSV originales en la raíz y el comparador reproducible `tools/audit_seven_cloud_exports.py`.

## Archivos clave en la raíz

- `master_all_C_cases.json`: conjunto maestro consolidado.
- `reports/GEMINI_V4_REVISION.md`: auditoría de v4 y sus controles.
- `reports/PAQUETE_PARA_GEMINI.md`: síntesis y archivos vinculados al traspaso a Gemini.
- `reports/MODELOS_REFUTADOS_PARA_GEMINI.md`: familias de modelos ya evaluadas y límites de sus refutaciones.
- `reports/C_DATASET_Y_FORMULAS.md`: descripción del dataset y ecuaciones de curvas.
- `reports/INFORME_MODELO_C_INDEPENDIENTE.md`: análisis de modelos alternativos.
- `reports/C_PRUEBAS_15_SEGUNDOS.md`: investigación de controles en 15 s.
- `reports/COMO_CONTINUAR_MANUALMENTE.md`: pasos operativos de continuación.
- Archivos `*.py`, `*.pine`, `*.json`, `*.csv` y documentos Markdown históricos: permanecen en sus ubicaciones originales para conservar sus rutas relativas.

## Regla para elegir fuente

Para una medición concreta, preferir el CSV original de `manual/` y documentar la revisión del indicador oficial, símbolo, timeframe, zona horaria, anclas y vela de lectura. Las tablas o cifras de conversaciones son contexto secundario hasta enlazarlas con la exportación que las respalda. El nombre “maestro” describe la consolidación actual; no elimina la necesidad de revisar cobertura y procedencia de cada caso.
