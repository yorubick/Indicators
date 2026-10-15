# Etiquetas del indicador oficial

Revisión visual14oct2026 deCharacter Tree v6.5.36, perfilB Manual, NQ1!ETH,UTC,BADJoff. No se actualizó el script. Rango12oct18:55–19:20, fuente/gráfico1m. Se activó temporalmenteShowPDarrays y se mantuvoShowrange. Las dosopciones se revisaron en la interfaz, sin leer código protegido.

- **Show range:** representación del rango y sus anclas/precios. No se observó una tablaC ni métricas de su fórmula impresas dentro del rango.
- **Show PD arrays:** zonas con etiquetas **FVG, IFVG yVI**, visibles incluso antes de la ruptura en el corteReplay19:25. No se encontró unvalorCdecimal o una estadística intermedia que pudiera identificar su generador a partir de esas etiquetas.
- **Show EMA timeframe labels** es una opción distinta, ya activada en la configuración original. Después de avanzarReplay hasta la aparición de lascurvas se leen **C/27 2.3s [TV5s]**, **C/9 6.89s [SYN7s]**, **C/3 20.67s [TV30s]**. Son segundos de la familia ya derivada deC62; redondeados, no ecuación ni inputs internos del generador.
- También aparecen STARTBULL, AUTOBULL yBREAKUP: etiquetas de dirección/ruptura, no una medición adicional deC.

Las etiquetas de temporalidades se sitúan sobre losvaloresEMA; en el control anterior a ruptura no aparecieron porque no habíaEMApublicada. No resuelve siCinternamente ya está calculado enEND. No demuestra que ninguna otra configuración o versión pueda ofrecer otras salidas.

Evidencia: manual/C_pack_PD_prebreak.png ymanual/C_pack_PD_postbreak.png. Para leer losobjetos se activó temporalmenteScalepricechartonly; después se desactivó. Al finalizar: ShowPDarraysoff, Showrangetrue, Litevisible, gráfico1m, fuenteLite1m/CharacterChart, anclasoriginales, preciosauxiliares originales, Replayoff. Configuraciónregistrada enmanual/C_pack_restauracion_config.txt; captura finalmanual/C_pack_restaurado.png.
