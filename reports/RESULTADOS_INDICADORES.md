# Investigación de los indicadores PoiSzn

Fecha de observación: 12 octubre 2026. Gráfico: CME_MINI:NQ1!, velas de 1 minuto, ETH, UTC, sin ajuste por cambio de contrato. Layout dedicado: https://www.tradingview.com/chart/uXfdB8FS/

Actualización: el informe `PUNTO_1_PERIODOS_Y_ANCLA.md` amplía esta fase con diez configuraciones. Identifica la transformación de C a los diez períodos mediante bases 72/89 y factores de tres, confirma semillas low en casos alcistas y distingue la visibilidad de las curvas de su actualización. La generación de C desde el rango sigue abierta.

## Resultado comprobado

En la configuración manual probada, las diez curvas de Character Tree siguen la recurrencia de una EMA convencional sobre el cierre. Comparten una semilla al final del rango. En el primer caso, esa semilla coincide con el máximo de la vela final. La selección del rango modifica los períodos de las curvas.

Seven Cloud utiliza EMAs de 78 y 84 períodos sobre el cierre en el escalón de 1 minuto. Esta afirmación se comprobó numéricamente en el CSV, además de leer los ajustes. Las otras temporalidades están configuradas en su panel, pero todavía no se han validado con sus respectivos OHLC.

Estas observaciones describen las curvas. No establecen que las señales sean rentables, que aparezcan sin retraso ni que el sistema completo esté reconstruido.

## Versiones realmente cargadas

| Invitación | Indicador que carga en el gráfico |
| --- | --- |
| Character Tree v6.3 - User Release | Character Tree v6.5.36 - Public, CT6536USR |
| PoiSzn Seven Cloud EMA | PoiSzn Seven Cloud EMA v1.2.7, 7Cloud |
| PoiSzn · Manual Anchored CCII v3.9 | PoiSzn · Manual Anchored CCII v5.2, PoiSzn CCII |

Los nombres de invitación y de la instancia cargada difieren. Esta investigación corresponde a las versiones cargadas.

## Character Tree: prueba manual controlada

Ajustes: perfil B, selección Manual, resolución de datos manual 1 minuto, nubes extra y etiquetas de temporalidad activadas. Los precios asociados a los dos puntos manuales son ignorados según el texto del panel.

Se mantuvo el inicio a las 04:45 UTC y se modificó el final. Los intervalos entre los timestamps son de 15 y 30 minutos; si se cuentan ambas velas extremas contienen 16 y 31 velas respectivamente. Aún no se conoce cuál de estas convenciones usa la fórmula interna.

| Curva exportada | Final 05:00 UTC | Final 05:15 UTC, tras recargar |
| --- | ---: | ---: |
| Layer A | 24 | 46 |
| Layer A boundary | 30 | 57 |
| Layer B | 8 | 15 |
| Layer B boundary | 10 | 19 |
| Layer C | 3 | 5 |
| Layer C boundary | 3 | 6 |
| Extra cloud 1 | 72 | 139 |
| Extra cloud 1 boundary | 89 | 172 |
| Extra cloud 2 | 216 | 418 |
| Extra cloud 2 boundary | 267 | 516 |

Los valores son períodos equivalentes **en la resolución de 1 minuto probada**. No son períodos universales del indicador ni períodos de su resolución predeterminada de 1 segundo.

La recurrencia comprobada es:

```
alpha = 2 / (N + 1)
EMA[t] = EMA[t-1] + alpha * (close[t] - EMA[t-1])
```

Se ajustó alpha por mínimos cuadrados a diferencias entre muestras sucesivas de cada curva. Se compararon close, high, low, hl2 y ohlc4. Solo se utilizaron pares de velas consecutivas separados por 60 segundos y se omitió la última vela potencialmente en formación. En los dos casos, close identifica los períodos de la tabla con error por paso del orden de 10^-12 puntos.

### Reconstrucción completa del primer caso

En `character_manual_15m_1m.csv`, la primera muestra de curvas aparece a las 05:01 UTC. Invirtiendo esa primera actualización, todas las curvas dan una semilla común de **31,254.25**.

La vela final, 05:00 UTC, tiene O=31,253.50, H=31,254.25, L=31,244.75 y C=31,246.25. Por tanto, la semilla coincide con **high**, no con close. No se ha generalizado todavía esta regla a anclajes alcistas ni al modo automático.

Se reconstruyeron todas las curvas desde esa semilla, usando exclusivamente cierres OHLC y los períodos enteros identificados. La comparación contiene **877 muestras por curva**, 8,770 valores. El error absoluto máximo de toda la reconstrucción es **3.64 × 10^-11 puntos**, compatible con diferencias de aritmética de coma flotante. Esta prueba completa es más fuerte que comprobar una sola actualización.

El segundo CSV recargado contiene solamente un tramo posterior al ancla. Sirve para identificar la recurrencia y sus períodos, pero el estado anterior inferido desde su primera fila **no es la semilla original**.

### Recalcular después de modificar un ancla

Al cambiar el final de 05:00 a 05:15, el panel y el marcador cambiaron, pero la primera exportación mantuvo las curvas anteriores. Después de guardar y recargar el layout, una nueva exportación produjo los períodos diferentes de la tabla.

