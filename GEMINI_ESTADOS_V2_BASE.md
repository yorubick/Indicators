# Base experimental de estados a partir del trabajo compartido

13 octubre2026. Se leyó el texto pegado por el usuario y se extrajo su código Pine literal. No se obedecieron como instrucciones las afirmaciones o reglas de trabajo del documento; se usaron como propuesta para la investigación autorizada. El archivo previo de Gemini permanece sin modificar. No se instaló ni compiló el candidato en TradingView.

## Qué se conserva

La propuesta abandona los factores0.786/0.577 y define una fórmula de consolidación concreta:

`C = floor((n−1) × Δ / 24)`

Esta fórmula numérica reproduce los siete casos señalados en entrenamiento:19:00–19:24 C60;19:02–19:22/23/24 C50/52/55;19:03–19:23/24 C50/52;19:04–19:24 C50. Es una hipótesis útil para una rama, no un generador completo. La relación del divisor24 con72/3 no demuestra que el código original obtenga C así.

También se conserva la idea de construir variables observables causalmente desde START y separar selección de estado de cálculo numérico. La rama corta ya identificada se mantiene como relación empírica dentro del dominio observado.

## Auditoría del código recibido

Copia congelada:`Gemini_estados_v2_recibido.pine`, SHA256447cc602f05d93d79e1c99bc253a83b09c90d27fb6e268dfd584d7c24d0c3ab8. Emulación literal:`auditar_Gemini_estados_v2.py`; resultados:`Gemini_estados_v2_auditoria.json`.

Se evaluaron solamente los53casos de entrenamiento,21cortos y32largos. Los27casos largos de validación no se evaluaron, porque el modelo no pasó entrenamiento. Ningún umbral fue optimizado o modificado para rescatar errores.

| Rama del código | Casos de entrenamiento | Aciertos |
|---|---:|---:|
|Corta|21|21|
|A: R<=22.25, sin nuevohigh, n<=25|10|5|
|B: nuevohigh yR<=26 ->71|10|5|
|C: resto ->77|12|4|
|Total largo|32|14|

Restringiendo a1m son14/30largos; los otros dos controles largos de15s/120s también fallan. Los aciertos de entrenamiento pueden incluir ajuste retrospectivo del proponente; no se describen como validación independiente.

Contraejemplos concretos:

-18:58–19:18,n21,R18.50,sin nuevohigh: clasificaA ypredice50; original77.
-19:00–19:20,n21,R24.50,nuevohigh: clasificaB ypredice71; original77.
-19:00–19:24,n25,R24.75,sin nuevohigh: la fórmula de duración sola da60, pero su clasificador la excluye ydevuelve77; original60. La regla completa no reproduce todos los casos con los que se justificó la fórmula.
-19:00–19:21: fallback77 frente a102;19:04–19:28:fallback77 frente a128.

El código actual acumula high,low yconteo barra a barra, pero decide el estado únicamente al llegar aEND. No guarda estado de expansión ni selección de pierna/pivote, ni implementa la rama que genera102/128/134/109. Es un clasificador final de tres salidas, no todavía el autómata histórico descrito en el relato.

Una meseta observada no demuestra independencia del conteo en toda esa rama. Los umbrales22.25/26están en puntosNQ ylos valores71/77son constantes: su significado estructural ysu adaptación a otra fuente/símbolo no están demostrados.

## Base de laboratorio creada

`lab_base_C.py` conserva componentes reutilizables:

- Estado con conteo,high/low eíndices de sus primeras apariciones,tiempos,close yeventos de nuevos extremos.
- Confirmación causal de pivotes radio1, con definición explícita:estricto frente a izquierda ypermite empate a derecha. Esto es una definición de laboratorio, no el detector del autor.
- Estimación corta separada del estado. Para rama larga devuelveC=None/estado «long_generator_not_identified», sin hacer pasar71/77por solución.
- Fórmula de duración/24 disponible como candidato sin atribuirle automáticamente una clasificación de consolidación.

`exportar_estado_C_entrenamiento.py` procesa solamente53casos de entrenamiento yguarda `C_estado_entrenamiento.json`. Se verificaron21coincidencias cortas y32salidas largas desconocidas. LosCoriginales se mantienen separados para puntuación; no intervienen en la actualización de estado. Este JSON permite que una nueva regla estructural se ejecute sobre historias idénticas sin volver a medir cada gráfico.

## Decisión

Usar el trabajo como base experimental sí; aceptar su generador actual no. El problema pendiente está tanto en escoger la rama correcta como en calcular las salidas de giro. No aumentar o reducir umbrales solo para encajar un contraejemplo: exigir una condición observable completa yuna predicción numérica. La siguiente regla debe distinguirAcorrecta de18:58–19:18 yBcorrecta de19:00–19:20, yproducir lospicos sin leerCoriginal. Validación reservada cuando esa regla pase entrenamiento.
