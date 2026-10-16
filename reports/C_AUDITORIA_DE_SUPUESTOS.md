# Pausa de investigación: qué falta para encontrar C

13 de octubre de 2026. Auditoría de informes, protocolos y transcripción local de Character. Sin nuevas mediciones ni cambios de TradingView. No se identificó el generador de C.

## La principal laguna

Gran parte de nuestras búsquedas supone que C es una función exclusivamente del OHLC comprendido entre START y END, a la resolución elegida para las EMA. Ninguna de esas dos premisas está demostrada.

1. La regla de actualización de las EMA identifica su fuente de precios y su resolución efectiva. No identifica necesariamente la serie usada por el cálculo previo de C. Ese cálculo podría usar otra resolución, estado acumulado anterior, o una selección interna de velas. Son posibilidades, no hallazgos.
2. Los cortes de replay del caso C134 confirman estabilidad de las curvas publicadas hasta cortes posteriores, pero dejan sin excluir datos entre END19:20 y la ruptura19:26. El primer corte con extracción estricta fue19:33; no medimos un C observable al cierre de END.
3. Ampliar historial exportado y recargar conservó C134, pero no eliminó las series internas previas proporcionadas por TradingView. Ese control no prueba independencia de toda prehistoria.

Las restricciones anteriores están expresamente registradas en C_PRUEBAS_15_SEGUNDOS.md, sección «Historial previo, replay temprano y aparición de curvas». Varias búsquedas posteriores adoptaron OHLC del rango como universo de hipótesis sin haber cerrado esas restricciones.

## Qué sí está identificado

- Se infiere C a partir de los períodos de las curvas. Lite elimina en las muestras la ambigüedad causada por redondear períodos.
- Con C suministrado, se reconstruyen las EMA, sus semillas en END y su primera publicación en los casos comprobados.
- Retirar una vela inicial o añadir una final puede producir saltos grandes de C conservando los extremos globales.
- Lite y Character coinciden en catorce configuraciones, todas de una jornada y dos episodios. No son catorce experimentos de mercado independientes.

Estos resultados caracterizan la salida del indicador. No equivalen a identificar el generador. Que C se exprese en segundos en nuestra normalización o etiquetas no implica que el código lo obtenga midiendo directamente una duración.

## Otro límite del método usado

Hemos rechazado muchas familias diseñadas por nosotros: C proporcional a una medida con un K común, raíces de condiciones específicas de EMA, eventos y ventanas prefijados. El número de variantes no mide la proximidad a la fórmula del autor. Un selector de ventana, una condición lógica o una selección de rama podría producir saltos que esas familias no incluyen.

La repetición de C106 en varios rangos y la secuencia115/106/79/66/106 justifican investigar selección discreta de soluciones o estados. No demuestran catálogo de valores: los resultados también son compatibles con una fórmula continua cuantizada a segundos. Debemos distinguir ambas posibilidades mediante pruebas, sin afirmar ninguna.

La guía automática transcrita explica anclaje y modos Manual/Balanced/Broad; no proporciona la función generadora. Es una transcripción automática y no debe usarse para inferir términos matemáticos del autor que no estén claros.

## Prioridad 1: establecer cuándo C es observable y estable

Usar dos casos de START ya fijados con fuente15s:18:54:15–19:20 (C118) y18:54:30–19:20 (C67). En ambos, la primera publicación histórica es19:20:45. Incluir después un caso bajista1m:04:45–05:30 (C110), ruptura05:36.

Para cada caso:

1. Seleccionar el corte de replay cerca de END, con fuente explícita y anclas verificadas. Comprobar en el CSV el último timestamp, el OHLC cerrado real y los plots; no asumir que el corte solicitado ya produjo la actualización correspondiente.
2. Observar antes de la ruptura, inmediatamente tras ella y después de dos, seis y más velas cerradas. Guardar dos exportaciones por estado. Para evaluar estado persistente, repetir un arranque de replay directamente en un corte temprano y otro avanzando desde antes de END, siempre comprobando las anclas y la resolución.
3. Comparar plots comunes cerrados por timestamp y recuperar C del primer tramo suficiente. Lite permite estimar alpha mediante pares consecutivos sin exigir períodos enteros; para muestras cortas exigir acuerdo de las seis curvas, repetición y denominadores informativos. La última fila se excluye por el desfase ya observado.
4. Registrar «C no observable» cuando no hay curvas o pares suficientes. Nunca registrar C=0 ni concluir que el cálculo aún no existe por falta de plots.

Interpretación: si las curvas históricas anteriores cambian al avanzar, hay una dependencia de datos posteriores o estado que debemos localizar. Si no cambian, se acota la estabilidad de lo observable a esos cortes; no se prueba independencia de la información entre END y la ruptura. Si C no puede observarse antes de la ruptura, ese límite permanece explícito.

Este protocolo no pretende que Replay permita editar OHLC. Tampoco equivale a una auditoría interna de request.security ni excluye todas las series que TradingView pueda proporcionar al script.

## Prioridad 2: separar serie de cálculo de C y serie de salida

Mantener anclas temporales exactas y fuente explícita mientras se cambia solo el intervalo del gráfico, usando intervalos compatibles con la fuente. Elegir un caso sin saturación mínima. Comparar timestamps, C y OHLC fuente efectivos. Después mantener gráfico compatible fijo y cambiar únicamente la fuente.

Invariancia ante cambiar gráfico apoya independencia del intervalo visible, pero no identifica por sí sola la resolución interna usada para generar C. Cambiar fuente modifica la agregación: no debe confundirse con editar un solo parámetro sobre una trayectoria idéntica. Documentar cualquier dato fuente ausente, fallback y error de resolución; no aceptar exportaciones obsoletas tras cambios.

## Prioridad 3: rangos mínimos y selección discreta

Una vez asegurada la fuente efectiva, medir rangos de una, dos, tres y cuatro velas cerradas en episodios alcistas, bajistas y mixtos. Repetir en dos resoluciones y otra jornada. En esas ventanas se pueden enumerar manualmente todos los precios y condiciones de borde.

Si todos los C se saturan en la resolución, el experimento informa del límite pero no del generador: pasar a la ventana más corta que dé C por encima del mínimo. Examinar si las transiciones ocurren por añadir un extremo, por cuerpo/dirección, o por cambiar una condición de selección. No deducir una regla solo porque encaje en dos ejemplos.

## Decisión

Pausar la ampliación de barridos de fórmulas proporcionales. La siguiente tanda debe cerrar primero las dependencias observables y la fuente efectiva. Solo entonces elegir una hipótesis que prediga por adelantado un cambio de C y contrastarla en una jornada distinta. Registrar predicción, condición de rechazo y resultado; no elegir una raíz o ventana por su cercanía al C ya conocido.
