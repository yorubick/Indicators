# Auditoría del modelo unificado Gemini v3.1

13oct2026. Se leyeron los archivos entregados en el scratch de Gemini y se congelaron copias en `Gemini_v31_evaluador_recibido.py` y `Gemini_v31_recibido.pine`, sin modificar los originales. SHA256 y resultados completos en `Gemini_v31_auditoria.json`. Reproducción: `auditar_Gemini_v31.py`. No se ejecutó el código superior del evaluador: se extrajo únicamente su funciónpredict_C mediante AST y se la evaluó sin ajustar parámetros.

## Resultado cuantitativo reproducible

|Subconjunto|Exactos, tolerancia1e-7|Casos|MAE segundos|
|---|---:|---:|---:|
|Entrenamiento original, cortos+largos|51|53|0.1321|
|Entrenamiento original, solo largos|30|32|0.2188|
|Validación original, cortos+largos|30|40|1.4000|
|Validación original, solo largos|17|27|2.0741|
|Seis controles ya publicados13oct|4|6|0.6667|
|Total original del informe|85|99|0.6768|
|Controles adicionales de esta investigación|0|13|47.2308|
|De esos adicionales, fuente/gráfico15s|0|11|53.7273|

Los13adicionales son las dos ventanas de réplica24 en1m y los once controles nativos15s de resolución, transiciónEND, prefijo y recorteSTART. No se deduplicaron por C: distintas selecciones temporales son distintos controles. No son13episodios independientes. Ya estaban medidos y disponibles localmente cuando se recibió el modelo: no se certifica que Gemini no los hubiera visto. Su fallo sí prueba incompatibilidad con esos controles verificados.

Los porcentajes85/99,92/99dentro3s y93/99dentro5s se reproducen. El evaluador permite llamar"exacto" a resultados que solo redondean al mismo entero y redondea errores antes de calcular MAE. En estos99casos, usar tolerancia estricta1e-7 conserva los85aciertos: ese detalle no infla el resultado concreto reproducido.

Para auditar las afirmaciones del modelo externo se puntuó explícitamente su particiónvalidation, sin usarla para entrenar ni cambiar reglas. No debe presentarse esta auditoría como una evaluación ciega. El reporte de Gemini afirma que los seis controles13oct son ciegos/prospectivos, pero el código los lee de resultados ya publicados y contiene una rama identificada en su comentario con ese episodio. No se aportó un preregistro fechado anterior a la medición para respaldar independencia prospectiva. Evaluar después de observar resultados no equivale a una predicción previa.

## Por qué no identifica el generador

1. La rama larga15s devuelve16incondicionalmente. Los once controles adicionales requierenC61,67,79u88; todos fallan. La rama120s también es una constante137, no una regla de escalado demostrada.
2. Python contiene una excepción `n == 25 and rng <= 24.75 and max(highs) == 30870.75` que devuelve60. Un precio absoluto específico del episodio no justifica una regla general de consolidación.
3. Los picos128/134/109,83/76,102y93 se asignan como literales mediante umbrales de rango/conteo. Es una función determinista reproducible, pero no demuestra que esas reglas pertenezcan al indicador original. No implementa un detector completo de SFP ni una recurrencia de estados de swing.
4. La supuesta cuantizaciónh=0.05*dt aparece en comentarios/informe; no se utiliza como operación de cuantización en el motor. Además, el propio motor devuelve82como base macro, fuera de3Zy3Z−1. Las dos redes no explican todos los valores macro ni establecen un algoritmo.
5. Duración/24 continúa siendo una regularidad de ventanas solapadas de un episodio. La auditoría previa encontró un intervalo de divisores compatibles(23.77358490566038,24], no identificación matemática exclusiva de24. Los controles de cobertura equivalente15s producen67y88frente50en1m. Añadir un selector ajustado a ejemplos conocidos no prueba causalmente el divisor.

Los aciertos de1m justifican conservar el modelo como aproximación congelada para comparación, no llamarlo fórmula descifrada. La regla corta es la ya verificada34/34, no un nuevo descubrimiento independiente de esta entrega. Incluir esos34casos en el85.9%global oculta parte de la dificultad específica de la rama larga.

## Python y Pine no son el mismo modelo

Se emularon las condiciones del generador Pine, sin compilarlo ni instalarlo. En los99originales hay dos predicciones diferentes:

|Rango1mUTC12oct|Original|Python|Pine|
|---|---:|---:|---:|
|15:28–15:52|81|75|93|
|19:00–19:24|60|60|77|

Entre las discrepancias de código: Python usa precio máximo absoluto30870.75dondePine usa highEND==rng_high; Python exige distancias a extremos para ciertos picos, Pine omite esas condiciones. Por tanto, los porcentajes del evaluadorPython no validan automáticamente el Pine entregado.

## Reconstrucción de curvas incompleta/incorrecta

- `show_ct` se declara, pero no controla ningún trazado de Character. Solo se calculan seis períodos redondeados; no hay diez curvas Character ni las dos nubes extra anunciadas.
- `calc_ema` inicializa todas las EMAs con closeEND y las publica desdeEND. Nuestra reconstrucción verificada usa lowENDpara la rama alcista/highENDpara la bajista, actualiza después deEND y publica a partir de la ruptura por cierre del rango inclusivo. El Pine no implementa esas semillas y esa puerta de publicación.
- No tiene la doble rama causal verificada ni la selección de fuente propia del indicador comprado; utiliza velas del gráfico. No se ha compilado ni probado visualmente este archivo enTradingView; no hay base para llamarlo reconstrucción exacta completa.

## Decisión

Conservar la entrega como referencia auditable, sin reemplazar el laboratorio causal ni cambiar la dirección de la investigación por sus porcentajes. La prioridad continúa siendo el cruce START:15/:30conEND19:23:30 frenteEND19:23:45, para contrastar una regla local explícita sobre la interacción de ambos límites. Antes de medir, fijar sus predicciones y conservar fallos. C sigue sin fórmula general identificada.
