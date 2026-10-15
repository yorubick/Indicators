# Comparación de anclas estructurales: 1 minuto y 15 segundos

Fecha de auditoría: 14 de octubre de 2026. Instrumento NQ1!, ventanas del 12 de octubre, UTC. Indicador PS EMA LITE v1.2. Las mediciones del indicador Character no intervienen.

## Resultado

Se completaron las 20 ventanas registradas, con dos exportaciones aceptadas por ventana. Se conservó la cobertura de cada minuto: START en :00 y END en :45 de su minuto final. Se cambiaron conjuntamente la resolución del gráfico y la fuente a 15 segundos.

| Ancla propuesta | START | Minuto de END | C con fuente 1m | C con fuente 15s |
|---|---|---|---:|---:|
| Primer mínimo local posterior a la recuperación | 18:52 | 19:07 | 60 | 38 |
| Mínimo más profundo de la mitigación posterior | 18:52 | 19:10 | 62.295081967 | 45 |
| Último mínimo local antes de la nueva expansión | 18:52 | 19:17 | 62 | 106 |
| Pausa previa al origen, proxy provisional de failure swing | 18:47 | 18:52 | 60 | 16 |

Los eventos se habían identificado sobre precios de un minuto; no se redefine retrospectivamente su ubicación sobre las subvelas. La denominación failure swing sigue siendo provisional.

Para la última mitigación, C15 fue 106 en la ventana base; mover START un minuto hacia atrás o adelante dio 66 en ambos casos. Mover END un minuto atrás dio 66 y un minuto adelante dio 152. El mínimo local de C que aparecía en la base de un minuto no se conserva en esta comparación.

## Verificación

- Las cuatro subvelas de 15 segundos reproducen exactamente apertura, máximo, mínimo, cierre y volumen de cada vela original de un minuto, dentro de cada ventana y durante la hora posterior.
- Las seis curvas recuperan el mismo C dentro de la tolerancia y se reconstruyen desde END:45 con el extremo de la subvela final como semilla. Error máximo de reconstrucción: 1.565e-10; ninguna discrepancia de visibilidad.
- Los máximos y mínimos de las cajas coinciden con los de las ventanas originales.
- Las dos ventanas B con n15=20 cumplen la regla corta conocida: C=16.393442623. Las ventanas B con n15=24 o 28 dan C=16.
- Se restauró gráfico y fuente a un minuto, START 18:55 y END 19:20. Las seis curvas recuperan C=62 y coinciden con la referencia en 2,993 velas cerradas comunes. La captura final verifica visualmente intervalo y anclas.

## Incidencia conservada

El primer par de A_first_start_plus fue discrepante: a dio 53 y b dio 68. No se promediaron ni sobrescribieron esos archivos. Se registró una repetición y se exportaron c/d después de volver a configurar la ventana: ambos dan 68 y d coincide exactamente con el antiguo b en 11,841 velas cerradas comunes. Una recarga pendiente es una explicación posible del antiguo a; la causa no está demostrada. El JSON conserva los valores, comparaciones y hashes de ambos pares.

## Qué permite concluir

En estas ventanas, la misma cobertura temporal y los mismos OHLCV agregados de un minuto no determinan un C independiente de la resolución. C=62 tampoco sirve como firma universal de que una caja estructural sea correcta. Valores como 38, 53, 65 y 106 refutan una cuadrícula exclusiva de múltiplos de 3 o de 9 para estas salidas.

La comparación no identifica el mecanismo de C. Cambian simultáneamente el número de velas, la secuencia de cierres intraminuto, la rama corta/larga en algunas ventanas y la semilla final. No demuestra ni excluye una transformación armónica más general, ni establece un ancla oculta anterior a START. Todavía no tenemos una regla que permita predecir C en un caso nuevo.

La auditoría previa de un minuto detectó una revisión de volumen a las 22:00 (547 a 548) fuera de las ventanas y sus horizontes de verificación. No se afirma igualdad global con aquella descarga anterior. La restauración actual usa la referencia reciente y las agregaciones de esta prueba sí coinciden en todo su ámbito registrado.

## Siguiente experimento propuesto

Mantener gráfico y fuente en 15 segundos, fijar START=18:52:00 y medir END cada 15 segundos desde 19:16:45 hasta 19:18:45, nueve posiciones incluidas. Registrar el barrido antes de medir y repetir cada exportación. Este intervalo conecta los controles ya medidos C=66, 106 y 152 sin cambiar de resolución. Permitirá localizar si los saltos ocurren al incorporar una subvela concreta o si forman una evolución gradual. No se usará un único salto como prueba suficiente de armonía.

## Archivos

- Protocolo: C_ESTRUCTURA_15S_PREREGISTRO.json.
- Repetición registrada: C_ESTRUCTURA15_REPETICION_A_FIRST_START_PLUS.json.
- Resultados completos y hashes: C_estructura15_resultados.json.
- Auditor reproducible: auditar_C_estructura15.py.
- Exportaciones y capturas: manual/C_estructura15_*.
- Restauración: manual/C_estructura15_regreso_1m_final.csv y manual/C_estructura15_final.png.
