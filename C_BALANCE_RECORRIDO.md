# C como calibración de una EMA al recorrido completo

13 de octubre de 2026. Análisis local de OHLC y extracciones originales verificadas. No se modificó TradingView.

**Resultado: esta búsqueda no identifica el generador de C.** Se contrastan cuatro condiciones sobre todo el recorrido, no solo el contacto con la vela final:

1. Suma de errores firmados cierre − EMA igual a cero.
2. Suma de error × valor absoluto del error igual a cero, que equilibra errores cuadrados positivos y negativos.
3. Posición media de la EMA dentro de las mechas igual al punto medio. Se omiten velas sin altura y no se recortan posiciones fuera de las mechas.
4. Error cuadrático medio, expresado como RMS, igual al rango verdadero medio de los pasos procesados.

Se busca una longitud EMA N que satisfaga la condición y se contrasta si puede relacionarse con C mediante `N = K × C / resolución`, con un mismo K para todos los rangos. La estimación inversa es `C = max(resolución, N × resolución / K)`; el mínimo es una hipótesis empírica.

## Diseño y límites

- Cuatro precios de actualización: cierre, hl2, hlc3 y ohlc4. El error siempre se mide frente al cierre.
- Recorrido cronológico e inverso; se incluyen o excluyen las velas de los extremos en cuatro combinaciones.
- Nueve semillas: OHLC del extremo donde comienza el procesamiento, máximo/mínimo/punto medio global y dos elecciones del extremo global según el desplazamiento neto del cierre. En el recorrido inverso se invierte el sentido del desplazamiento.
- Se prueban dos selecciones de raíz: la menor o la mayor encontrada. No se elige la más cercana al C conocido.
- Total: 2,304 modelos contando las dos ramas. Malla inicial de 1,200 longitudes entre 1.00001 y 10,000 velas. Solo se localizan raíces con cambio de signo, mediante interpolación lineal.
- Las condiciones se evalúan después de cada actualización EMA. En el recorrido inverso, el rango verdadero se calcula con el cierre previamente procesado, no como ATR cronológico estándar.

Los 34 casos anteriores se usan para el ajuste; cuatro saturados en la resolución se excluyen del criterio de existencia de raíz. Quedan 30 casos por encima del mínimo. Una raíz ausente en un caso saturado no se usa para rechazar el modelo.

Las cuatro ventanas nuevas (START 18:52, 18:53, 19:01, 19:02, END 19:20, fuente 15 s) se contrastan después. Sus C ya se conocían, por lo que esto es separación del ajuste numérico, no comprobación prospectiva. Las ventanas se superponen y pertenecen a la misma fecha.

## Resultados

La ampliación de semillas permite encontrar raíces en los 30 casos no saturados para 256 modelos. Tener una raíz en cada rango no implica que la escala K sea común. Se contrasta el intervalo admisible de K impuesto por cada intervalo observado de C.

La mejor aproximación, ordenada únicamente por el peor error de ajuste, usa:

- Recorrido cronológico, sin la primera vela, actualizado al cierre.
- Semilla en el extremo global a favor del movimiento neto: mínimo si el cierre final es mayor o igual que el inicial, máximo si es menor.
- Condición RMS(error) = rango verdadero medio.
- La menor raíz localizada.

Los factores individuales que pediría esta regla varían aproximadamente entre 1.356 y 12.751. El K geométrico ajustado es aproximadamente 3.2559. Su peor error de ajuste es 291.64 % y el de las cuatro ventanas posteriores 51.82 %. No coincide con ningún intervalo original de C en esos cuatro casos.

Esto no constituye una aproximación suficientemente fiable para incorporarla a una réplica.

## Control de precisión

Se repite el cálculo de la candidata mejor ordenada con 12,000 longitudes. La mayor variación relativa de sus raíces respecto a la malla de 1,200 puntos es `8.8431e-6`, aproximadamente **0.000884 %**.

En la malla refinada, para respetar simultáneamente los intervalos medidos de C, K tendría que ser mayor que aproximadamente 12.73497 y menor o igual que 1.35652. Es incompatible. La discrepancia de esa candidata no se explica por el tamaño de la malla.

El refinamiento solo controla la candidata mejor ordenada, no todas las reglas. La búsqueda finita no descarta raíces tangentes, longitudes fuera del intervalo, actualización previa a la vela, otras condiciones de calibración, semillas adaptativas ni otros algoritmos.

## Consecuencia para la investigación

Además de las reglas de pivotes y medidas promedio anteriores, estas cuatro calibraciones concretas de una EMA al recorrido completo no ofrecen una fórmula de C. Sigue sin haber una candidata que prediga los rangos de forma fiable. Esto limita otra familia de explicaciones; no permite estimar cuánto falta para reconstruir el algoritmo.

Resultados: `C_balance_recorrido.json` y `C_balance_convergencia.json`. Scripts reproducibles: `probar_C_balance_recorrido.py` y `refinar_C_balance_recorrido.py`, con Python y NumPy.

## Control adicional: evaluar antes de actualizar

Se repitieron las 2,304 configuraciones midiendo el error con la EMA anterior a procesar cada vela. Esta fase se ejecuta con `probar_C_balance_recorrido.py --before` y conserva los resultados previos en archivos separados.

152 configuraciones tienen raíces en los 30 casos no saturados, pero ninguna admite un K común compatible con sus intervalos de C. La mejor aproximación tiene error máximo de ajuste de 426.98 % y de contraste posterior de 51.38 %. Tampoco constituye un generador válido. No se refinó esta fase: el control numérico de 12,000 puntos documentado arriba se refiere solamente a la mejor candidata de la fase posterior.

Datos del control: `C_balance_recorrido_antes_update.json`. Ambos sentidos de evaluación siguen sujetos a las limitaciones de raíces con cambio de signo y rango finito de longitudes.
