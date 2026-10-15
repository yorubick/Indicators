# Contraste del informe START y curvas atribuidas a Lite v1.3

14 octubre 2026. Auditoría local reproducible: `auditar_Gemini_START_v13.py`; salida `Gemini_START_v13_auditoria.json`. Datos originales Lite v1.2. No se midió v1.3 en esta auditoría ni se modificó TradingView.

## Qué se confirmó

Los 18 precios comunicados (seis curvas en 19:26 UTC para START19:03 y END19:23/24/25) coinciden al redondear al céntimo con los CSV históricos v1.2. Es compatible con el motor reconstruido, pero no certifica equivalencia universal entre versiones, sesiones o intravelas. C se proporciona en esa reconstrucción: no se deduce su generador.

El barrido con END19:23 también coincide con los datos históricos: START19:03 n21 C50; START19:02 n22 C52; START19:01 n23 C77, con H30870.75 y L30849. El salto 52→77 es25; 50→77 es27. Ninguno demuestra una operación con potencias de3.

## Contrastes que cambian la interpretación

| START | END | n | C |
|---|---|---:|---:|
|19:01|19:21|21|77|
|19:01|19:22|22|77|
|19:01|19:23|23|77|
|19:01|19:24|24|77|
|19:02|19:22|21|50|
|19:02|19:23|22|52|
|19:02|19:24|23|55|
|19:03|19:23|21|50|
|19:03|19:24|22|52|

C77 ya existe con21 velas; no hay una liberación universal al llegar a23. START19:02 con23 velas da55, no77. El conteo no basta.

Para END19:22, START19:01 y19:02 conservan los mismos extremos y las21 velas finales OHLCV idénticas, comprobadas registro por registro. Incluir19:01 cambia50→77. Cambian conjuntamente el prefijo, el conteo y cualquier inicialización que use START: no permite separarlos causalmente.

La vela19:01 tiene O30852.75/H30863.50/L30852/C30859.25/V700; cuerpo+6.5 puntos. La de19:02 tiene cuerpo−1.5 y la de19:03 cuerpo0. Es una pista descriptiva para orientación inicial, no una condición demostrada. Sus cierres normalizados al rango son aproximadamente0.471/0.414/0.425, respectivamente: tampoco permiten afirmar que un umbral de posición esté identificado.

## Auditoría siguiente acotada

Trabajar sobre estos controles ya medidos antes de hacer otro barrido. Si Gemini propone un estado dependiente del prefijo, debe publicar la inicialización exacta, actualización por barra y conversión numérica a C. Registrar la traza tanto al alcanzar20/21 velas desde START como en END. Alinear además las trazas por timestamp para distinguir edad del estado y posición relativa.

La prioridad es comprobar si una regla conserva información del prefijo mediante una semilla/orientación o un acumulador; no basta detectar un pivote final. Ya fueron probadas y refutadas familias concretas de reinicios que olvidan el prefijo y medias de alpha/eficiencia: consultar MODELOS_REFUTADOS_PARA_GEMINI.md antes de duplicarlas.

Exigir que la misma regla explique numéricamente77 para START19:01 n21..24 y50/52/55 para START19:02 n21..23. Si asigna el mismo estado completo a dos entradas con C distintos, descartarla. Que dos estados difieran solo evita esa refutación; no valida el mapeo a C. Una regla que pase estos controles debe congelarse y medirse en otro episodio antes de ajustar nuevos umbrales.

No se dispone de la serie interna del código protegido; las trazas candidatas son reconstrucciones propias. La disponibilidad de curvas solo después de ruptura sigue sin determinar cuándo se calcula C internamente.
