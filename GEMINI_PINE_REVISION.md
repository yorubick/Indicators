# Revisión del Pine de laboratorio compartido

13 de octubre de 2026. Se leyó el archivo C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch/PoiSzn_C_Detector_Lab.pine. No se modificó ni se instaló en TradingView. La comprobación numérica emula su recurrencia en Python; no constituye compilación ni ejecución del Pine.

## Hallazgos del código

1. Líneas51–55: f_structural_audit devuelve66.0 fijo. Calcula rng pero no usa ese valor ni n/dt para determinar C. El modo «Automatico (Modo Diagnostico)» no implementa una regla de swings ni un generador.
2. Líneas100–103: la primera vela activa devuelve la semilla sin procesar su cierre. La reconstrucción validada procesa ese primer cierre posterior a END. El error puede quedar oculto si el primer cierre coincide con la semilla, como en el control C118 de15s.
3. Líneas106–108: siempre usa low de END. La semilla high está almacenada pero nunca seleccionada para las curvas; falla en casos bajistas.
4. Líneas111–123: publica las seis curvas desde la primera vela posterior a END; no contiene selección de dirección ni condición de cierre exterior al rango. Nuestra regla comprobada actualiza antes de ruptura y publica desde ella.
5. Línea10 y líneas111–116: res_sec cambia los períodos pero las recurrencias reciben close del gráfico. No hay adquisición o agregación de una fuente distinta. Para esta comparación debe coincidir con la resolución del gráfico; elegir15 en gráfico1m no procesa velas15s.
6. Líneas81–90: calcula diez períodos Character para la tabla, pero no calcula ni dibuja sus diez curvas. show_ct no se usa en esas operaciones ni en los plots. Solo hay seis llamadas plot, correspondientes a Lite.
7. Línea24: la alternativa time<=end_time && time[1]<end_time && time>end_time es contradictoria, así que is_end_bar solo puede activarse por time==end_time. Si END no coincide con una apertura del gráfico, no fija la semilla ni aplica C manual.
8. La tabla informa amplitud, conteo y períodos; no calcula distancias a pivotes. La afirmación de métricas de pivotes no corresponde a esta versión del archivo.

Las bases72/89 y divisores3/9/27 de los períodos sí coinciden con la familia que identificamos. Una familia de períodos correcta no basta para garantizar curvas idénticas.

## Contraejemplos numéricos del modo manual

Se proporcionó el C correcto, se igualó res_sec al intervalo del CSV y se usaron anclas exactas. Se emuló el estado del código: low de END, semilla sin primera actualización, luego EMA(close). Comparación de las seis curvas durante90 minutos posteriores a END, solo en timestamps donde el indicador original tiene valores:

| Caso | C manual correcto | Error máximo visible, puntos | Plots publicados prematuramente por el laboratorio |
|---|---:|---:|---:|
| 18:55–19:20, fuente1m | 62 | 0.2671669 | 30 celdas |
| 18:54:15–19:20, fuente15s | 118 | 9.45874e-11 | 12 celdas |
| 04:45–05:30, fuente1m, bajista | 110 | 7.6038907 | 30 celdas |

El caso C118 coincide numéricamente en las partes visibles porque el primer cierre posterior a END equivale a su low. Eso no valida la recurrencia para cualquier C/rango y no arregla la publicación prematura. Los otros dos casos refutan la afirmación de exactitud universal del modo manual.

Reproducción: auditar_lab_Gemini.py. Datos y errores por curva: Gemini_lab_auditoria.json.

## Interpretación de swings y de la guía

La secuencia de END19:20→19:22 se midió cambiando el extremo de selección en modo Manual. No observamos un C que se reinicie espontáneamente mientras las anclas permanecen fijas. Describir C115 como «reinicio de nuevo setup» requiere una prueba específica; el nuevo máximo y los posteriores cambios son observaciones, no una regla para calcular115/106/79/66.

La frase citada aparece en la transcripción automática de **Auto Zoom**, aproximadamente8:32–8:53: habla del anclaje de EMA desde failure swing hasta el final de OLR y de formar otro árbol al aparecer un setup nuevo. Da una pista sobre selección de rangos de ese producto, sin definir la transformación del rango a C. No aparece como tal en la transcripción de Character Tree. Se debe confirmar en el audio antes de atribuir exactitud textual a una transcripción automática.

Las tablas refutan una regla dependiente solo del segundo dentro del minuto. No refutan toda función de tiempo que también reciba duración, fecha, sesión o minuto.

## Consecuencia para la investigación

El Pine sirve de borrador de visualización, pero esta versión no es una réplica validada ni incorpora un generador de C. Antes de usarlo como instrumento de medición, corregir actualización inicial, dirección, visibilidad, fuente efectiva, END y curvas Character. Esas correcciones reconstruyen salidas con C suministrado; no resuelven C.

La hipótesis de selección de swing sigue abierta. Para hacerla comprobable hay que definir cómo selecciona pivotes, qué ventana exacta procesa y qué operación obtiene C, con predicciones previas sobre las tablas completas. No tomar un relato de ruptura/retest como prueba de una fórmula numérica.
