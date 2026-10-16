# C: recurrencia de eficiencia con memoria

13 octubre 2026. Prueba exploratoria local: nueve controles conocidos y solapados, separados del dataset maestro. Reglas guardadas antes de ejecutar. No es validación ciega. Sin nuevas mediciones ni cambios en TradingView.

## Modelo definido

Fuente close o HL2; eficiencia ER=desplazamiento absoluto/recorrido absoluto en las últimas L variaciones disponibles, o todas desde START. Si recorrido=0, ER=0. L=3,9,20,27 o creciente.

`target_t = (2/31 + (2/3 - 2/31)*ER_t)^p`, con p=1 o2.

Inicialización en la primera variación: coeficiente lento, rápido o primer target. Actualizaciones siguientes:

`alpha_t = alpha_previous + 2/(M+1)*(target_t-alpha_previous)`

M=1,3,9,20,27,81. La recurrencia permanece entre sus límites lento/rápido; el programa comprueba este invariante. Con M1 también comprueba alpha final=target final. No incluye historia anterior a START.

Mapeo sometido a prueba: `C=K*dt*(2/alpha_END-1)`, con un único K positivo para todos los casos. Se intersectaron los intervalos de K compatibles con cada C observado +/-1 segundo. También se puntuaron cinco escalas fijas, redondeando al entero más cercano. Ningún parámetro por caso ni excepciones de precio/hora.

## Resultado

- 360 recurrencias: **0 intervalos comunes de K factibles**.
- Escalas fijas 24,8,72/27,72,216: máximo **2/9 aciertos**, sin candidato suficiente.
- No se usaron entrenamiento32 ni validación reservada para rescatar el modelo.

La pareja END19:23:45 UTC del 12 octubre ya basta para refutar las 360 variantes:

| START | Velas | C observado |
|---|---:|---:|
| 19:03:15 | 83 | 88 |
| 19:03:30 | 82 | 61 |

El segundo rango es el primero sin su primera vela. La razón de períodos del modelo entre ambos está entre **0.8131991885483306 y1.0**. La razón exigida por los C, incluso con +/-1 segundo, está entre **1.403225806451613 y1.4833333333333334**. Los intervalos no se cruzan. La escala común K se cancela en esta comparación.

En esta familia retirar la primera vela mantiene o aumenta el período. En el indicador, retirar esa vela lo reduce de88 a61. Por tanto el fallo no se corrige con una escala diferente.

## Alcance y próxima condición necesaria

Esta prueba no excluye toda memoria recursiva, ni todos los coeficientes basados en eficiencia. Excluye las fuentes, ventanas, semillas, constantes, exponentes, recurrencias y mapeo especificados. Otros umbrales, estados, fuentes y prehistoria siguen abiertos. No identifica un pivote causal ni demuestra que el original sea una máquina de estados.

El siguiente candidato debe poder invertir la dirección del cambio de esta pareja y distinguir la interacción START/END de la matriz. Antes de nuevos barridos conviene declarar una regla de selección de subrango o reinicialización y comprobar qué estado concreto cambia al excluir la vela19:03:15; no basta añadir constantes a esta recurrencia. No existe todavía una regla específica validada para esa selección.

Reproducción: ejecutar probar_C_memoria_eficiencia.py --spec y después el mismo script sin argumentos. Artefactos: C_memoria_eficiencia_preregistro.json y C_memoria_eficiencia_resultados.json. La fórmula generadora de C sigue pendiente.
