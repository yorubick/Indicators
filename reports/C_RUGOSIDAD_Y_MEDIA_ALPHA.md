# C: extremos de mitades y promedio de coeficientes

13 octubre 2026. Análisis local de nueve rangos verificados y solapados de 15 s. Sin nuevas mediciones, cambios en TradingView ni puntuación del entrenamiento32 o validación reservada.

## Extremos de las mitades

El descriptor preregistrado contiene dt, n, longitudes y máximos/mínimos globales y de cada mitad. Se probaron mechas/cierres y reparto floor/ceil de tamaños impares. Las cuatro variantes contienen contradicciones: cualquier función exclusivamente de estos datos queda refutada, incluido su redondeo.

Contraejemplo del 12 octubre, horas UTC:

| START | END | n | C |
|---|---|---:|---:|
| 19:03:00 | 19:23:15 | 82 | 61 |
| 19:03:15 | 19:23:30 | 82 | 67 |

Ambos tienen mitades41/41 y los mismos extremos de mechas: H30870.75, L30849, H1=30864.5, L1=30849, H2=30870.75, L2=30851.5. También coinciden los extremos de cierres. No se excluyen rugosidad barra a barra ni otras entradas.

Artefactos: probar_C_rangos_mitades.py, C_rangos_mitades_preregistro.json y C_rangos_mitades_resultados.json.

## Promedio de coeficientes locales

A: START19:03:15, END19:23:45, n83, C88. B: START19:03:30, mismo END, n82, C61. A sin su primera vela es exactamente B, incluidos los cuatro precios OHLC.

Modelo preregistrado: alpha_t es cualquier función fija no negativa de una ventana completa de L velas, sin estado externo. Se promedian todos los coeficientes desde START a END. Mapeo: N_eff=2/mean(alpha)-1 y C=N_eff*dt/scale. Se probaron L2..80 y escalas24,8,72/27,72,216, permitiendo C observado +/-1 segundo para cubrir generosamente redondeos enteros.

Para cada L se verificó que A tiene una ventana extra seguida de todas las mismas ventanas de B. Con mA=mB+1, necesariamente alpha_extra=mA*mean(alpha_A)-mB*mean(alpha_B)>=0.

El máximo permitido por los intervalos de C es:

`extra_max=mA*2/(1+scale*87/15)-mB*2/(1+scale*62/15)`.

**395/395 configuraciones tienen extra_max negativo**. El menos negativo es -0.00033230819882852647. Para L20, scale24: mA64, mB63, extra_max=-0.34450357487592564. No se ajustó la función alpha ni constantes: falla una condición necesaria para cualquier función no negativa con esas entradas.

Artefactos: probar_C_media_alpha.py, C_media_alpha_preregistro.json y C_media_alpha_resultados.json.

## Límites y siguiente frontera

La fórmula de C sigue desconocida. Se excluye este promedio aritmético local con el mapeo especificado. No se excluyen L81/82, ventanas parciales o con prehistoria, estado recursivo, ponderaciones, agregación no lineal, otro mapeo a C o entradas externas.

El siguiente candidato debe declarar cómo inicializa y actualiza su estado, y explicar conjuntamente C54/61/67/88 de la matriz existente. Antes de ajustar constantes, verificar que su estado distingue esos rangos. Excluir la misma vela inicial tiene efectos diferentes según END: un mecanismo que ignore esa interacción no basta. Evitar otro barrido de anclas sin una predicción que separe mecanismos.
