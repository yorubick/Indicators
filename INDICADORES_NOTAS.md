# Investigación inicial de los indicadores

Fecha: 2026-10-12. Objetivo: identificar el cálculo de las curvas y después investigar las reglas de señales con históricos y observación incremental.

## Accesos reportados por el usuario

- Seven Cloud EMA.
- Manual Anchor CCII V3.9.
- Character 3 V6.3 User Release.

Se verificó la sesión de TradingView del usuario y la sección Purchased → Invite-only. Los nombres exactos visibles son:

- Character Tree v6.3 - User Release, autor TCMTrader1.
- PoiSzn Seven Cloud EMA, autor TCMTrader1.
- PoiSzn · Manual Anchored CCII v3.9, autor TCMTrader1.

Al añadir Character Tree solicita seleccionar puntos sobre el gráfico antes de completar su incorporación: “Manual: click the range START candle. Auto: click the fixed box END candle.” Se canceló esa incorporación con Escape; no se eligió aún un rango de prueba. No se deben inferir fórmulas ni equivalencia exacta con Auto Zoom solo por el nombre.

## Evidencia visual de la guía Character Tree

Se extrajeron fotogramas del archivo local Character-Tree-081026.mp4. Esta revisión inicial es visual: no constituye una revisión completa del audio ni de todas las opciones.

- En 00:45 y 01:30, el panel se titula CT63PDU11. Incluye Profile (B en el ejemplo), Theme, Show delivery signals, Anchor mode (Manual), Range start / auto search begins, Range end candle (included) y Data resolution (1 second).
- También incluye Show extra EMA clouds, colores de dos nubes adicionales, Show range y Show PD arrays.
- En 07:30, Anchor mode muestra una opción cuyo texto visible comienza con Auto Bal...; el nombre completo aún no está confirmado. Se ve el abanico de curvas arrancando al terminar el rango destacado.
- La relación entre Character 3 V6.3 User Release y la guía Character Tree es muy probable por versión y aspecto, pero hay que comprobar el título y ajustes del indicador instalado.
- La configuración de resolución interna es una variable esencial: no se debe asumir que las EMA se actualizan exclusivamente con las velas de un minuto mostradas.

## Evidencia visual de Auto Zoom

Se extrajeron fotogramas de Auto-Zoom-081026.mp4. El panel se titula Auto Zoom y el gráfico muestra rangos, niveles, señales y nubes locales. No está confirmado que este producto sea equivalente a Manual Anchor CCII V3.9, ni que el usuario haya recibido acceso a Auto Zoom.

## Próximo paso

Inspeccionar por separado las tres instancias en TradingView: nombres exactos, valores por defecto, fuentes, períodos o perfiles, resolución interna y reglas de anclaje. Registrar símbolo, contrato/continuo, sesión, ajustes de precios y zona horaria. Empezar con Character 3 para comparar sus curvas con las capturas originales.

Priorizar una prueba controlada con ancla fija; después investigar el modo automático, cuándo se confirma el rango y si cambia tras avanzar o recargar. Analizar señales solo después de establecer el cálculo de curvas. No presentar coincidencias visuales como recuperación demostrada del código o fórmula exacta.
