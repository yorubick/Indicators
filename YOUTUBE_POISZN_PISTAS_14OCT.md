# Fuentes públicas que cambian la prioridad experimental

Revisión14octubre2026. Se leyeron descripciones y transcripciones automáticas; no se recuperó código privado ni una fórmula de C. No se modificó TradingView.

Dynamic EMA,2octubre2026:
https://www.youtube.com/watch?v=DS0Pcm2z_qY
Tiempos relevantes:0:15–0:40,1:17–1:35,2:34–3:10,3:34–4:31,4:34–5:55,6:18–6:41,8:18–8:42.
Describe familias según caja,anclas estructurales alternativas,reconfiguración al mover bordes y preferencia por fuente1s si existe cobertura. La caja elegida representa acumulación para su esquema de fases. No explica una fórmula de C ni confirma ancla automática anterior a START.

CSD Fractal Model,10septiembre2026:
https://www.youtube.com/watch?v=dHv7HH9BZSU
Tiempos relevantes:1:24–3:43,6:22–6:51,12:43–13:20,20:45–22:05.
Define secuencia de cuatro etapas por cambios de dirección y toma de extremos previos; distingue igualdad de barrido efectivo. Explica fijar temporalidad de detección y subir dos niveles de potencias de tres desde la EMA observada para elegir temporalidad fractal. No ofrece conversión numérica a C.

Inferencias a verificar, no afirmaciones del autor: los futuros ejemplos visuales deben marcar primero los eventos estructurales y usar los mismos tipos de ancla. Probar mapeo entre familia y temporalidad, no suponer que potencias de tres implican frecuencia sinusoidal. Las reglas descartadas sobre proxies72/89 y estados discretos no descartan el sistema de longitudes dinámicas del autor. Cambiar cuadro de detección, fuente y gráfico son intervenciones diferentes.

Prioridad:1)identificar eventos de ancla sin usar C;2)repetir mismo rango y fuente con control de versión/cobertura;3)comparar familias y temporalidades1/3/9/27 guiadas por los videos;4)contrastar hipótesis de geometría o ancla oculta con predicción nueva. Comparaciones visuales y numéricas pueden avanzar juntas; no es necesario agotar todas las hipótesis antes.