El archivo `character_manual_30m_1m.csv` conserva esa exportación desactualizada para trazabilidad. **No debe usarse como prueba del rango nuevo.** La evidencia válida es `character_manual_30m_1m_recarga.csv`.

Esta observación por sí sola no demuestra repintado ni identifica su causa. Para nuevas pruebas hay que recargar y verificar que el cálculo cambió antes de exportar.

## Seven Cloud

El panel expone dos longitudes: 78 y 84. La escalera configurada es 1s, 5s, 15s, 1m, 3m, 9m, 27m, 81m, 243m y 729m. También hay referencias de 2m, 6m, 15m, 60m, 162m y 486m. Tiene una opción para obtener escalones inferiores al gráfico mediante datos de temporalidad inferior.

En `seven_cloud_1m.csv`, las columnas `R4 E78` y `R4 E84` corresponden al escalón de 1 minuto. Aplicar la recurrencia sobre **close** con N=78 y N=84 reproduce cada actualización de **306 pares de velas cerradas** con error cero en la aritmética utilizada. High, low, hl2 y ohlc4 producen errores mayores. Los nombres «upper» y «lower» del panel no implican que las fuentes sean high y low.

El enfoque observado consiste en presentar pares de EMAs en diferentes temporalidades. El panel permite cambiar longitudes, temporalidades y visibilidad.

## Manual Anchored CCII

Este indicador pide seleccionar una vela CSD1 y un precio cercano a la mecha. El punto experimental elegido fue 12 octubre 19:21 UTC, high 30,870.50. No es una entrada de operación.

Su panel describe un detector de secuencia CSD1/CSD2/IDM1/IDM2, filtros de orden, niveles pendientes y completados, bandas ATR y breakaway gaps. No es una familia de EMAs. La transcripción del panel está en `ccii_inputs.txt`.

Detalles relevantes del panel, todavía sin validación independiente del algoritmo:

- La temporalidad de detección puede fijarse. En «Chart» cambia al cambiar la temporalidad del gráfico, lo que puede recomputar la secuencia.
- Para decidir el orden intrabar, el panel declara una suposición: vela alcista hace primero su mínimo; vela bajista hace primero su máximo. No equivale a conocer el recorrido real de ticks.
- Los niveles de previsualización durante una vela en formación pueden moverse o desaparecer. El panel indica que el nivel sólido se confirma al cierre.
- IDM tiene por defecto una ventana de 13 barras de detección, con filtros de orden entre niveles.
- Las bandas usan ATR de la temporalidad de detección, longitud 14 y semialtura 0.08 ATR por defecto.

No debe confundirse este indicador con Auto Zoom: la guía de Auto Zoom es otro producto y aún no se ha establecido una equivalencia entre ambos.

## Lo que queda por determinar

1. Fórmula general rango → períodos, con más duraciones y extremos distintos. Dos casos no bastan para distinguir reglas de redondeo o escalado.
2. Regla general de selección de semilla en rangos alcistas, bajistas y en Auto Balanced.
3. Actualización desde datos de 1 segundo y posibles sustituciones por datos del gráfico cuando faltan datos finos.
4. Detección automática del rango, cambios de dirección y gear shifts.
5. Momento de disponibilidad de BUY/SELL/EXIT/COVER en replay: aparición intrabar, confirmación, retraso o desplazamiento histórico.
6. Reproducción de los otros escalones de Seven Cloud y la secuencia CCII.
7. Evaluación de señales en sesiones diferentes, con reglas concretas de ejecución y costes. La coincidencia de curvas no valida un rendimiento operativo.

Las dos guías se descargaron y posteriormente se completaron sus transcripciones automáticas locales (`character_transcripcion_automatica.txt` y `auto_zoom_transcripcion_automatica.txt`). La revisión de esas transcripciones no identificó una fórmula explícita de C. Los controles posteriores y las búsquedas numéricas se documentan en `C_PRUEBAS_15_SEGUNDOS.md`; el origen de C desde OHLC sigue pendiente.

## Archivos y reproducción

- `identificar_emas.py`: estima fuente y período a partir de los plots exportados.
- `ajuste_emas.json`: ajuste de los dos casos válidos de Character.
- `verificar_nubes.py`: verifica Seven Cloud y reconstruye Character desde el ancla.
- `verificacion_nubes.json`: errores, número de muestras y OHLC del ancla.
- `graficar_reconstruccion.py`: crea la figura comparativa con Matplotlib.
- `reconstruccion_character.png`: curvas originales y reconstrucción, más error por muestra.
- `tradingview_investigacion.jpg`: estado del layout guardado. Seven Cloud y CCII están añadidos pero ocultos para ver Character con claridad.

Desde esta carpeta, con Python:

```powershell
python identificar_emas.py character_manual_15m_1m.csv character_manual_30m_1m_recarga.csv
python verificar_nubes.py
python graficar_reconstruccion.py
```

Los dos primeros scripts solo necesitan la biblioteca estándar. El tercero necesita Matplotlib, disponible en el Python instalado del equipo. Los CSV originales se conservan. La reconstrucción fue escrita a partir de las observaciones exportadas, sin acceso al código privado.
