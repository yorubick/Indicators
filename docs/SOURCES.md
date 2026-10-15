# Orígenes y copias centralizadas

## TradingView / trabajo de análisis

La carpeta del proyecto ya era `G:\trading\guias\analisis`; `manual/` contiene las exportaciones/capturas que estaban junto a scripts e informes. Los nombres se preservaron. La importación no movió ni borró las carpetas de origen.

## Gemini

- `imports/gemini/c_discovery/`: copia recursiva de `C:\Users\PC\.gemini\antigravity\scratch\c_discovery`, excluyendo `__pycache__` y archivos `.pyc`.
- `imports/gemini/brain_0d7f3bfd/`: copia recursiva del scratch asociado al Brain `0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27`, excluyendo caché Python.

Las importaciones son preservaciones del material hallado, no una declaración de que cada script sea actual o seguro de ejecutar. Comprueba dependencias y rutas antes de ejecutar.

## Codex

- `imports/codex/2026-10-14_telemetry_paste.txt`: copia del adjunto `Texto pegado.txt` proporcionado en el chat activo, conservando contenido; el nombre de destino aclara fecha y procedencia.
- `docs/CODEX_THREADS.md`: índice de hilos relacionados e IDs, no un archivo de transcripciones.

## Integridad

`docs/IMPORT_MANIFEST.csv` registra ruta fuente, ruta destino relativa, tamaño y SHA-256 de cada copia importada. `docs/FILE_CATALOG.csv` registra ruta, categoría, tamaño y SHA-256 de los archivos del proyecto, excluyendo `.git`, cachés Python y el propio catálogo.
