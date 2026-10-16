# PoiSzn: análisis de C y réplica de curvas

Este repositorio reúne la investigación de ingeniería inversa del indicador PoiSzn, las mediciones exportadas de TradingView, los modelos evaluados y el material procedente de Codex y Gemini.

## Empezar aquí

1. Lee [el estado de la investigación](docs/RESEARCH_STATUS.md) para separar resultados verificados, hipótesis y preguntas abiertas.
2. Consulta [el mapa del proyecto](docs/PROJECT_MAP.md) para localizar datos, scripts, informes e importaciones.
3. Antes de repetir una prueba, revisa [los modelos ya refutados](reports/MODELOS_REFUTADOS_PARA_GEMINI.md), [el informe de v4](reports/GEMINI_V4_REVISION.md) y [la guía para continuar](reports/COMO_CONTINUAR_MANUALMENTE.md).
4. Registra cada medición nueva con el protocolo de [contribución y experimentos](docs/CONTRIBUTING.md).

## Estado resumido al 16-oct-2026

- **Resuelto:** con C fijado, el motor de curvas reproduce las seis curvas Lite. En el régimen corto ($n<21$ barras inclusivas de la fuente), C sigue una fórmula exacta: $\max(\Delta t,\ n\,\Delta t\cdot 10/183)$, que acierta 35/35 casos.
- **Abierto (objetivo principal):** la regla con la que el indicador oficial elige C en el régimen largo ($n\ge21$). Allí C es siempre entero (110/110), pero ninguna regla propuesta ha acertado casos que no se usaran para construirla.
- **Retirado el 16-oct:** el «operador completo 21/21» (era una tabla de consulta), la «ley universal $T/18.3$» (3/110 aciertos exactos) y la «celosía de 9 s/27 s» (al nivel del azar). Detalle en [el estado de la investigación](docs/RESEARCH_STATUS.md#revisión-de-afirmaciones-previas).
- El dataset maestro es `master_all_C_cases.json`: 179 selecciones únicas, 145 con C Lite medido y 34 solo de Character. Ningún caso está certificado como ciego o prospectivo.
- Seven Cloud: una instancia recién añadida coincidió exactamente con el estudio oficial en 392 barras cerradas × 32 curvas. La paridad dentro de la vela en formación sigue abierta. Ver el [informe](docs/SEVEN_CLOUD_AUDIT_2026-10-16.md).
- Los valores copiados de conversaciones o reportados a mano son pistas hasta que tengan su CSV primario, el contexto del gráfico y el método de ajuste.

## Datos y procedencia

- Exportaciones y capturas manuales de TradingView: [`manual/`](manual). Se conservan sus nombres originales.
- Importaciones de Gemini y Codex: [`imports/`](imports), copiadas sin modificar. El inventario de copia y hashes SHA-256 está en [`docs/IMPORT_MANIFEST.csv`](docs/IMPORT_MANIFEST.csv).
- Inventario de todos los archivos y su SHA-256: [`docs/FILE_CATALOG.csv`](docs/FILE_CATALOG.csv). Para regenerarlo: `python tools/build_file_catalog.py`.
- Repositorio remoto: [`github.com/yorubick/Indicators`](https://github.com/yorubick/Indicators).

## Alcance

El repositorio organiza evidencia y documentación para continuar la investigación. No valida automáticamente la exactitud de los datos históricos ni convierte hipótesis discutidas en resultados confirmados. Consulta cada informe de origen para su alcance y limitaciones.
