# Geometría y EMAs históricas: estados simples insuficientes

14 octubre2026. Análisis exploratorio de9rangos ya medidos en NQ1!,12octubre UTC,fuente/gráfico1m. Mediciones declaradas en C_GEOMETRIA_EMA_MEDICIONES.json antes de calcular métricas. No se optimizaron períodos,umbrales ni regresiones usando las etiquetas C.

## Método y cobertura

Posiciones de open/close respecto a H/L,cuerpos y mechas divididos por altura,variación total de cierres/altura,eficiencia abs(último−primero)/suma de movimientos absolutos y pendiente lineal/altura. Estas métricas no se denominan fases armónicas.

EMAs históricas de cierre de períodos24,89/3,8,89/9,72/27,89/27 más72y89. Las seis primeras son proxies derivados de la arquitectura de salida para C60; no sabemos si son las longitudes históricas internas del autor. Se midieron distancia close−EMA/altura,pendiente/altura,ancho absoluto de cada par/altura,posición arriba/dentro/abajo y número de cruces. Los valores continuos son mediciones, no predictores validados.

Primer CSV desde16:01 tenía173velas antes de START18:54; EMA89 podía cambiar de signo en END19:20 bajo semillas iniciales±100puntos. Por ello se amplió el historial real de TradingView y se exportó desde08:50:604velas previas. Recalculadas las mismas longitudes,sin elegir otras,no hay signos inestables bajo ese control. Para START18:54 el efecto de±100 en distancia normalizada es2.28×10⁻⁷ para EMA72 y5.60×10⁻⁶ para EMA89. Este control no garantiza una cota de toda historia verdadera desconocida.

La exportación ampliada conserva exactamente OHLCV y seis curvas de Lite en2.725velas comunes; C62 persiste. Mostrar más historia no prueba que antes Pine careciera de ella ni constituye corte de Replay.

## Medidas de geometría

| Rango UTC | C | Posición close START | Posición close END | Eficiencia |
|---|---:|---:|---:|---:|
|18:54–19:19|134|0.538462|0.901099|0.100917|
|18:54–19:20|134|0.500000|1.000000|0.142857|
|18:54–19:21|109|0.500000|0.918367|0.116809|
|18:55–19:19|107|0.439560|0.901099|0.132075|
|18:55–19:20|62|0.408163|1.000000|0.173653|
|18:55–19:21|106|0.408163|0.918367|0.146199|
|18:56–19:19|77|0.285714|0.901099|0.184211|
|18:56–19:20|109|0.265306|1.000000|0.225000|
|18:56–19:21|134|0.265306|0.918367|0.195122|

El mínimo C62 no tiene máxima eficiencia; esta es0.225 en C109. La eficiencia sola no presenta una relación monotónica global con C en estos9casos. La posición inicial sola tampoco determina C: posición0.408163 ocurre en C62y106. La posición final sola tampoco:END en máximo(1.0) da C134,62y109. Estas observaciones no excluyen combinaciones ni relaciones no lineales.

## Estados EMA que no explican C

Seis casos18:55/18:56x19:19/19:20/19:21 empiezan bajo las seis EMAs cortas y terminan sobre ellas; C107,62,106,77,109,134. Todos tienen los mismos conteos de cruces[7,1,5,5,11,11]. Por tanto esas firmas discretas solas no determinan C.

La combinación ampliada de signos de START/END,conteos de cruces y orden relativo de las seis EMAs en ambos bordes también produce colisiones:

-18:54–19:20(C134) y18:54–19:21(C109).
-18:55–19:19(C107) y18:56–19:19(C77).
-18:55–19:20(C62),18:55–19:21(C106),18:56–19:20(C109),18:56–19:21(C134).

Agregar signos/cruces de EMAs72/89 no separa el último grupo: todos empiezan por debajo de ambas; terminan sobre72,bajo89,con1cruce de72y0de89. Distancias y pendientes exactas sí cambian: por ejemplo,para START18:55,EMA72 termina a0.108707alturas de close en19:20 y0.026332en19:21. Ese cambio no proporciona por sí solo una conversión a62/106.

## Conclusión limitada

Se refutan estas reglas concretas basadas únicamente en estados de las EMAs proxy y esas métricas simples. No se refutan todas las longitudes posibles,distancias continuas,EMAs ancladas al setup,fases de otras familias ni armónicos en general. No se descubrió fórmula de C ni predicción nueva defendible. Aprender una tabla que distinga los9casos sería ajuste retrospectivo.

Siguiente análisis útil: aplicar estas mismas medidas,sin cambiar sus definiciones,a controles anteriores fuera de esta matriz y exigir que una hipótesis explique tanto sus simetrías como cambios de C. Solo después declarar predicciones para ventanas nuevas. La falta de una explicación con estos períodos no autoriza una búsqueda ilimitada de longitudes ajustada a cada etiqueta.

Artefactos: medir_C_geometria_ema.py,C_geometria_ema_resultados.json(historia corta),C_geometria_ema_historia_larga_resultados.json y tablasCSV respectivas. Resultados completos incluyen distancias,pendientes,anchos,cuerpos/mechas,sensibilidad,firmas y hash de fuente. Historial ampliado en manual/C_startSweep1920_geometria_historia_larga.csv. Gráfico conservado en NQ1!,1m,rango18:55–19:20,vista19:10; layout principal sin cambios.
