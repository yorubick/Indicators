# Frontera de21 velas: tercera fuente y evolución posterior

13 de octubre de2026. NQ1!, ETH, UTC, BADJ apagado. Anclas del12 de octubre. Lite v1.2 fuente explícita igual al gráfico; Character v6.5.36 perfilB Manual fuenteChart. Siete controles nuevos verificados con OHLC completos, pareja repetida de16 curvas y C Lite contenido en intervalo Character.

## Predicciones de fuente120s

Antes de medir se fijó C=max(Δ,n*Δ*10/183) en C_DECIMALES_PREDICCIONES.md. START18:00, fuente/gráfico2m:

| END | n | Predicción de relación corta | C medido |
|---|---:|---:|---:|
| 18:36 | 19 | 124.59016393 | 124.59016393 |
| 18:38 | 20 | 131.14754098 | 131.14754098 |
| 18:40 | 21 | 137.70491803 | 137 |

Las dos predicciones cortas aciertan. En21 velas la continuación falla. Aunque137 coincide con el entero inferior a137.704918, no se deduce un redondeo general: los otros controles21 daban16 frente a17.2131 (15s) y75/77/81 frente a68.8525 (1m).

La frontera observada se repite en fuentes15/60/120s. Veintiuna velas corresponden a duraciones entre anclas5/20/40 minutos respectivamente: apoya investigar una condición por conteo fuente en lugar de un umbral único en minutos. No establece el código ni un umbral universal; los controles de otra fecha eran de60s.

## Rama larga, fuente60s

START19:00 fijo, END consecutivos:

| END | n | C | Máximo global | Mínimo global | Close END |
|---|---:|---:|---:|---:|---:|
| 19:20, control anterior | 21 | 77 | 30870.50 | 30846.00 | 30870.50 |
| 19:21 | 22 | 102 | 30870.50 | 30846.00 | 30868.50 |
| 19:22 | 23 | 77 | 30870.75 | 30846.00 | 30868.50 |
| 19:23 | 24 | 77 | 30870.75 | 30846.00 | 30866.50 |
| 19:24 | 25 | 60 | 30870.75 | 30846.00 | 30869.50 |

La secuencia77→102→77→77→60 no se explica prolongando la pendiente corta. La rama posterior puede volver al mínimo de fuente; observar C=60 no identifica por sí solo la rama de calentamiento.

C cambia21→22 velas sin nuevo extremo global. C cambia24→25 conservando extremos globales. Dos END consecutivos19:21/19:22 tienen el mismo cierre y C distintos: no basta el cierre final aislado. Estas observaciones no excluyen conteo combinado con precios, diferencias de mechas, estado recursivo ni selección de ventana/solución.

## Auditoría

Los primeros archivos a/b de19:21 y19:22 mostraban recálculo incompleto de Character y no se aceptan como parejas estables. Los primeros de19:23/19:24 tenían curvas posteriores utilizables pero no los OHLC del rango histórico, porque el viewport seguía en la jornada actual; no se usan para analizar estructura. Se volvió explícitamente al12 de octubre y se verificaron anclas. Se aceptan c/d de los cuatro controles1m. Todos los originales diagnósticos se conservan.

Los tres controles2m usan a/b con OHLC completos y curvas idénticas. El analizador exige la pertenencia del C decimal al intervalo Character, sin exigir entero compatible para19/20 velas. Comparar_Lite_Character.py añadió soporte de etiqueta2m sin cambiar archivos de1m/15s.

## Estado y siguiente experimento

La relación corta predice19/20 velas en tres fuentes y dos fechas del conjunto acumulado. Es evidencia de una rama simple, sin recuperar el generador general. Los valores posteriores dependen de algo adicional al conteo proporcional y a los extremos aislados.

Conviene comparar ventanas de longitud fija21/22/23 desplazando ambos extremos, y comprobar si anclas diferentes que conservan un mismo tramo final dan C distintos. Ese diseño separa conteo de estructura y prueba si el algoritmo selecciona una subventana o un estado inicial. Las condiciones deben fijarse antes de medir, evitando buscar retrospectivamente un pivote que explique cada C.

Script analizar_C_frontera21.py; datos C_frontera21.json incluyen todos los OHLC y restricciones. CSV manual/Lite_1900_192100/192200/192300/192400_1m_[c/d].csv y manual/Lite_180000_183600/183800/184000_2m_[a/b].csv. Capturas C_rama_larga_*_anclas.jpg y C_frontera_2m_anclas.jpg.

Referencia restaurada y guardada:12 de octubre18:55–19:20, fuente/gráfico1m. Captura C_frontera21_referencia_final.jpg.
