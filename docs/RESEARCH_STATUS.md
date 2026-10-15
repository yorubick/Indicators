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

## Control 19:36 / 19:37 — 14-oct-2026

La lectura oficial en 19:37 resultó vacía (`∅`) porque no hubo ruptura del high de END. La auditoría de E también tiene contraejemplos en 19:26 y 19:33, y la fórmula publicada con `round` no coincide con todos los C; ver [el informe detallado](../experimentos/15s_serie_1903/CONTROL_1936_EVAL_1937.md) y [la captura de TradingView](../experimentos/15s_serie_1903/evidencia/C_Lite_1936_eval_1937.png).

## Controles de Desplazamiento de START (END 19:33, Eval 19:34, Fuente 15s) — 14-oct-2026

- **START 19:08, END 19:33** (`CTRL-20261014-1908-1933-15S`): $C = 70\text{ s}$ confirmado en las 6 líneas con residuo $< 0.005$ pt. Revela un cambio de $\Delta C = -17\text{ s}$ para $\Delta T = -300\text{ s}$ respecto a START 19:03 ($C = 87\text{ s}$), con tasa $\Delta T / \Delta C \approx 17.65 \approx 18.3$. Ver [informe](../experimentos/15s_serie_1903/CONTROL_1908_1933_EVAL_1934.md).
- **START 19:13, END 19:33** (`CTRL-20261014-1913-1933-15S`): $C = 66\text{ s}$ confirmado en las 6 líneas con residuo $< 0.005$ pt. Conecta exactamente con la ley de régimen corto para $n_{\Delta} = 20$ barras: $\operatorname{round}(20 \times 60 \times 10 / 183) = \operatorname{round}(65.5738) = \mathbf{66.0\text{ s}}$. Ver [informe](../experimentos/15s_serie_1903/CONTROL_1913_1933_EVAL_1934.md).
- **START 19:18, END 19:33** (`CTRL-20261014-1918-1933-15S`): $C = 39\text{ s}$ confirmado en las 6 líneas con residuo $< 0.005$ pt. Falsifica el tope inferior $\max(60)$ en fuente de 15s y muestra un salto cuántico de exactamente $27\text{ s}$ ($3^3$) desde $66\text{ s}$ ($66 - 27 = 39$). Ver [informe](../experimentos/15s_serie_1903/CONTROL_1918_1933_EVAL_1934.md).


