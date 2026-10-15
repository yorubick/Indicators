# Reflexión 70000−P: C permanece en 50

14 octubre 2026, prueba real en copia xqM5dZIf. Lite v1.2, fuente/gráfico 1 minuto, START 12 octubre 19:02 UTC y END 19:22 UTC (21 velas). Character excluido. Protocolo declarado antes de medir en C_REFLEXION_50_PREREGISTRO.json.

| Condición | C en seis curvas | Dirección de primera ruptura |
|---|---:|---|
| NQ1! | 50 | Alcista |
| 70000−NQ1! | 50 | Bajista |
| Regreso NQ1! | 50 | Alcista |

La expresión se conservó visible en título y diálogo de exportación. Se verificaron 2.721 velas cerradas comunes: O'=70000−O, C'=70000−C, H'=70000−L y L'=70000−H exactamente; volumen idéntico. Todas las curvas conservan la visibilidad y equivalen a 70000−curva original, con error máximo 5.83×10⁻¹¹ puntos. Dos exportaciones reflejadas coinciden en 2.722 velas y el regreso reproduce la referencia en 2.721. Se excluye la última fila de cada CSV.

El ajuste independiente de las seis recurrencias EMA entrega C=50 con error menor que 10⁻⁶ y RMSE menor que 4×10⁻¹². La primera ruptura y la aparición de las seis curvas ocurren en el mismo timestamp (1791833160) y cambian de alcista a bajista. La semilla esperada END low=30866.75 pasa a END high=39133.25, cuyo total es 70000. No se estima una nueva semilla libre ni se exige C=50 como criterio de aceptación de datos.

En esta ventana, duplicar, trasladar y reflejar precios conserva C=50. Ello respalda estudiar medidas normalizadas y simétricas o estructura temporal. No demuestra que C ignore dirección en otras ventanas, que exista alineación armónica ni cuál historial participa. Metadatos y fuentes internas del script no son completamente observables; las transformaciones afectan el historial completo disponible. Un mecanismo temporal puro y una geometría normalizada siguen siendo compatibles.

Siguiente prioridad: repetir estos controles en una ventana con C diferente, empezando por 12 octubre START18:55/END19:20, fuente/gráfico1m, con una referencia fresca antes de transformar. Eso permite comprobar si la simetría encontrada pertenece únicamente a la rama que produjo C50. Después, estudiar desplazamientos de START/END conservando extremos y ruptura; cambiar el viewport de Replay no elimina por sí solo el historial de Pine.

Auditoría reproducible: analizar_C_reflexion50.py genera C_reflexion50_resultados.json con ajustes, cobertura de 21 velas y una hora posterior, comparaciones, ruptura, visibilidad y hashes SHA256. CSV/capturas en manual/C_reflexion50_*. Gráfico guardado y restaurado en NQ1!, 1 minuto; layout principal sin modificar.
