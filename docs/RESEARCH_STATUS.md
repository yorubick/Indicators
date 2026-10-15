# Estado de la investigación — 14-oct-2026

## Qué puede afirmarse con el material consolidado

- `master_all_C_cases.json` registra 179 selecciones únicas: 145 con C Lite medido y 34 Character-only. Los casos Character-only no deben presentarse como C Lite medidos.
- La revisión de v4 registra 96/112 casos exactos bajo la tolerancia estricta indicada en el informe; 62/78 en la rama larga y 12/13 en los controles añadidos. Lee `GEMINI_V4_REVISION.md` para definiciones, alcance y salvedades.
- La reproducción de las curvas EMA con C fijado concuerda con los casos comprobados en el alcance documentado. Esto valida la parte de curvas para esos casos, no la regla que elige C.
- Los controles externos descritos en el informe de v4 no respaldan una predicción prospectiva general; cinco controles de 15 s fallan las predicciones anotadas allí.
- Las pruebas de agregación y timeframe disponibles no aíslan por sí solas una causa temporal: pueden variar la cobertura efectiva, las barras y el cálculo de C. Véanse `PAQUETE_PARA_GEMINI.md` y los JSON de barrido asociados.
- El experimento [`experimentos/15s_serie_1903/`](../experimentos/15s_serie_1903/README.md) midió e invirtió 13 ventanas consecutivas (19:23 a 19:35 UTC) con fuente oficial 15 s en gráfico 1 m. Demostró que $C_{15\text{s}}$ es estrictamente entero ($\{88, 67, 88, 88, 79, 102, 123, 67, 87, 106, 87, 123, 87\}$) con residuo $< 0.005$ pt en las 6 curvas, confirmando que la resolución de fuente altera el valor intrínseco de $C$.

## Qué sigue abierto

1. La regla general, determinista y causal por la que el indicador oficial elige C.
2. Qué variables alimentan esa elección: anclas, barras previas, rango/volumen, estado persistente u otra condición.
3. La equivalencia completa entre Character Tree y Lite, en especial durante huecos de sesión y cambios de régimen.
4. La reproducibilidad de lecturas en vivo recientes: hacen falta exportaciones primarias, versión exacta del indicador, configuración y vela de evaluación.

## Lecturas conversacionales que no deben elevarse a “verdad de referencia”

El adjunto [`imports/codex/2026-10-14_telemetry_paste.txt`](../imports/codex/2026-10-14_telemetry_paste.txt) contiene una tabla de lecturas y razonamiento pegados desde una conversación. Úsalo como pista de búsqueda, no como sustituto de los CSV fuente. En particular, una secuencia con patrón armónico o etiquetas “pico/meseta” no demuestra por sí misma un mecanismo causal; registra primero los valores observados, y evalúa la hipótesis en casos nuevos no usados para formularla.

## Prioridad para continuar sin rehacer trabajo

1. Leer completos `GEMINI_V4_REVISION.md`, `MODELOS_REFUTADOS_PARA_GEMINI.md` y `COMO_CONTINUAR_MANUALMENTE.md`.
2. Localizar en `manual/` los CSV vinculados a cada control; confirmar que las seis curvas oficiales están exportadas y que las barras evaluadas son comparables.
3. Reproducir primero los resultados históricos con el código y parámetros anotados; guardar comandos, versiones y residuos.
4. Diseñar la siguiente hipótesis a partir de casos de entrenamiento y fijar controles nuevos antes de observar sus salidas. Separar predicción ciega de ajuste retrospectivo.

## Convenciones

- **Medido**: lectura primaria en un archivo exportado o captura verificable, con contexto suficiente.
- **Ajustado/inferido**: C estimado mediante el ajuste de las curvas; registrar método, tolerancia y residuo.
- **Predicción**: valor escrito antes de consultar el control.
- **Hipótesis**: interpretación aún no discriminada por controles independientes.
