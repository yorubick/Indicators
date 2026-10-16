# EMA inicializada con una media de varias velas

13 octubre 2026. Análisis local de CSV existentes, sin nuevas mediciones de TradingView.

## Hipótesis nueva frente a pruebas anteriores

La búsqueda anterior de una EMA ajustada al precio final probó semillas de precios puntuales y extremos del rango. Esta tanda amplía la inicialización: **media simple de las primeras k velas**, seguida de actualizaciones EMA únicamente con las velas restantes. Se busca un período N que haga coincidir el valor final de la EMA con un precio de END; la hipótesis requiere una escala común N = K × C / resolución.

Se fijaron k = 2, 3, 5, 8, 13, 21; siete fuentes (open, high, low, close, hl2, hlc3, ohlc4) y los mismos siete precios objetivo de END. Son 294 combinaciones de fuente/semilla/objetivo, con ramas de menor y mayor raíz especificadas. No se escogió por rango la raíz más cercana al C observado.

## Datos y resultado

Se reutilizaron 30 casos anteriores cuyo C excede la resolución fuente. Los casos del piso empírico se excluyen de este contraste, para no confundir saturación con ausencia de solución. También se calcularon las raíces de las cinco ventanas recientes del barrido END. Son ventanas superpuestas de una jornada, no datos independientes entre mercados.

**Ninguna combinación tiene una raíz detectada en todos los 30 casos anteriores.** Por ello ninguna llega a la etapa de estimar K común y contrastarlo con el barrido reciente. En las cinco ventanas recientes, 78 combinaciones sí tienen raíces en todas: eso muestra que ajustar solo ese pequeño barrido podría dar una falsa impresión de éxito. Tener raíz no demuestra compatibilidad con C ni con una escala común.

La búsqueda numérica usa 3,000 longitudes logarítmicas entre 1.00001 y 10,000 y detecta cambios de signo del residual. Una raíz tangente, un período fuera de ese intervalo, una inicialización distinta o un procesamiento inverso no se excluyen mediante esta búsqueda.

## Contraejemplos matemáticos

Para **278 de las 294 combinaciones** hay al menos un caso donde el objetivo no pertenece al interior del intervalo convexo de la semilla y los precios procesados. Con N > 1 finito, alpha = 2/(N+1) está entre cero y uno: cada actualización es una combinación de pesos positivos. La EMA final no puede alcanzar un valor exterior, ni un extremo del intervalo si hay valores distintos con peso positivo. Este argumento no depende de la malla numérica.

Ejemplo: fuente open, semilla = media de las primeras dos aperturas, objetivo = low de END. En el rango 04:45–05:05, fuente 1m y C compatible 75, el objetivo es **31235.25**. La semilla y aperturas restantes están entre **31238.50 y 31258.50**. Ningún período N > 1 produce el objetivo. El script conserva estos testigos por combinación.

Una ventana demasiado corta para procesar después de la semilla se marca sin raíz; no se inventan velas. Esto es una incompatibilidad con esa regla fija, pero no descarta una regla adaptativa que reduzca k según el tamaño del rango.

## Estado y dirección siguiente

Este resultado descarta otra familia concreta de ajuste al precio final; todavía no identifica C. Conviene dirigir el próximo control hacia reglas que seleccionen ventanas o puntos internos antes de ajustar, en vez de seguir ampliando indiscriminadamente semillas y coeficientes. El nuevo barrido muestra que ni los extremos globales ni el recorrido acumulado de cierres fijan C por sí solos.

Script: `probar_C_semilla_SMA.py`. Datos, cobertura, casos faltantes y testigos convexos: `C_semilla_SMA.json`.
