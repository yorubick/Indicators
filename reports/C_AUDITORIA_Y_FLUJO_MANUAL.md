# Auditoría de END y reconstrucción de la selección de rama

13 de octubre de 2026. Análisis local de 38 casos Manual con fuente y gráfico coincidentes. No se modifica TradingView.

## Resultado

**34 casos permiten reconstruir las diez curvas desde END**, con 89,690 valores contrastados y error máximo aproximado de `9.83e-11` puntos. En esos mismos 34 casos, la primera aparición de todas las curvas coincide con el primer cierre posterior a END estrictamente fuera del máximo/mínimo global del rango seleccionado.

Cuatro exportaciones antiguas no contienen plots en los primeros 90 minutos después de END. No son fallos de la regla: quedan **no comprobables en esta auditoría**. Son `character_manual_30m_1m_recarga.csv`, `character_20m.csv`, `character_40m.csv` y `character_5m.csv`. El script registra los OHLC de apoyo y los huecos; no inventa valores de plots ausentes. Los OHLC comunes de los archivos de apoyo se comparan con los originales.

El control de END y de recurrencia no certifica por sí solo que START haya sido aplicado correctamente. Dos selecciones con END y C iguales pueden producir las mismas curvas. Los casos antiguos sin repetición siguen necesitando trazabilidad de UI para una certificación definitiva de las anclas. Las cuatro nuevas mediciones aceptadas conservan su verificación por exportaciones repetidas.

## Regla de selección de semilla contrastada

Se compara la mejor semilla low/high de END con tres predictores:

| Predictor | Coincidencias en los 34 casos comprobables |
|---|---:|
| Cuerpo de END: alcista → low, bajista → high | 27 |
| Desplazamiento cierre START → cierre END: positivo → low, negativo → high | 30 |
| Primera ruptura por cierre: arriba → low, abajo → high | 34 |

Los dojis y desplazamientos nulos se asignan a low en los dos primeros predictores. Los contraejemplos completos están en el JSON.

Que la primera ruptura prediga la semilla no demuestra que el código original la use internamente. Puede existir otra regla correlacionada con ella. Sí permite una reconstrucción alternativa que no consulta precios futuros para elegir una rama al publicar las curvas.

El conjunto está desequilibrado: 33 casos comprobables rompen por arriba y solo uno por abajo. La coincidencia bajista necesita más rangos independientes antes de generalizarla.

## Reconstrucción que procesa las velas en orden

`flujo_manual.py` implementa este procedimiento con C como entrada:

1. Calcular los períodos de la familia ya identificada.
2. En END iniciar dos familias EMA: una desde low de END y otra desde high de END.
3. Procesar cada cierre posterior en ambas familias, incluso mientras no se muestran curvas.
4. Al primer cierre estrictamente superior al máximo global del rango, seleccionar la familia iniciada desde low. Al primer cierre estrictamente inferior al mínimo global, seleccionar la iniciada desde high.
5. Publicar los valores de la rama seleccionada desde esa vela.

La elección se realiza usando solamente la vela procesada y las anteriores. No se escoge la semilla ajustándola a los plots originales. El script de auditoría confirma de nuevo las 34 reconstrucciones bajo este procedimiento.

Este avance precisa la inicialización y la primera aparición de las curvas. **No genera C desde OHLC**, ni reproduce señales, cambios posteriores de modo, alertas o el comportamiento Auto Balanced. El control se limita a los plots de los casos comprobables en una ventana de hasta 90 minutos después de END. La saturación y el redondeo de períodos son los ya contrastados para esta familia.

## Reproducción

Ejecutar `auditar_C_ancla_completa.py` con Python y NumPy. Resultados por archivo, candidatos de semilla, contraejemplos, huecos y errores de reconstrucción: `C_auditoria_ancla.json`. La clase de procesamiento en orden está en `flujo_manual.py` y recibe C en segundos explícitamente.

La investigación del generador de C continúa abierta. Esta auditoría aporta una comprobación amplia de las mediciones y una pieza funcional de la réplica con C proporcionado; no debe presentarse como ingeniería inversa completa.
