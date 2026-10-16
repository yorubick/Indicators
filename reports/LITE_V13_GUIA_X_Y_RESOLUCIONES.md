# Lite v1.3, guía de X y contraste de resoluciones

14 octubre 2026. Lectura directa de la publicación TradingView en navegador autenticado y del post compartido por el usuario. No se modificó el gráfico de investigación ni se realizaron nuevas mediciones deC.

## Fuentes y versión

- Publicación: https://www.tradingview.com/script/B2yVeJKv-PoiSzn-EMA-Origin-Lite-v1-2/
- Guía: https://x.com/PoiSzn/status/2110110293837652362
- La cabecera sigue mostrando v1.2, pero las notas dicen Release Notes v1.3, actualización14oct2026. La fecha/hora visible fue01:14CST; no se usa el tiempo relativo como evidencia de un cambio matemático.
- Las notas dicen: default de resolución1m por compatibilidadEssential;1s sigue disponible donde esté soportado; sin cambio declarado a anclaje manual,trazadoEMA,proyeccionesfib oPDA. No afirman que toda la implementación oCsea idéntica: repetir un control con resolución explícita antes de combinar mediciones de versiones.
- Es público y gratuito, de código protegido. La invitación deCharacter impide acceso público sin autorización, pero la cuenta del usuario sí permite inspeccionar sus ajustes y salidas; no permite leer su Pineprivado.

## Guía en audio

El video está accesible sin iniciar sesión en X. Se guardó su audio completo mediante el playlist observado en el navegador; el primer MP4 observado era solo un fragmento de inicialización y no contenía la charla. Audio completo: G:/trading/guias/Lite-X-2110110293837652362-audio-completo.m4a.

Se transcribió localmente con el modelo ya instalado, sin enviaraudio a un servicio. Archivos Lite_X_2110110293837652362_transcripcion.json/txt. La transcripción automática tiene errores, por ejemplo nombresFVG y retracement; no atribuir palabras técnicas dudosas como citas exactas.

Lectura contextual de la transcripción:

- Aproximadamente0:33–1:30: selección de máximo→mínimo→retroceso para un caso bajista y secuencia opuesta para alcista; lasEMAse adaptan a la caja elegida. Es una pista de cómo usar las anclas, no una fórmula deC.
- Aproximadamente1:39–1:44: recomendación relacionada con datos en segundos cuando estén disponibles y1mcomo alternativa. La transcripción de la frase no es suficientemente clara para citarla literalmente; las notas oficiales sí confirman1s/1m.
- Aproximadamente1:48–2:11: la explicación del timeframe inferior separado está en el contexto dePDarrays. No trasladarla aCni al origen de los períodosEMAcomo si fuera una afirmación expresa.
- Aproximadamente3:40–4:32: proyecciones basadas en altura de caja, con niveles1,1.5,2,2.5,3.5,4según la transcripción. La publicación oficial denomina estas proyeccionesFibonacci. No demuestra queCuseesos mismos niveles.
- La segunda parte muestra funciones de la versiónpremium. Mantener separados el motorLitey las señales del comprado.

## Texto adicional aportado por el usuario

Describe funciones tácticas de primeras medias, una central y dos de agotamiento. No proporciona un cálculo de longitud. Sin URL oimagen de ese segundo post, no podemos identificar con seguridad qué curvas o versión denomina:Liteexporta6curvas en3pares yCharacterexpone5nubes en10curvas. No contar las palabrasdelpostcomo si fueran nombres deplots.

## Prueba propuesta con resoluciones

Primero repetir un control conocido con resolución explícita1m en la versión actualmente cargada. Registrarversiones,anclas,CSVpares yC. No comparar un default antiguo contra un defaultnuevo como cambio de algoritmo.

Después, sobre un tramo reciente con datos1scompletos y anclas de minutos:

1. Fijar gráfico1m y variar únicamente resolución de cálculo1s,15s,1m (si están disponibles).
2. Exportar OHLCnativo de las fuentes y verificar primera/última vela incluida. La etiqueta de hora no basta:Liteincluye subvelas de la vela del gráfico que contieneENDen los controles anteriores.
3. RecuperarCalineando actualizaciones nativas. No ajustar unaEMAde1actualización por minuto si su fuente realiza60actualizaciones1s.
4. Fijar fuente1s y comparar gráficos1m/3m solo con coberturaENDefectiva igual. Verificar semillas y compensar su diferencia para comparar niveles; no atribuir aCuna diferencia causada por semilla.
5. Anotar cantidad de muestras, cobertura y volumen. La elección1senelinputno prueba que haya datos1spara todo el rango. TradingView tiene límites a las intrabarras solicitadas; una serie ausente hace inválida la comparación, no demuestra un ciclo o un fallback específico.

Fuente sobre límites: https://www.tradingview.com/pine-script-docs/writing/limitations/

Interpretación: siCseconserva al variar gráfico con fuente y datos efectivos fijos, respalda que la escala provenga de la fuente elegida para esos casos. Si cambia, existe otra dependencia observable por investigar. La resolución elegida modifica la agregación del precio;noesreescala temporal exacta de una señalidéntica.

## Prueba mínima nueva en1s

Si hay cobertura y la extracción está validada a1s, usar gráfico/fuente1s y19/20/21velas exactas. La regla corta existente prediceC19=190/183=1.0382513661 yC20=200/183=1.0928961749. La continuación de esa regla para21sería210/183=1.1475409836; se registra como control de continuación, no como predicciónvalidada de la rama larga.

Esto puede llevar la frontera desde20minutos(fuente1m) a20segundos(fuente1s) y dar un caso pequeño para examinar el recorrido. SiC21coincide con la continuación, una sola igualdadnoexcluyeuncambiodealgoritmo; si cambia, será compatible con una frontera por conteo en esa fuente, no prueba de armónicos.

## Hipótesis armónica que estas notas justifican investigar

Relaciones geométricas de impulso/retroceso y escalas entre filtros, además de ciclos sinusoidales. Son hipótesis diferentes. Las notas identifican proyeccionesFibonaccideprecio; la familiaEMAyaidentificada utiliza3/9/27. Aún no hay evidencia de que cualquiera deesasdosarquitecturas genereC.
