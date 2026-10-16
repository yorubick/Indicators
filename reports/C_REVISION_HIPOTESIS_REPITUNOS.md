# Revisión de la propuesta de repitunos en base 3

13 de octubre de 2026. Revisión de la propuesta compartida por el usuario, contrastada con mediciones locales. No se ejecutó ni se inspeccionó el Pine propuesto: no se encontraron PoiSzn_C_Detector_Lab.pine ni INFORME_DESCUBRIMIENTO_ORIGEN_C.md bajo G:/trading al buscar sus nombres.

## Identidad aritmética frente a generador

R(k)=(3**k-1)/2 genera 0,1,4,13,40,121 para k=0,1,2,3,4,5. Los offsets0,1,13,40 seleccionan k=0,1,3,4 y omiten k=2. Si k es la cantidad de velas de15s que faltan para :45, k debe ser0,1,2,3, y la propuesta daría C66,67,70,79; no C66,67,79,106.

Elegir k=3 para dos velas pendientes y k=4 para tres podría ser una hipótesis adicional, pero falta una regla que determine k desde los datos, sin mirar el C objetivo. Identificar que13 y40 son repitunos no determina esa regla ni el origen de la base66.

## Contraejemplo al offset fijo por cuarto de minuto

START fijo18:55, fuente15s, anclas del12 de octubre:

| Segundo de END | END19:20 | END19:21 |
|---|---:|---:|
| :00 | 106 | 115 |
| :15 | 79 | 106 |
| :30 | 67 | 79 |
| :45 | 66 | 66 |

Con base66 en ambos minutos, un offset que depende solo del segundo de END no puede explicar ambos. Los offsets de19:21 son49,40,13,0; la propuesta enumera40,13,1,0. Esto no refuta toda operación ternaria, pero sí el esquema horario fijo que se sugiere.

Las diferencias88−79=9 y115−106=9 son verdaderas. Pueden motivar una investigación, pero no demuestran que el algoritmo use potencias de3. Que la familia de períodos EMA use divisores3/9/27 tampoco demuestra que el generador de C emplee el mismo método.

## Cómo convertir la propuesta en una prueba

Antes de ejecutarla como generador, definir base b y k mediante reglas explícitas que solo reciban entradas disponibles, y explicar el salto omitido k=2. Especificar condiciones para sumar9. No admitir C medido como entrada de esas reglas ni constantes específicas por ejemplo.

Contrastar primero con la tabla completa anterior, START variables C123/118/67/106/66/88/79 y controles bajistas C116/113/110. Si una regla sobrevive, fijarla antes de medir otra jornada.

El modo manual del Pine podría ser útil para visualizar la reconstrucción de curvas con C suministrado. Esa coincidencia no valida su modo automático. Para afirmar curvas idénticas se deben verificar fuente efectiva, períodos decimales de Lite, semillas END, actualizaciones ocultas antes de ruptura y publicación por cierre exterior. No se revisó el contenido del archivo y no se presume cómo lo implementó.

Referencias locales: C_PRUEBAS_15_SEGUNDOS.md (tabla END19:20 y START), C_END_BARRIDO.md (END19:21), LITE_CHARACTER_END.md (repetición independiente en Lite). La fórmula generadora de C sigue pendiente.
