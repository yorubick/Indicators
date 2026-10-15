# Modelos contrastados: evitar repeticiones, conservar el alcance

No se ha identificado Cgeneral. Un fracaso en una familia finita no refuta todas las funciones de volumen, memoria, pivotes, regresión o datos posteriores. Mesetas e integerC no demuestran una máquina de estados; que un cálculo pueda implementarse enPine tampoco lo convierte en el algoritmo original.

| Familia definida | Resultado / contraejemplo | Referencia reproducible |
|---|---|---|
|Continuación corta `max(dt,n*dt*10/183)` para rama larga|Funciona en34controlescortos; falla ya en21, que puede dar50,62,69,77,81 condt60.|C_DATASET_Y_FORMULAS.md; C_FRONTERA21_SMA20.md|
|Csolo por conteo, extremos o segunderoEND|Mismosn/H/L danCdistinto. Mismos segundosEND en19:20/21 no danelmismoC. No se excluyen funciones conjuntas con entradas adicionales.|C_VENTANAS_FIJAS_Y_MENOR_QUE_FUENTE.md; C_END_BARRIDO.md|
|Selección de pivotes/extremos que olvida el prefijo|Estado seleccionadoOHLCV idéntico puede dar88/61;44de52selectoresnuevos contradichos, cuatro sin eventos, dos selectores distintos de primercrucevolumen siguen abiertos pero sin mapeoCvalidado.|C_REINICIO_SUBRANGO.md; probar_C_selectores_pivotes.py|
|SeparabilidadSTART/END aditiva o multiplicativa|La misma vela final causa+21 o-6 dependiendoSTART. No descarta una función conjunta.|C_CRUCE1903.md|
|Kcomún por métricas de tendencia/ER|408variantes sinKfactible en entrenamiento, fuentes/transformaciones especificadas.|probar_C_tendencia_recorrido.py; C_tendencia_recorrido.json|
|Kcomún por22características de volumen/VWAP|66variantes cuantizadas1m sinKfactible;22características15s tampoco;44tras dosselectoresvolumen fallan.|probar_C_volumen.py; C_VOLUMEN_FRONTERA.md; C_REINICIO_SUBRANGO.md|
|Contactos/cruces/objetivosEND deEMA, semillasSMA y balances|Familias finitas fallaron. Respetar fuentes, semillas, intervalosN, objetivos y tolerancias de cada script; no exclusión general de lasEMA.|C_SEMILLA_SMA.md; C_BALANCE_RECORRIDO.md; probar_C_cruce_doble.py; probar_C_contacto_interior.py|
|Cmaximiza separaciónfinal deEMA72/89|30semillas/divisoresclose y30HL2:ningún9/9. Mezcla continuaλclose+(1-λ)HL2:ningúnλfactible para30configuraciones definidas.|C_MAX_SEPARACION.md; C_MAX_SEPARACION_HL2.md|
|Rugosidad exclusiva por extremos de dos mitades|Cuatrodescriptores colisionan: mismos extremos/n dan61y67. Cualquierfunción solo de esosdescriptores falla.|C_RUGOSIDAD_Y_MEDIA_ALPHA.md|
|Promedio aritmético dealpha local no negativo|L2..80, cincoescalas, C+/-1:395/395excluidos por cota, exigealphaextra negativo. No cubre estado recursivo ni otra agregación.|probar_C_media_alpha.py|
|Memoriaalpha basada enER con reglas fijadas|360recurrencias sinKcomún, incluso+/-1s. Pareja88/61 exige razón>1.40, modelos dan<=1.|C_MEMORIA_EFICIENCIA.md|
|Primera variaciónSMA20 definealpha yC21|32variantes,0/11entrenamiento21. No explica el umbral mediante ese ajuste concreto.|C_FRONTERA21_SMA20.md|
|Celige contacto en primera ruptura|108configuracionescurva/fuente/objetivo, ningúncontacto; todas excluidas inclusoC+/-1por cota derivativa.|C_CONTACTO_RUPTURA21.md|
|AR1/acf/espectro/selecciones de recorrido previamente ensayadas|Familias discretas especificadas, sinmodeloexactogeneral. No es prohibición de otros modelos de memoria o espectro.|C_MEMORIA_INTERNA.md; C_espectro.json; probar_C_estructura.py|
|ClasificadorGemini v4 como generador exacto|96/112 conocidos, pero3/9otros controles publicados. Sus literales y condiciones no son una fórmula descubierta.|GEMINI_V4_REVISION.md|

Reglas de trabajo: declarar inputs, resolución y manejo deSTART/END; usar la misma regla para todos loscasos; no seleccionar raíces/ventanas por cercanía alCconocido; mantener predicción separada deCobservado. Para Character-only puntuar contra el intervalo compatible, no tratar el integercompatible como una medición decimalLite. Los datos compartidos ya fueron conocidos: no llamarlos validación ciega o prospectiva.

Sigue abierto el origen deC: otra resolución/serie, estado anterior aSTART o datosEND→ruptura. Las curvas vacías antes de la ruptura impiden resolver el instante de cálculo con las salidas examinadas. El paquete aporta evidencia, no garantiza una ecuación fundamental única.
