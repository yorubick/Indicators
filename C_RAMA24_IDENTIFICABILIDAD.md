# Auditoría de la posible rama duración/24

13 octubre 2026. Cálculo local reproducible con `auditar_C_rama24.py`; resultados completos en `C_rama24_auditoria.json`. No se modificó TradingView ni se midieron nuevos C. No se consultaron los 27 controles largos reservados para validación.

## Resultado

Sobre los 32 controles largos de entrenamiento, `floor((n-1)*dt/24)` coincide con 7 y falla en 25. Los siete aciertos están en el episodio del 12 de octubre alrededor de 19:00–19:24 UTC y sus ventanas se solapan. Constituyen una regularidad local, no siete réplicas independientes.

Se revisaron nueve descriptores causales, sin optimizar umbrales: nuevo máximo/mínimo global, confirmación de pivote alto/bajo radio1 al END, orden de extremos globales, signo del recorrido neto, signo de cuerpo START/END y cuerpo END contra el recorrido neto.

Solo tres condiciones son comunes a los siete aciertos: no hay nuevo mínimo en END, el máximo global aparece después del mínimo y el recorrido neto es alcista. La conjunción también selecciona 19 controles donde la fórmula falla. No permite decidir cuándo utilizarla. Los otros seis descriptores no tienen un único valor común a todos los aciertos; eso no descarta combinaciones más complejas ni otras entradas.

## El divisor no está identificado exactamente

Para cada acierto con tiempo transcurrido T y C entero positivo, `floor(T/d)=C` permite el intervalo `T/(C+1) < d <= T/C`. La intersección de los siete intervalos es:

`23.77358490566038 < d <= 24 segundos`.

Por ejemplo, tanto 23.9 como 24 reproducen los siete valores. El número 24 es una hipótesis sencilla compatible con ellos, pero los datos aún no demuestran que sea la constante original. Este argumento solo aplica a esta familia de fórmulas; no afirma que el indicador divida tiempo por una constante.

## Consecuencia para las próximas mediciones

La prioridad es encontrar una segunda aparición fuera de ese episodio antes de ajustar una máquina de estados o dar por identificada una rama. La selección debe hacerse con OHLC y una definición explícita de semejanza, sin mirar C de la nueva ventana; una semejanza seleccionada no garantiza C=50.

Si aparece otro tramo de 21 velas de 1m con C=50, extender a 22/23/24 velas y registrar antes las predicciones 52/55/57. C=57 en 24 velas estrecharía el intervalo del divisor a `(23.79310344827586,24]`, todavía sin identificarlo exactamente. Si la rama cambia, esa extensión no aporta una restricción válida sobre el divisor.

Si no encontramos una réplica independiente, conservar duración/24 como observación local y evitar construir un selector para explicar retrospectivamente estas siete ventanas. No se descartan datos de otra resolución, anteriores a START o posteriores a END antes de la primera publicación observable de curvas.
