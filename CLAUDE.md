# Protocolo para agentes (Claude, Luna/Codex u otros)

Proyecto: ingeniería inversa del parámetro **C** («Character») del indicador PoiSzn EMA Origin Lite v1.3 (TradingView, código cerrado). Idioma de trabajo y de documentos: **español**.

## Antes de nada

1. Trabaja **solo** en la rama `claude/exciting-cerf-zufni8`. No subas nada a `main`. Empieza con `git pull origin claude/exciting-cerf-zufni8`.
2. Lee `docs/RESEARCH_STATUS.md` (resultados sólidos R1–R8 y afirmaciones retiradas) y `experimentos/EXP-20261016-dependencias/README.md` (experimentos M1–M10, con resultados y lo pendiente).
3. Nunca presentes una hipótesis como resultado. Distingue **medido**, **predicho antes de medir**, **ajustado** e **hipótesis**. No codifiques casos por fecha u hora en una regla.

## Hechos establecidos (no volver a probarlos)

- Con C fijado, las 6 curvas son EMA con $\alpha = 2/(b_0 C/\Delta t + 1)$, $b_0 \in \{24, 89/3, 8, 89/9, 8/3, 89/27\}$; la semilla es el extremo de la vela END.
- Régimen corto ($n < 21$ velas inclusivas de la fuente): $C = \max(\Delta t, n\,\Delta t\cdot 10/183)$, exacto.
- Régimen largo ($n \ge 21$): C es un entero, **sin regla conocida**. C depende solo de las velas de START a END (RTH = ETH), de la resolución de la fuente y de nada más (el Lite no tiene otras entradas).
- Familias ya refutadas: ver `reports/MODELOS_REFUTADOS_PARA_GEMINI.md` y las filas «refutada» de los dos documentos anteriores.

## Herramientas

| Tarea | Comando |
|---|---|
| C exacto de un CSV del Lite (fuente = gráfico) | `python tools/invertir_C_csv.py manual/ARCHIVO.csv [--dt 60]` |
| C exacto con fuente más fina que el gráfico | `python tools/invertir_C_subfuente.py CSV VELAS_FUENTE.json --end AAAA-MM-DDTHH:MM --dt 15` |
| Marcador de reglas (maestro, 2 m, nuevos) | `python tools/evaluador_C.py evaluar` |
| Verificar M9 | `python experimentos/EXP-20261016-dependencias/verificar_M9.py` |
| Regenerar catálogo (antes de cada commit) | `python tools/build_file_catalog.py` |
| Abrir Brave con CDP (puerto 9222, perfil propio) | `tools\abrir_brave_cdp.bat` |
| Ejecutar un .js en la pestaña de TradingView | `python tools/cdp_ejecutar.py ARCHIVO.js -o SALIDA.json` (`--listar` comprueba la conexión) |

Entorno local (Windows): carpeta del proyecto `G:\trading\Indicators\` con `repo/` (este clon), `.venv/` (dependencias de `requirements.txt`) y `brave_cdp/` (perfil de Brave para CDP, fuera de git). Usa `G:\trading\Indicators\.venv\Scripts\python.exe` para todos los comandos.

Las velas de la fuente se descargan con el conector de TradingView (`get_ohlcv`, formato columnas) y se guardan en la carpeta del experimento.

## Convenciones

- Exportaciones de TradingView: en `manual/`, con nombre descriptivo (p. ej. `M9_1012_0035_0105.csv`). No se renombran ni se editan después.
- Cada experimento nuevo: hipótesis y predicciones escritas y **commiteadas antes de medir**.
- Commits en español, con resultados verificados por el propio agente (no copiar cifras ajenas sin recalcularlas).
- No descifrar ni tocar el ILScript ni el código protegido del autor. Solo metadatos, plots y exportaciones que TradingView ya muestra al usuario.
- Archivos grandes (audio, vídeo): no añadir más a git.

## Reparto de trabajo

- **Usuario / Luna (equipo local con navegador):** mediciones en TradingView, exportaciones CSV y DevTools.
- **Sesión de mantenimiento (Haiku):** verificar exportaciones subidas, recuperar C, añadir casos al evaluador, actualizar la documentación y hacer commits. No diseña hipótesis nuevas.
- **Sesión de análisis (Opus):** diseño de experimentos, hipótesis y búsquedas. Se abre cuando hay datos nuevos que interpretar.
