# Prueba de C mediante transformaciones del precio

Propuesta del segundo chat, 13 octubre 2026. No contiene mediciones nuevas del indicador ni afirma identificar C. Se revisaron los informes locales y no se encontró este experimento entre las pruebas documentadas.

## Pregunta

¿Conserva C su valor cuando se presenta la misma trayectoria temporal con otro nivel o escala de precio?

Las comparaciones entre ventanas reales cambian varias entradas simultáneamente. Una transformación afín P'=aP+b permite conservar timestamps y la estructura relativa del recorrido. Debe verificarse sobre los datos exportados; no basta la semejanza visual.

TradingView permite expresiones con símbolos, números y operadores. Su documentación indica que los spreads históricos intradía se construyen desde barras de un minuto. Por ello esta prueba comienza en gráfico y fuente de 1 minuto, sobre datos históricos cerrados, y no sobre las fronteras de 15 segundos.

Fuente: https://www.tradingview.com/support/solutions/43000502298-spread-charts-explained/

## Controles congelados antes de medir

Símbolo base S=CME_MINI:NQ1!, sesión ETH, sin ajuste de contratos, UTC, modo Manual. Indicadores originales Character y Lite, versiones de la investigación. Fuente y gráfico 1m. Trabajar en una copia del layout para evitar interferencias.

1. Rango largo: 12 octubre 2026, START18:55:00 y END19:20:00 UTC. Referencia histórica C=62; repetirla primero.
2. Control corto: misma fecha, START19:00:00 y END19:19:00 UTC, 20 velas incluidas. Regla corta observada predice C=65.57377049180328. Es un control de compatibilidad, no una ley demostrada para símbolos sintéticos.

Expresiones a solicitar, en este orden:

| Expresión | a | b | Propósito |
|---|---:|---:|---|
| S | 1 | 0 | Repetir la referencia original |
| S+0 | 1 | 0 | Detectar efectos de pasar a un símbolo sintético |
| S+10000 | 1 | 10000 | Cambiar el nivel conservando diferencias en puntos |
| 2*S | 2 | 0 | Duplicar nivel y diferencias, conservando proporciones |

No medir las dos últimas como contrastes interpretables hasta aceptar S+0. Si la interfaz simplifica S+0 al símbolo original, registrar que este control no verifica la compatibilidad con un contexto sintético.

## Criterios de aceptación

- Dos exportaciones estables por configuración, con anclas exactas y suficiente historial posterior para recuperar C de las seis curvas Lite.
- Exportar también volumen. Comprobar su disponibilidad y si coincide; si cambia o desaparece, no atribuir una diferencia de C exclusivamente al precio.
- Exigir cobertura temporal idéntica desde START hasta el final del intervalo posterior analizado, incluida la primera publicación. Anotar cuánto historial previo se pudo comparar; no afirmar que se comprobó toda la prehistoria interna.
- Para a>0, comprobar open',high',low',close'=a*(open,high,low,close)+b en cada timestamp, tolerancia absoluta 1e-7. Si falla, el contraste no corresponde a la transformación propuesta.
- En S+0 comprobar C y curvas iguales al original. Un fallo puede deberse a volumen, metadatos, resolución o datos internos: no equivale a demostrar dependencia del nivel de precio.
- Recuperar C con la recurrencia de los datos efectivamente exportados. Exigir acuerdo entre los seis canales Lite dentro de 1e-6 segundos y residuo de precio <=1e-7. Si falla, investigar la fuente efectiva antes de usar el resultado.
- Transformar también los precios auxiliares de las anclas si existen. Mantener todas las opciones iguales. Registrar tick mínimo y metadatos visibles; las diferencias pueden introducir redondeo o ramas por tipo de instrumento.
- Restaurar y repetir S al final. No interpretar cambios de un recálculo incompleto.

## Predicción e interpretación

Hipótesis H: C depende de la geometría relativa y tiempos de la trayectoria, con los demás datos relevantes conservados. Predicción: ambas transformaciones positivas conservan C en cada rango; las curvas Lite transformadas cumplen EMA'=a*EMA+b con la misma visibilidad.

Si desplazar cambia C pero escalar no, el resultado orienta hacia medidas porcentuales o ratios de precios. Si escalar cambia C pero desplazar no, orienta hacia magnitudes en puntos, ticks o umbrales absolutos. Si ambas conservan C, se obtiene invariancia para estos controles, compatible con varias reglas normalizadas, pero no prueba su invariancia universal ni identifica una fórmula. Si ambas cambian, revisar primero la compatibilidad de datos y metadatos.

Las diferencias son pistas condicionadas a los controles, no una identificación exclusiva del mecanismo. Toda la historia y las velas posteriores se transforman también: el experimento no localiza por sí solo si C utiliza datos anteriores a START o posteriores a END.

Una segunda tanda, solo si la primera resulta interpretable, puede invertir la dirección con K-S. Se deben intercambiar high/low, comprobar todos los OHLC y tratar volumen/metadatos con el mismo rigor. No usar invertir visualmente el eje como sustituto de transformar los datos.

## Estado

Se confirmó que el gráfico original está accesible desde este chat. No se modificaron símbolo, anclas ni ajustes, y no se midió C en expresiones sintéticas. La propuesta debe superar primero el control S+0; no se presupone que los indicadores protegidos admitan estos símbolos.
