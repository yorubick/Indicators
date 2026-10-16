# PoiSzn: análisis de C y réplica de curvas

Este repositorio reúne la investigación de ingeniería inversa del indicador PoiSzn, las mediciones exportadas de TradingView, los modelos evaluados y el material procedente de Codex y Gemini.

## Empezar aquí

1. Lee [el estado de la investigación](docs/RESEARCH_STATUS.md) para separar resultados verificados, hipótesis y preguntas abiertas.
2. Consulta [el mapa del proyecto](docs/PROJECT_MAP.md) para localizar datos, scripts, informes e importaciones.
3. Antes de repetir una prueba, revisa [los modelos ya refutados](MODELOS_REFUTADOS_PARA_GEMINI.md), [el informe de v4](GEMINI_V4_REVISION.md) y [la guía para continuar](COMO_CONTINUAR_MANUALMENTE.md).
4. Registra cada medición nueva con el protocolo de [contribución y experimentos](docs/CONTRIBUTING.md).

## Estado resumido al 16-oct-2026

- El dataset maestro es `master_all_C_cases.json`: 179 selecciones únicas; 145 casos con C Lite medido y 34 casos Character-only. Los 34 últimos no son mediciones Lite.
- El emulador reproduce las curvas Lite en el alcance medido cuando se fija C. Esto no demuestra que el generador automático de C esté descubierto.
- La regla general que el indicador oficial usa para elegir C sigue abierta. Hay controles externos donde la predicción de v4 no coincide; por tanto, v4 no debe describirse como una regla ciega/prospectiva ya validada.
- El repositorio preserva las rutas históricas de los archivos para no romper scripts existentes. La organización nueva está en `docs/`, `imports/` y `tools/`.
- Los valores copiados de conversaciones o reportados manualmente se consideran pistas hasta que tengan su CSV/lectura primaria, contexto de gráfico y método de ajuste anexos.
- En la prueba Seven Cloud del 16-oct, la instancia recién añadida desde el código guardado coincidió exactamente con el estudio oficial en 392 barras cerradas y 32 curvas por barra; la instancia que ya estaba cargada conservó diferencias. La lectura intrabar sigue abierta. Ver el [informe y protocolo reproducible](docs/SEVEN_CLOUD_AUDIT_2026-10-16.md).

## Datos y procedencia

- Exportaciones y capturas manuales de TradingView: [`manual/`](manual/). Se conservan sus nombres originales.
- Importaciones de Gemini y Codex: [`imports/`](imports/), copiadas sin modificar. El inventario de copia y hashes SHA-256 está en [`docs/IMPORT_MANIFEST.csv`](docs/IMPORT_MANIFEST.csv).
- Inventario de todos los archivos y su SHA-256: [`docs/FILE_CATALOG.csv`](docs/FILE_CATALOG.csv). Para regenerarlo: `python tools/build_file_catalog.py`.
- Este repositorio Git aún no tiene remoto configurado. La preparación local para publicación incluye los archivos existentes del proyecto, las nueve exportaciones recientes y el informe reproducible de Seven Cloud; falta confirmar el repositorio GitHub de destino.

## Alcance

El repositorio organiza evidencia y documentación para continuar la investigación. No valida automáticamente la exactitud de los datos históricos ni convierte hipótesis discutidas en resultados confirmados. Consulta cada informe de origen para su alcance y limitaciones.
