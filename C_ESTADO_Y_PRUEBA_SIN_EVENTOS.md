# Suficiencia del estado y prueba prospectiva sin eventos

13 octubre2026. Continuación de la base experimental de Gemini. No se identificó el generador generalC. Se probaron conjuntos de entradas del estado usando solamente entrenamiento yse midieron cuatro selecciones nuevas de otra jornada, con predicciones anteriores a observarC. Los27controles largos de validación originales siguen sin usarse para ajustar o puntuar este candidato.

## Estado final propuesto: contraejemplo exacto

Los controles19:01–19:23 y19:02–19:24 del12oct tienen fuente60s,23velas,high30870.75,low30849.00, amplitud21.75 yENDsin nuevo extremo global. Sin embargo, C=77 y55. Una función determinista que reciba solo esas variables no puede producir ambos resultados. Cambiar los umbrales de amplitud o conteo no corrige una entrada idéntica.

Se compararon11conjuntos explícitos de variables en32rangos largos de entrenamiento. Los conjuntos de conteo/extremos/banderas anteriores tienen contradicción; extremos,velaEND,edades de extremos yedades del último pivote sin conteo también presentan10pares contradictorios. Añadir suficiente detalle produjo32entradas únicas:que no haya contradicción en ese caso no valida una fórmula, porque ningún estado se repite.

Los timestamps absolutos se omitieron deliberadamente en estas pruebas:conteo yENDabsoluto pueden identificar una ventana yvolver trivial la ausencia de contradicciones. No se afirma que el algoritmo original ignore la hora. Script `probar_C_suficiencia_estado.py`; salida `C_suficiencia_estado.json`.

## Eventos definidos y alcance del ensayo

Se definieron cuatro eventos observables: nuevohigh global estricto, nuevolow global estricto, nuevohigh local radio1 confirmado y nuevolow local radio1 confirmado. Radio1 exige extremo estricto frente a izquierda ypermite empate a derecha. La confirmación ocurre al recibir la vela derecha, no antes.

En21transiciones consecutivas deENDcon STARTfijo de entrenamiento,13cambianC y8lo conservan. La unión de eventos aparece en20/21transiciones, por lo que tenerla presente discrimina poco. Siete transiciones tienen evento pero no cambianC; la única sin evento conservaC. Esto justificó buscar controles nuevos sin eventos, en lugar de declarar demostrada una máquina de estados.

Ningún evento individual es condición necesaria para todos los cambios de estos controles. Por ejemplo,7cambios ocurren sin nuevohigh global y9sin nueva confirmación dehigh local. No se extrapola a cualquier detector de pivotes. Script `probar_C_eventos_estado.py`; salida `C_eventos_estado.json`.

## Selección y predicción prospectiva

Usando únicamenteOHLC de13oct se eligieron cronológicamente las primeras dos ventanas no solapadas de22velas entre06:00y18:59, amplitud>=5puntos, sin ninguno de los cuatro eventos al agregar la vela22. Se verificó que esas selecciones no estaban en el conjunto93. No se consultóCpara elegirlas.

Hipótesis operacional limitada:si C solo cambia cuando ocurre alguno de esos cuatro eventos, sin ellos deltaC=0. Esa predicción se registró para ambos pares antes de medir sus dosC. Es una predicción del cambio, no un cálculo delC inicial. Archivo `C_sin_evento_predicciones.json`; selector `seleccionar_C_sin_evento.py`.

| START13octUTC | ENDantes ->después | Cantes ->después | Predicción deltaC=0 |
|---|---|---|---|
|06:00|06:20 ->06:21|75 ->75|Pasa|
|06:25|06:45 ->06:46|87 ->84|Falla|

El segundo caso refuta la necesidad de esos cuatro eventos para cambiarC. High30675.25 ylow30644.50 se conservan; los índices de los últimos pivotes confirmados también:high índice19,low índice18. Cambian el conteo21→22,el cierre30651.75→30652.50 ylas edades relativas (últimohigh confirmado1→2velas, último low2→3). Por tanto, un estado que también actualice edades, precios uotras estadísticas sigue siendo posible. No se descartó toda máquina de estados ni todos los pivotes.

En el primer casohigh30694.25 ylow30633.25 se conservan; C75persiste pese al cambio de cierre30651.25→30655.25 yconteo. Ninguno de los dos casos identifica una fórmula de edades o cierres por sí solo.

## Repetición y verificación

Las cuatro selecciones nuevas tienen fuente ygráfico1m,Lite fuente1m yCharacter Tree v6.5.36 perfilB Manual fuenteChart,ETH,UTC,BADJapagado,Replayapagado. Cada pareja pasa coberturaOHLC exacta igual a la selección previa,estabilidad16curvas yacuerdo de seis estimacionesLite con el intervaloCharacter. Las cuatro parejas aceptadas comparan172,640celdas de curvas cerradas,excluyendo última fila.

El par87/84 se repitió desde otra selección. Las e/f reproducen los dosC ycoinciden con la primera exportación d en43,152celdas por selección. No se usa un cambio observado una sola vez ni se confunde un recálculo antiguo con el resultado.

CSV/capturas:`manual/C_noevent_1_before/after_*` y`manual/C_noevent_2_before/after_*`. Para el segundo par se aceptan e/f yse preservan c/d. Analizador `analizar_C_sin_evento.py`; resultados `C_sin_evento_resultados.json`. No se agregaron esas etiquetas al ajuste existente.

Layout restaurado yguardado en12oct18:55–19:20,gráfico1m,Lite1m,CharacterChart,Replayapagado. Captura `manual/C_sin_evento_restaurado.png`.

## Consecuencia para el candidato

Conservar la base de estados, pero abandonar la regla deCconstante entre esos eventos. La siguiente propuesta debe especificar una salida numérica que pueda cambiar dentro de un mismo estado de pivotes,por ejemplo mediante edades o una estadística recursiva explícita; no basta agregar otra etiqueta.

Si usa edades, debe explicar87→84 sin evento y75→75en otro rango. Si usa un segmento fijo, debe respetar los contraejemplos de entradas locales idénticas conCdistintos. Se necesita definir una regla antes de medir otro episodio; no convertir estos dos valores en constantes de una tabla.
