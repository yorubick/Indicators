# Obtención de C y contraste de su cálculo

12 octubre 2026. Character Tree v6.5.36, perfil B, modo Manual.

## Estado

Ya se puede **recuperar C automáticamente de los plots exportados del indicador original**, con un intervalo de incertidumbre derivado del redondeo de sus períodos. La herramienta es `obtener_C.py`, usa solo la biblioteca estándar y se comprobó en 16 exportaciones.

**Todavía no se encontró la fórmula que genera C exclusivamente desde las velas del rango.** La extracción usa los plots originales. No sustituye al indicador para producir C sin acceso a él ni completa una réplica independiente.

**Límite de uso:** las pruebas posteriores de Auto Balanced no validaron la misma recurrencia sobre cierres del gráfico. El extractor actual se aplica a los controles Manual documentados con fuente y gráfico coincidentes; no debe atribuirse un C de Auto Balanced a partir de un ajuste aproximado. Véase `C_PRUEBAS_15_SEGUNDOS.md`, sección de selección de mecha en Auto Balanced.

## Experimento con END fijo

Se mantuvo END=19:20 UTC, gráfico de 1 minuto y fuente Chart. Se seleccionó un corte de replay a las 19:40, que muestra velas hasta 19:39.

| START | Duración | C entero compatible | Períodos de Extra cloud 1 |
| --- | ---: | ---: | ---: |
| 18:50 | 30 min | 118 s | 142/175 |
| 18:55 | 25 min | 62 s | 74/92 |
| 19:00 | 20 min | 77 s | 92/114 |

Los casos 18:50 y 19:00 repiten las mediciones anteriores con fuente explícita de 1 minuto. El caso 18:55 es nuevo y descarta una interpolación lineal de C entre esos dos resultados.

El rango de 25 minutos se comprobó otra vez tras salir de replay y permitir todo el historial posterior disponible. Mantiene el mismo intervalo compatible de C:

```
61.91011235955056 <= C < 62.08333333333334 segundos
```

Si C es un número entero de segundos, el único compatible es **62**. Las etiquetas visuales C/3≈20.67 s son consistentes con ese resultado. Que haya un único entero compatible no demuestra, por sí solo, que el cálculo interno siempre use enteros.

Se compararon **130 valores de curvas en timestamps comunes** entre la exportación de replay y la del gráfico completo. Coinciden exactamente. Esto demuestra estabilidad en ese control, no en todos los rangos o estados del indicador.

## Precio del primer punto

En el control START=18:50, END=19:20 se cambió Point 1 price de 31,228.710432720807 a 30,866, manteniendo las fechas. C sigue siendo compatible con 118 segundos y las longitudes siguen en 142/175 para Extra cloud 1.

Por tanto, el precio del primer punto no explica C en ese caso manual. Esta prueba respalda la interpretación de que los precios de los clics no son los parámetros que generan C en Manual. No se extiende a Auto Balanced, que sí usa el precio del segundo punto.

## Fuente de datos en replay

Con fuente explícita «1 minute», el primer corte de replay no produjo plots utilizables. Cambiar la fuente a **Chart**, con gráfico de 1 minuto, permitió calcular el rango y las curvas. El archivo `C_replay_1940.csv` documenta el intento sin plots y no se usa para inferir C.

Los controles posteriores usan Chart. En los dos rangos repetidos, sus C coinciden con las mediciones previas. No se atribuye el fallo inicial a repintado ni se ha identificado su causa.

El recálculo tarda algunos segundos. Tras cambiar parámetros, la caja puede actualizarse mientras los plots aún muestran valores anteriores. Las capturas y exportaciones confirmadas se tomaron después de observar el resultado actualizado. No se deben comparar valores inmediatamente después de pulsar Ok.

## Modelos contrastados

Se contrastaron duración, amplitud del rango, rangos medios de vela, cuerpos medios, true range, equilibrio del rango y ajustes de EMA hacia delante y hacia atrás.

La búsqueda numérica adicional comparó una clase explícita de modelos con:

- una EMA de longitud N=K×C/Δ y una constante K común a todos los casos;
- fuentes open/high/low/close/hl2/hlc3/ohlc4;
- recorridos cronológicos e inversos;
- distintas inclusiones de las velas START y END;
- semillas y objetivos obtenidos de OHLC, extremos y punto medio del rango;
- selección de mechas basada en cuerpo o posición frente al punto medio.

No se encontró una combinación que explicase los ocho casos no saturados contrastados con la precisión de C observada. Los resultados están en `busqueda_operador_C.json` y la búsqueda reproducible en `buscar_operador_C.py`.

La exploración cubre N entre aproximadamente 1 y 10,000, con una malla logarítmica y raíces interpoladas. **No demuestra que ningún algoritmo de EMA pueda producir C.** No incluye, por ejemplo, filtros múltiples, ajuste por eventos, ventanas parciales elegidas dinámicamente o reglas distintas por régimen. Es un descarte de esa clase concreta de modelos simples.

## Consulta de la guía

Se transcribió localmente el audio de Character-Tree-081026.mp4. El video no se envió a un servicio de transcripción. La transcripción automática se guarda como `character_transcripcion_automatica.txt` y `.json`.

