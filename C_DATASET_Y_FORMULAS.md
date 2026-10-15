# Conjunto consolidado y contraste de fórmulas explícitas

13 octubre2026. No se recuperó todavía el generador general de C. Esta tanda consolida las mediciones de11informes y contrasta dos familias numéricas, sin modificar sus constantes a partir de validación.

## Lo identificado

En las34selecciones observadas con menos de21velas:

`C = max(Δ, n × Δ × 10 / 183)`

n es el conteo inclusivo de velas fuente yΔ la duración de la fuente en segundos. Coinciden34/34, incluyendo fuentes15s/60s/120s y dos fechas. No se afirma una ley universal fuera del dominio observado; una vela única sin curvas sigue siendo no observable. Las59selecciones restantes son la rama larga pendiente, no explicada por esta continuación.

## Consolidación y partición

`C_dataset_verificado.json` reúne93selecciones únicas a partir de107referencias en11informes previamente auditados. Clave de deduplicación:fuente,START,END. Toda referencia repetida exige OHLC idéntico y C concordante dentro de1e-7segundos. No hubo conflictos. Se conserva procedencia, pareja cuando está disponible,OHLC completo y hash. `C_dataset_indice.csv` permite revisar la tabla manualmente.

Partición establecida antes del ajuste: entrenamiento12oct con ambos límites en la hora06 oSTART>=18; validaciónotros episodios y13oct. Las extensiones06:57–07:20 permanecen junto al episodio07en validación para no dividir ventanas solapadas entre conjuntos.

| Rama | Ajuste | Validación |
|---|---:|---:|
|Corta|21|13|
|Larga|32|27|

Las etiquetas ya fueron vistas durante la investigación. La partición controla cómo ajusta constantes el algoritmo; no es una prueba prospectiva ni ciega para el investigador. Tampoco son93episodios independientes: muchas ventanas se solapan. Los controles originales de estabilidad de curvas se heredan de los informes; el consolidador no los ejecuta todos de nuevo. Es un núcleo consolidado, no todos los archivos históricos del proyecto. Se excluyen los experimentos de visualización agregada donde fuente y gráfico difieren.

## Familia de tendencia y recorrido

Regla larga candidata:

`C = cuantizar(K × n × Δ × 10/183 × g(r,ER))`

r=valor absoluto de correlaciónPearson entre precio e índice de vela;ER=desplazamiento neto absoluto/suma de cambios absolutos. Se pruebanclose,hl2,hlc3,ohlc4; ventana completa o últimas21;17transformaciones explícitas y nearest/floor/ceil:408modelos. Las transformaciones incluyen1±r,1±r²,inversas,raíz del residuo1−r² y variantes deER. Las definiciones completas están en `probar_C_tendencia_recorrido.py` y se registraron antes en el protocolo.

Para cada modelo se calcula el intervalo necesario de un K común que acertaría todos los C de entrenamiento después de cuantizar. **Los408intervalos son vacíos.** No es un problema de que el optimizador eligiera malK: ningúnK único permite el ajuste exacto de esa familia en los controles usados. No se aplica un sueloΔ a la rama larga, pues datos anteriores mostraron C menor queΔ.

Un ejemplo del mejor candidato por ajuste (ohlc4,ventana completa,g=1/(1+r),nearest) exige K>=2.7737656 para el controlC134 de19:04–19:29 yK<1.0439551 para C50 de19:02–19:22. Es una contradicción numérica dentro de esa fórmula. Su Kmediano acierta7/32 y tiene error máximo60segundos; no es una aproximación presentada como generador.

Ningún candidato completo pasó entrenamiento, por lo que no se usaron los27controles largos de validación para ajustar, seleccionar o rescatar modelos. Rechazar408variantes no demuestra cercanía a la fórmula ni excluye toda función de tendencia.

## Volumen: entrada antes no cubierta

Las búsquedas revisadas de C no tenían ensayos explícitos con volumen. Se mostró temporalmente el indicadorVol existente, se cargó12oct04:45 y se exportó en1m dos veces. `manual/C_VOL_1m_a/b.csv` incluyeVolume. El layout volvió a su estado inicial yVol quedó oculto.

La serie se une por timestamp a87selecciones1m del conjunto; para cada unión se exige OHLC idéntico al original. Se excluyen las seis selecciones15s/120s porque no se exportó su volumen nativo. Salida `C_dataset_con_volumen.json`. Tener esa serie no demuestra que el indicador la use.

Se registró antes del cálculo otra familia con Kúnico: concentración de volumen por número efectivo `(sumV)²/sum(V²)`, relacionesVolEND/media yVolSTART/media,EMA20Vol (semilla media20 y actualización2/21), coeficiente de variación, correlación precio-volumen y desvíoVWAP normalizado por rango/std de precio.22formas ×3cuantizadores=66modelos,30rangos largos de ajuste y27de validación. Todos tienen intervaloKvacío; ninguno pasa ajuste. No se abrió validación para rescatar esos modelos. Esto no refuta algoritmos de volumen con selección, memoria o funciones distintas.

## Reproducción

- `consolidar_C_verificado.py` ->`C_dataset_verificado.json` y`C_dataset_indice.csv`.
- `probar_C_tendencia_recorrido.py` ->`C_tendencia_recorrido.json` con todos los modelos y testigos de contradicción.
- `probar_C_volumen.py` ->`C_dataset_con_volumen.json` y`C_volumen_candidatos.json`.
- Predicciones/definiciones previas:`C_DECIMALES_PREDICCIONES.md`.

Se ejecutaron los tres scripts hasta completar las salidas; la segunda familia requirió convertir escalaresNumPy a tiposPython para serializar resultados. El error inicial de serialización no se trató como resultado matemático.

Layout en referencia12oct18:55–19:20, gráfico1m, Lite1m, CharacterChart, Replay apagado yVoloculto. Captura `manual/C_dataset_volumen_restaurado.png`.

## Decisión de investigación

La fórmula corta es la única relación exacta encontrada en este conjunto. No aceptar un modelo largo por error promedio bajo o unos pocos aciertos. Un próximo candidato necesita especificar un algoritmo conjunto:qué datos usa,qué segmento/estado selecciona yqué operación numérica devuelveC. Debe explicar los contraejemplos y producir una predicción en un rango nuevo reservado.

Sigue sin demostrarse que las únicas entradas internas sean OHLC/volumen del rango a la resolución de lasEMA; otra serie, prehistoria o información entreEND y primera publicación son posibilidades abiertas. Rechazar estas familias no cierra esas dependencias. Buscar una fórmula exclusivamente de las entradas asumidas puede fallar aunque el código original sea simple.
