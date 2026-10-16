# Revisión actualizada del laboratorio Gemini y dos controles nuevos de C

13 octubre 2026. El archivo compartido cambió respecto al revisado en `GEMINI_PINE_REVISION.md`. Se leyó otra vez la versión actual, sin modificar el original ni instalarlo en TradingView. Copia exacta: `Gemini_hibrido_auditado.pine`; SHA256 bd4fd5694982867eefbc5bb7b6b6abf3a93cbe2578e75dba392d60709ff5138f.

## Lo que ahora sí aporta

El nuevo código calcula seis curvas Lite y diez Character, actualiza las ramas alcista y bajista desde la primera vela posterior a END, siembra respectivamente en low/high de END y publica desde el primer cierre estrictamente exterior al rango. Corrige las principales limitaciones de la versión anterior.

Emulando esas operaciones con C original suministrado, fuente y gráfico1m y anclas exactas, las18ventanas recientes reproducen39,664 valores originales durante180minutos posteriores a END. Error máximo Lite4.01e-11 puntos, Character3.64e-11 y cero discrepancias de visibilidad. Todas tienen muestras visibles (mínimo534 valores Lite por caso). Se amplió el horizonte inicial90min a180min porque dos casos aún no habían publicado dentro de90min; no se contaron como validaciones numéricas sin muestras.

Esto valida la emulación numérica del motor en esos controles; **no constituye compilación ni ejecución del Pine en TradingView**, ni equivalencia universal con todos los modos del original. Puede servir para visualizar curvas con C conocido y comparar candidatos.

## Generador automático: separar sus dos ramas

Líneas76–78 de la copia: reproduce la regla corta observada C=max(dt,n*dt*10/183) para n<21. En los dos conjuntos históricos auditados y nuevos controles hay7casos cortos,7coincidencias. Esto reutiliza una relación ya medida, no descubre la rama larga.

Líneas80–108: la rama larga usa ticks del rango, posición del open de START, nuevos extremos y confirmación del high anterior. Aplica factores0.786/0.577, sumas de conteo y pasos2. El propio código la llama «Modelo Heurístico Experimental». Es una fórmula concreta que puede refutarse.

Se emuló exactamente esa rama en35casos de21velas o más: coincide en4 y falla en31. En las12ventanas largas recientes (10de la tanda de fronteras/desplazamientos y2nuevas) falla en las12. Las4coincidencias pertenecen a rangos anteriores:19:00–19:20 C77,19:03–19:24 C52,19:04–19:24 C50 y19:04–19:28 C128. No se sabe qué datos usó Gemini para construir sus factores; esos aciertos no se describen como validación independiente.

| Ventana12oct,21velas | C original | C automático Gemini |
|---|---:|---:|
|06:00–06:20|77|114|
|14:00–14:20|62|248|
|15:30–15:50, nuevo control alcista|69|276|
|07:00–07:20, nuevo control lateral|75|87|

En las dos últimas ventanas, las predicciones276y87 se registraron antes de medir C. No se cambiaron factores tras observar resultados. En modo automático, el error visible Lite llega a27.10puntos en el nuevo control alcista y3.93puntos en el lateral durante el contraste inicial90min; el JSON final conserva la emulación180min por separado.

## Selección de los nuevos controles

Se usó exclusivamente OHLC del CSV ya descargado. Candidatos: ventanas inclusivas21velas que empiezan a horas enteras o medias horas entre07:00y18:30 del12oct, excluyendo14:00/14:30. Control alcista: máximo ER entre cambios de cierre positivos. Control lateral: mínimo ER con amplitud>=10puntos. ER=abs(cierre final-cierre inicial)/suma de cambios absolutos de cierre. No se consultó C para elegir ventanas.

- 15:30–15:50: avance neto63.25puntos, ER0.565996, amplitud87.75; C69.
- 07:00–07:20: cambio neto2puntos, ER0.0187793, amplitud37.50; C75.

«Alcista» y «lateral» describen estos criterios, no categorías perfectas. Son ventanas de una misma jornada, sin solapamiento entre sí. Ambas pasan cobertura21OHLC, estabilidad exacta de16curvas en parejas c/d, seis estimaciones Lite concordantes e inclusión de C en el intervalo Character. Cada pareja compara39,856celdas de curvas. Los pending se conservaron.

Junto a las ventanas bajistas06:00(C77)y14:00(C62), tenemos ahora valores distintos en cuatro rangos del mismo conteo y resolución. Esto sigue sin determinar el generador: dirección o una categoría de estructura no basta como fórmula.

## Limitaciones adicionales del Pine

La fuente efectiva es el gráfico: no obtiene otra resolución nativa. END solo se inicializa si time==end_time (línea40); START exacto fija start_open (línea49). Anclas sin coincidencia exacta, cobertura insuficiente o intervalos distintos requieren manejo adicional y no están validados. dt usa segundos/minutos y devuelve60 en los demás intervalos (línea71): no usarlo como laboratorio de días/semanas. El fallback nz(c_auto,c_manual),línea110, puede mostrar un C manual cuando el automático no está disponible; debe identificarse como fallback, no medición automática exitosa.

## Archivos y continuación

Auditoría: `auditar_Gemini_hibrido.py`, `Gemini_hibrido_auditoria.json`. Nuevas mediciones: `C_21_seleccion_regimenes.json`, `analizar_C_21_regimenes.py`, `C_21_regimenes.json` y `manual/C_21_alcista/lateral_*`. El informe anterior se conserva como auditoría de otra versión.

La utilidad comprobada es el motor con C suministrado y la rama corta en el dominio probado. La rama larga actual no debe usarse como origen recuperado de C. Próximo contraste: barrer START con END fijo en los nuevos controles69y75 para observar puntos de cambio y comprobar si una regla candidata debe usar toda la ventana o un segmento seleccionado. Registrar predicciones numéricas antes de probar otros rangos.

Layout restaurado y guardado en referencia12oct18:55–19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado. Captura `manual/C_Gemini_regimenes_restaurado.png`.
