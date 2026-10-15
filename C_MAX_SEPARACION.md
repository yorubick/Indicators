# Primer contraste matemático de inicialización sobre la matriz

13oct2026. Análisis local, sin modificarTradingView. Se revisaron las familias anteriores de contacto final/interior, cruce deEMAs, balance de errores del recorrido, semillaSMA yAR(1). La nueva condición es distinta: maximizar separación final, no buscar un contacto/cero.

## Hipótesis congelada antes de ejecutar

Para cada C entero entre1y600segundos se procesan dosEMAs sobreclose, conNfast=72*C/(divisor*dt),Nslow=89*C/(divisor*dt),N>=1. Se elige elC que maximiza `abs(EMAfast_END-EMAslow_END)`; empate dentro1e-12en precio normalizado elige elmenorC.

Cinco divisores conocidos de la familia de curvas:3,9,27,1,1/3. Seis inicializaciones fijas:open/high/low/close deSTART, ylow/high de las primeras20velas. EnSTART se procesan cierres desde la segunda vela; enbootstrap20se inicializa en la vela20 y se procesa desde la21. Elbootstrap20es una hipótesis motivada por la frontera corta/larga observada; no una propiedad conocida del indicador.

Treinta configuraciones; ninguna constante ajustada, ninguna semilla elegida por caso, ninguna condición sobre timestamps/precios absolutos. El modelo necesita acertar las nueve selecciones locales antes de evaluar los32largos de entrenamiento. La rama larga no recibe un sueloC>=dt.

Definición: `C_max_separacion_preregistro.json`; script `probar_C_max_separacion.py --spec`, después ejecuciónsin--spec. La matriz y sus valoresC ya eran conocidos: esto es un contraste exploratorio con especificación previa al cálculo, no predicción prospectiva deCdesconocido.

## Resultado

Ninguna de las30configuraciones acertó siquiera unC exacto de la matriz. Ninguna supera las nueve; no se evaluaron los32largos ni la validación para rescatar el modelo.

En las270comparaciones hay unC alternativo admisible con separación estrictamente mayor que la delC observado. La menor diferencia del objetivo es3.589729602460068e-8en precio normalizado, frente tolerancia1e-12. Ninguna predicción cae en el límite superior600. Ampliar el límite superior no puede convertir elC observado en máximo: ya hay un testigo mejor dentro de la malla.

Esto descarta específicamente una elección deC entero por esa máxima separación, esas entradasclose y esas semillas. No descarta otras funciones objetivo, ajustescontinuosantesderedondear, entradashigh/low/hl2, reinicios, otros filtros ni condiciones sobre el historial completo.

Resultadosporconfiguración ytestigos: `C_max_separacion_resultados.json`. No se promovió ninguna aproximación por cercanía.

## Colisión de estado más general para una inicialización

Los casos START19:03:15 y19:03:30,ambosEND19:23:45, danC88y61. LoshighdeSTART son ambos30857.00. Bajo el modelo que inicializa cualquierEMA en esehigh y procesa cierresdespuésdeSTART:

- Elprimer caso procesa adicionalmente elclose19:03:30=30857.00.
- La actualización `v+=alpha*(30857-v)` deja v exactamente en30857para cualquier período, puesvyaera30857.
- Después, ambos procesan exactamente los mismos cierres en el mismo orden.

Por inducción, para cualquier período fijo ambos tienen el mismo estado final; lo mismo ocurre con cualquier conjunto de esos filtros. Se comprobó igualdad exacta de los objetivos en los cinco divisores ytodoslosCdelamallacomo control numérico, pero la identidad se deduce de la recurrencia y no depende de600.

Por tanto, ninguna selección determinista basada exclusivamente en esos estados finales yelobjetivoidentico podría devolver88enunrangoy61enelotro. Una regla de ese tipo tendría que consultar otra entrada:conteo/duración,otraparte delhistorial,otroprecio deinicialización,mechas uotroproceso. El argumento no excluye selecciones que utilizanexplícitamenten,límitespermitidosdependientesden,tiempos uotrosdatos.

## Dirección posterior

No repetir búsquedas de contactos/cruces/balances ya descartadas ni asignarC54/61/67/88como tablas de salida. El siguiente contraste acotado puede cambiar la entrada del filtro a una medida que conserve las mechas, comoHL2, manteniendo los otros componentes explícitos; la colisión anterior deja de ser idéntica paraHL2. Esa diferencia justifica probar la dependencia de entradas, pero no demuestra que el autor utiliceHL2. Si se prueba, fijar su especificación antes de calcular y exigir los nueve controles completos sin reajustar constantes después.

C sigue sin fórmula general identificada. Estas restricciones no cuantifican cuánto falta ni demuestran una máquina de estados.
