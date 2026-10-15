# Sustitución de entrada y familia continua de mezclas

13oct2026. Análisis local sin acciones enTradingView. No se ajustaron constantes ni se puntuó entrenamiento32/validaciónreservada para rescatar candidatos.

## Sustitución controlada: HL2

Se mantuvieron las30configuraciones del contraste anterior:seis semillas, cinco divisores conocidos72/89, C entero1..600,N>=1, objetivo de máxima separación absoluta deEMAs enEND y regla de empates. Solo se sustituyócloseporHL2=(high+low)/2en las actualizaciones.

Especificación congelada antes de ejecutar:`C_max_separacion_hl2_preregistro.json`. Implementación:`probar_C_max_separacion_hl2.py` y motorparametrizado `probar_C_max_separacion.py`. La parametrización conserva exactamente las270predicciones/objetivos anteriores usandoclose, verificado contra elJSONoriginal.

Resultado:ningún modelo acierta los nueve controles. El máximo es1/9, en dos configuraciones (seedSTART_high/divisor9 yseedSTART_close/divisor9). Hay268testigos con mayor separación que la correspondiente alC observado; las dos coincidencias restantes no validan un modelo completo. Ninguna predicción toca600. Resultados:`C_max_separacion_hl2_resultados.json`.

## Todos los pesos fijos entre close y HL2

Se preregistró después una familia más amplia explícita, antes de resolver sus restricciones:

`price(lambda)=lambda*close+(1-lambda)*HL2`, `0<=lambda<=1`.

El mismo peso debe utilizarse en todos los rangos. Contieneclose(lambda1),HL2(lambda0) yHLC3(lambda1/3). Las semillasOHLC/primeros20extremos no cambian conlambda. No incluyeOHLC4, cuya entradaopenadicional no está representada en esta mezcla.

LaEMA es lineal en su entrada cuando la semilla y el período están fijados. Por tanto, para cadaC candidato:

`D_C(lambda)=lambda*D_C_close+(1-lambda)*D_C_HL2`, conD=EMAfast_END−EMAslow_END.

Para queC observado sea una salida admisible, su valor absoluto debe superar a todos los competidores:

`abs(D_observado(lambda)) >= abs(D_competidor(lambda)) - 1e-10`.

Es una condición necesaria más débil que el modelo original: permite todos los empates en vez de exigir elmenorC yusa una tolerancia100veces mayor. Se separan intervalos en los ceros de los términos afines; en cada intervalo la desigualdad es lineal. Se resuelve y se intersecta entre todos los competidores ycasos, sin muestrear pesos para el resultado principal.

## Resultado continuo

**0/30configuraciones admite algúnpeso compatible.** Todas quedan rechazadas ya por el primer control local: START19:03:00,END19:23:15,C61. No es necesario usar los otros ocho para rechazarlas. Tampoco se evaluaron los32largos ni la validación.

Especificación:`C_mezcla_separacion_preregistro.json`. Script:`probar_C_mezcla_separacion.py`. Intervalos/condiciones que vacían las intersecciones:`C_mezcla_separacion_resultados.json`.

Verificación independiente del solucionador:

- 6000comparaciones aleatorias entre pertenencia a sus intervalos yla desigualdad absoluta directa:coinciden todas.
- 1001pesos uniformes en cada una de las30configuraciones del primer control:ninguno compatible. El déficit mínimo muestreado del objetivo es0.00010399552593476358en precio normalizado, muy porencima de1e-10. Esta malla verifica el cálculo; el rechazo continuo procede de las intersecciones piecewiselineales, con aritméticafloat.

## Qué se descarta y qué falta

Cambiar el precio de entrada entreclose,HL2 ysu mezcla fija no rescata esta selección deC por máxima separación final conlas semillas/períodos enumerados. La coincidencia1/9deHL2 no se promovió ni se ajustaron pesos por ventana.

No se descarta cualquier uso deEMAs,otras inicializaciones,fuentesdistintas,pesosadaptativos,objetivosdiferentes,calibracióncontinua antes de redondear ni códigofuera delrangoseleccionado. LosC originalesyaeran conocidos, por lo que estas pruebas son exploratorias con especificación previa al cálculo, no validaciónprospectiva.

La siguiente propuesta necesita otra condición matemática de selección delperíodo oestado adicional, ydebe respetar la matriz completa. Revisar primero contactos/cruces yreglas anteriores ya descartadas; no convertir54/61/67/88en constantes deunselector paraacertarlos retrospectivamente. C sigue sin fórmula general identificada.
