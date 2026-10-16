# C: contraejemplos a selectores del último pivote/swing

13 de octubre de2026. Prueba local sobre23 ventanas verificadas de al menos21 velas, tomadas de C_matriz.json. NQ1!,12 de octubre, fuente60s. No hubo nuevas mediciones ni cambios en TradingView.

## Reglas explícitas

Se definen pivotes sobre mechas y sobre cierre, con una o dos velas a cada lado. Un máximo supera estrictamente todos los valores izquierdos y es mayor o igual que los derechos; el mínimo usa la condición inversa. Solo se confirma con velas comprendidas en el rango, sin mirar después de END. Estas son definiciones del experimento, no una afirmación sobre los pivotes del autor.

Se ensayan tres selectores:

- Último máximo y último mínimo confirmados.
- Último par consecutivo de pivotes opuestos, excluyendo pares simultáneos.
- Último pivote confirmado de cualquier lado. Los eventos se ordenan por índice y lado; si un bar es simultáneamente H/L, L queda después de H.

Para cada selector se comparan tres conjuntos de entradas: estructura seleccionada con todos los OHLC entre sus extremos; todos los OHLC desde su primer punto hasta END; y ese mismo tramo más los extremos globales del rango. Son36 definiciones:2 fuentes×2 radios×3 selectores×3 alcances.

No se intenta ajustar una duración, altura ni coeficiente: se buscan pares cuya **entrada seleccionada completa sea exactamente igual** pero C sea distinto. Si existe un par, ninguna función determinista basada exclusivamente en esas entradas puede generar ambos C.

## Resultado

Las36 definiciones tienen contraejemplos. Todas estaban definidas en las23 ventanas. Este resultado no descarta todo selector de swings: descarta usar exclusivamente los selectores y entradas enumerados. Un estado anterior, otra selección o una dependencia no proporcional del conteo total siguen abiertos.

## Ejemplo reproducible

Último pivote de mechas, radio1, tramo hasta END y extremos globales:

| START | END | Conteo total | C |
|---|---|---:|---:|
| 19:01 | 19:22 | 22 | 77 |
| 19:02 | 19:22 | 21 | 50 |

En ambos el selector elige el máximo confirmado19:20,H30870.50. Todos los OHLC seleccionados19:20–19:22 son idénticos; los máximos/mínimos globales son30870.75/30849.00. Es la misma entrada local, pero dos C diferentes. El OHLC exterior a ese tramo, START y el conteo total no son iguales y no se declaran aislados.

## ¿Lo explica multiplicar por el conteo total?

También se contrasta C=n×F(entrada_seleccionada), con o sin redondeo a segundos. Para entradas idénticas, F tendría que ser idéntica. Se concedió una tolerancia conservadora de±1 segundo a C antes de dividir por n, que incluye el efecto de nearest/floor/ceil además del caso sin redondeo. No se impone un mínimo de fuente.

En el ejemplo anterior:

- La ventana22 exige F entre76/22 y78/22, aproximadamente[3.45455,3.54545].
- La ventana21 exige F entre49/21 y51/21, aproximadamente[2.33333,2.42857].

No se intersectan. Las36 definiciones tienen también un contraejemplo de este tipo; un factor lineal de conteo no rescata esos selectores. No se descarta una función conjunta arbitraria F(estructura,n), una regla por ramas ni otras normalizaciones no lineales.

## Qué cambia en la investigación

El salto71→128 de END19:27→19:28 coincide con confirmar un máximo local bajo una definición concreta, pero esa coincidencia no basta para generar C. El mismo selector local produce entradas idénticas con resultados diferentes en otros rangos.

Los próximos modelos deben conservar explícitamente información anterior al último swing o especificar cómo el conteo global cambia la selección/cálculo. También sigue pendiente cerrar si se usan datos exteriores a START/END: estos contraejemplos no establecen independencia de esos datos.

Conviene probar inicializaciones o selecciones de primer pivote antes de volver a elegir otra batería de coeficientes. Que un selector no tenga contraejemplos tampoco sería validación de una fórmula: aún habría que predecir los C numéricos y contrastarlos fuera del episodio.

Archivos: probar_C_selectores_pivotes.py y C_selectores_pivotes.json. El JSON conserva definiciones, cobertura, número de pares contradictorios y dos testigos con todos los OHLC seleccionados para cada regla. Se vuelven a verificar los intervalos de Character a partir de los archivos correspondientes; no se usa el mínimo global refutado C>=fuente. La fórmula generadora general sigue pendiente.
