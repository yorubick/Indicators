# Ventanas fijas: C puede ser inferior a la fuente

13 de octubre de2026. NQ1!, ETH, UTC, BADJ apagado; anclas12 de octubre. Gráfico/fuente1m, Lite v1.2 fuente explícita1m; Character v6.5.36 perfilB Manual fuenteChart. Seis nuevos controles completos, curvas repetidas exactamente y ajuste independiente de seis curvas Lite.

## Conteo constante

| START | END | Velas | C Lite y Character |
|---|---|---:|---:|
| 19:00, anterior | 19:20 | 21 | 77 |
| 19:01 | 19:21 | 21 | 77 |
| 19:02 | 19:22 | 21 | 50 |
| 19:03 | 19:23 | 21 | 50 |
| 19:04 | 19:24 | 21 | 50 |

El conteo21 no determina C. Las tres últimas ventanas comparten máximos30870.75 y mínimos30849.00, pero eso no prueba que sus extremos determinen50: los casos siguientes proporcionan un contraste más estricto.

## Transición corta/larga con START fijo

| START | END | Velas | C |
|---|---|---:|---:|
| 19:02 | 19:21 | 20 | 65.57377049 |
| 19:02 | 19:22 | 21 | 50 |

La ventana20 reproduce la relación corta. Añadir una vela lleva C por debajo de la fuente60s. El máximo cambia0.25 puntos (30870.50→30870.75), el mínimo sigue30849.00 y el cierre final sigue30868.50.

**Se refuta el supuesto global C>=Δ.** El max(Δ,...) pertenece a la relación corta comprobada; no debe imponerse como límite universal al generador general. C=50 se observa en Lite y es el único entero compatible con las diez curvas Character. La fuente de actualización sigue siendo60s, con períodos Lite decimales convencionales; C es el parámetro normalizado de la familia, no el intervalo de actualización de las EMA.

Esto exige corregir la clasificación de datos para próximas búsquedas: C<Δ no es un caso saturado, inválido ni motivo para excluirlo. Las búsquedas antiguas con max(Δ,...) describían una familia hipotética, que ahora no puede ser universal.

## Un control de END y extremos fijos

| START | END | Velas | Máximo global | Mínimo global | C |
|---|---|---:|---:|---:|---:|
| 19:01 | 19:22 | 22 | 30870.75 | 30849.00 | 77 |
| 19:02 | 19:22 | 21 | 30870.75 | 30849.00 | 50 |

Las21 velas finales son idénticas registro por registro. La diferencia es incluir la vela19:01 al principio: O30852.75,H30863.50,L30852.00,C30859.25. Esa vela no establece un extremo global nuevo. Al excluirla cambia C77→50, conservando END, sus OHLC, los extremos y todo el tramo final.

Por tanto, C no depende únicamente del OHLC de las últimas21 velas ni de esas velas más los extremos globales y END. Sigue abierto que use el conteo total, duración, inicialización desde START o estadísticas del recorrido completo. La diferencia de conteo22/21 no se separa aquí del efecto de la vela excluida.

La comparación adicional de19:00–19:22 (23 velas,C77) con19:02–19:22 (21,C50) también conserva exactamente las21 últimas velas, aunque cambia el mínimo global; se registra en el JSON.

## Auditoría y archivos

Todas las parejas a/b nuevas tienen16 curvas cerradas comunes idénticas y OHLC completos. La dispersión de los seis C Lite es inferior a1e-8 segundos. En los casos C50, el intervalo Character es [50,50.13888889). El promedio ajustado de Lite queda unas1e-13 unidades por debajo de50 por error numérico; se usa tolerancia explícita1e-8 al comparar con extremos del intervalo. No se considera una diferencia real entre indicadores ni se modifica la extracción original.

Analizador: analizar_C_ventanas_fijas.py. Datos completos: C_ventanas_fijas.json. CSV manual/Lite_1901_192100_1m_[a/b].csv, Lite_1902_192200_1m, Lite_1903_192300_1m, Lite_1904_192400_1m, Lite_1902_192100_1m y Lite_1901_192200_1m.

Capturas: C_ventana21_*_anclas.jpg; C_vecinas_20_1902_1921_anclas.jpg; C_endfijo_1901_1922_anclas.jpg. Referencia18:55–19:20 restaurada y guardada; C_ventanas_fijas_referencia_final.jpg.

## Siguiente contraste

Desplazar ventanas de22 y23 velas alrededor de este mismo tramo, registrando predicciones de hipótesis específicas antes de medir. Se busca distinguir estado inicial de selección de estructura y conteo global, sin volver a imponer un mínimo igual a la fuente ni escoger un pivote retrospectivamente por su cercanía al C observado. El generador general sigue pendiente.
