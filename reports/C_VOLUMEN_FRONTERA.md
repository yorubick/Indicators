# C y volumen: controles nativos de 15 segundos

13 octubre 2026. Se recuperó volumen de las exportaciones ya existentes C_recorte1903_30_c/d.csv. Para los nueve controles de C_matriz_frontera15s.json se exige OHLC idéntico al registro original y OHLC/Volume idénticos en ambas exportaciones, excluyendo sus últimas barras. Se verifica separación temporal15s. No se dividió volumen de1m para fabricar datos15s. Dataset enriquecido separado: C_matriz_frontera15s_volumen.json.

## Qué aporta esta prueba

El volumen sigue siendo una entrada posible, no demostrada. Las66 fórmulas anteriores se habían evaluado en30 ventanas largas de1m; su fracaso no excluía selección, umbrales ni memoria con volumen. Ahora se probaron las mismas22 características numéricas en los nueve controles15s, con un K positivo común libre y tolerancia generosa de C observado +/-1 segundo. Las características incluyen concentración de volumen, volumen inicial/final frente a media, EMA20 de volumen, coeficiente de variación, correlación precio-volumen y desvíoVWAP normalizado. Ningún intervalo común de K es factible: **0/22**. Esto no equivale a excluir toda función de volumen.

## Pareja decisiva, 12 octubre, UTC

| START | END | Velas | Volumen total | C |
|---|---|---:|---:|---:|
| 19:03:15 | 19:23:45 | 83 | 8413 | 88 |
| 19:03:30 | 19:23:45 | 82 | 8275 | 61 |

Se elimina una vela de volumen138, un1.64% del volumen del primer rango. C cae27 segundos, un30.68%. La vela retirada ocupa el puesto19 por volumen descendente en ese rango (18 velas tienen mayor volumen). No es su máximo de volumen. Esta diferencia de magnitudes no refuta un umbral ni una decisión discreta.

La vela de máximo volumen es la misma en los nueve rangos: 19:20:30 UTC, volumen236, O30866/H30868.75/L30866/C30868.25. Elegir exclusivamente ese pico no distingue los valores54/61/67/88. El descriptor más amplio preregistrado, que también incluye n y ENDclose, no presentó colisiones: **eso no valida una fórmula de pico**, solo significa que este test de suficiencia no la refuta con esas entradas.

Se detectaron cuatro parejas con el mismo END y las mismas últimas80 velas completas OHLCV, pero distinto C. Añadir volumen al sufijo antes compartido no basta para explicar C como función exclusiva de esas80velas y END. Esto no excluye un conteo total, volumen anterior, inicialización o memoria desde START.

## Cómo continuar

No hay evidencia causal de volumen: al cambiar START cambian simultáneamente precios, volumen, conteo e inicialización. Aún no tenemos un control que varíe volumen manteniendo esas otras entradas constantes. Un candidato con volumen debe especificar qué umbral o estado depende de él, mostrar qué decisión cambia al retirar la vela138 y explicar también que con END19:23:30 la misma exclusión deja C67 en ambos rangos. Después debe generar una predicción en otro episodio antes de observar C.

No se cambiaron TradingView ni el dataset maestro, ni se usó entrenamiento32 o validación reservada. Nueve casos solapados y conocidos: análisis exploratorio, no validación independiente. FórmulaC desconocida.

Reproducción: probar_C_volumen_frontera.py --spec, luego sin argumentos. Reglas: C_volumen_frontera_preregistro.json. Salida completa: C_volumen_frontera_resultados.json.