La explicación habla de elegir y ampliar el rango observando la interacción con las EMAs y de los modos automáticos de una versión anterior. La transcripción no aporta una ecuación de C. La guía utiliza una versión anterior a la instancia v6.5.36 probada y la transcripción puede contener errores en términos técnicos; no se utiliza como prueba de la implementación actual.

Se terminó también la transcripción local de Auto-Zoom-081026.mp4 (`auto_zoom_transcripcion_automatica.txt` y `.json`). Entre aproximadamente 8:32 y 8:53 se describe que el árbol de EMAs está integrado en el OLR y que se forma un árbol nuevo con cada setup. Explica las nubes y sus señales, pero la transcripción tampoco aporta una ecuación que transforme las velas del rango en C. Los grados A/B/C de setups mencionados después no deben confundirse con la escala Character C investigada aquí.

Para transcribir se instalaron dependencias en `G:/trading/.tools/asr` y se descargaron pesos del modelo en `G:/trading/.tools/modelos_asr`. La inferencia se ejecutó en CPU. El audio de análisis es `character_audio.wav`. No se modificaron los paquetes globales de Python.

## Cómo obtener C en un rango nuevo

1. En el layout de investigación, seleccionar Manual, perfil B y activar las nubes extra.
2. Usar **Chart** como resolución manual y elegir la temporalidad de gráfico que se quiere analizar. Así, los cierres exportados y la fuente de las EMAs tienen el mismo intervalo.
3. Seleccionar START/END y esperar a que termine el recálculo. Deben existir suficientes curvas visibles; una caja sin plots no permite esta extracción.
4. Exportar mediante Manage layouts → Download chart data, con timestamps UNIX.
5. Ejecutar, sustituyendo el archivo por el CSV exportado:

```powershell
python G:\trading\guias\analisis\obtener_C.py "C:\Users\PC\Downloads\CME_MINI_NQ1!, 1.csv"
```

La herramienta identifica el intervalo de los timestamps, ajusta la recurrencia de las diez EMAs sobre close y comprueba que sus longitudes son enteras. Después intersecta las restricciones de redondeo de la familia 72/89. Devuelve el intervalo de C, los enteros compatibles, los períodos y el error del ajuste.

Se requieren al menos cinco pares consecutivos por curva. Si la fuente interna es más fina que la temporalidad exportada, las curvas no coincidirán con una EMA de los cierres exportados y la herramienta lo rechazará. Ese rechazo se comprobó con el CSV anterior que usa fuente de 1 segundo sobre gráfico de 1 minuto.

Las 16 extracciones comprobadas están en `C_extracciones_verificadas.json`. Incluyen repeticiones y controles, no son 16 rangos independientes.

## Pendiente para una réplica independiente

Sigue faltando identificar el operador que transforma las velas START–END en C, junto con la clasificación del lado inicial. No se ha introducido una fórmula aproximada como sustituto de esa parte desconocida.

El layout se dejó con START=18:55, END=19:20, gráfico de 1 minuto, fuente Chart, modo Manual y Direction mode Auto. C≈62 s permite revisar la nueva medición.

## Sensibilidad al inicio: controles adicionales

Se movió START minuto por minuto, manteniendo END=19:20 UTC, perfil B, Manual y fuente Chart de 1 minuto. Todos los casos siguientes tienen el mismo máximo **30,870.50**, mínimo **30,846.00** y vela END (O=30,866.25, H=30,870.50, L=30,864.50, C=30,870.50).

| START UTC | Duración | Único C entero compatible |
| --- | ---: | ---: |
| 18:54 | 26 min | 134 s |
| 18:55 | 25 min | 62 s |
| 18:56 | 24 min | 109 s |
| 18:57 | 23 min | 77 s |
| 18:58 | 22 min | 77 s |
| 18:59 | 21 min | 77 s |
| 19:00 | 20 min | 77 s |

El caso 18:54 se repitió tras recorrer los demás inicios: conserva exactamente el mismo intervalo de C [133.82022471910113, 134.02777777777777) y los diez períodos. Cada extracción nueva tiene al menos 85 pares consecutivos por curva y un error de recurrencia menor de 2×10⁻¹² puntos. Se comprobó además que el OHLC de las 21 velas comunes 19:00–19:20 coincide en todos estos archivos y en el control 18:50.

**Conclusión limitada:** C no depende exclusivamente del máximo, mínimo y OHLC final del rango. Tampoco es una función estrictamente creciente de su duración en estos controles. Los casos 18:57–19:00 producen las mismas longitudes a pesar de retirar tres velas. Esto deja abiertas reglas basadas en eventos, ventanas efectivas o ajustes con ramas; no demuestra cuál de ellas utiliza el autor ni que la vela inicial sea el único dato relevante.

Las mediciones y comprobaciones reproducibles están en `C_sensibilidad_inicio.json` y `C_sensibilidad_inicio.py`. Se conservan seis exportaciones adicionales (cinco inicios nuevos y una repetición). La fórmula generadora de C sigue sin identificar.

Se continuó con trece inicios cada 15 segundos y cinco finales cada minuto, manteniendo fuente y gráfico de 15 segundos. El detalle y la distinción de cobertura temporal frente al caso de un minuto están en [C_PRUEBAS_15_SEGUNDOS.md](C_PRUEBAS_15_SEGUNDOS.md). Los saltos principales se confirmaron por repetición. Esta fase tampoco identifica todavía la fórmula generadora.
