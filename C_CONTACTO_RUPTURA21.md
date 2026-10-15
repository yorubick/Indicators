# C21: contacto al romper el rango y primera muestra

13 octubre 2026. Once controles21 del entrenamiento maestro, mismas fuentes que el gráfico15/60/120s. Se usaron las parejasCSV históricas aceptadas enumeradas en el preregistro, sin nuevas mediciones ni cambiosTradingView. No se usó validación reservada ni se modificó el maestro.

## Hipótesis que incorpora precios posteriores aEND

Se definió C como el período que hace que una de las seisEMA Lite toque un precio concreto en la primera ruptura. Periodos=24,89/3,8,89/9,72/27,89/27 vecesC/dt. Fuenteclose oHL2. SemillaENDlow en rupturaalcista yENDhigh en bajista. Se procesan todas las velas posteriores aEND, incluida la ruptura.

Objetivos fijados: high/low/medio del rango, closeEND, open/high/low/close/HL2 de la ruptura. Seis curvas xdosfuentes xnueveobjetivos=108configuraciones. No se elige objetivo ni curva diferentes para cada caso. Condición necesaria antes de buscar raíces: el C observado tiene que satisfacer el contacto con tolerancia1e-7precio.

**Ninguna configuración logra siquiera un contacto exacto en los11casos; máximo0/11.** El ensayo anterior de contactoEND no cubría esta operación posterior aEND.

### Robustez al redondeo de C

Después del resultado de contactoexacto se registró otra comprobación: permitir unCreal entre Cmedido-1 yCmedido+1. No se muestrearon raíces para asumir que no existían. Para alpha(C)=2/(1+factor*C/dt), el estado es una combinación convexa de semilla y precios. Si m es el número de actualizaciones yR el rango de semilla+precios, entonces:

`abs(dEMA/dC) <= m*R*max(abs(dalpha/dC))`.

El máximo de la derivada dealpha en el intervalo ocurre enCmedido-1. Se verificó0<alpha<=1 en todo el intervalo. Si el residuo enCmedido excede esa cota más1e-7, no puede haber raíz a una distancia<=1segundo. Cada una de las **108configuraciones** tiene al menos un testigo que la excluye incluso con ese margen generoso.

No se excluyen optimizaciones de otro tipo, otras escalas, objetivos distintos ni toda dependencia de datos posteriores aEND.

## Verificación de la trayectoria invisible

La primera publicación de las seiscurvas coincide en los11controles con el primer cierre estricto fuera del high/low del rango. Se comprobó cobertura consecutiva de velas desdeEND hasta ese cierre y OHLC del rango igual al maestro. Los valores publicados en la ruptura coinciden en las parejas aceptadas.

Usando C ya recuperado, fuenteclose y semillaEND, se reconstruyeron los66primerosvalores de curvas. Error máximo3.2741809263825417e-11. Los intervalosEND→ruptura varían de1 a89velas. Esto confirma la trayectoria de lasEMA publicada, no el instante interno en que se eligióC: es compatible con calcular antes o recalcular retrospectivamente al romper.

## Dato adicional: una muestra puede bastar en dos controles

En START18:58 END19:18 ySTART18:59 END19:19 (12oct,1m), la ruptura es la primera vela posterior aEND, a19:19 y19:20 respectivamente. Solo hay una actualización. Con semillaS y primerprecioX, el primer valor publicadoY permite invertir:

`alpha=(Y-S)/(X-S)`

`C=dt/factor*(2/alpha-1)`.

Sin emplear muestras posteriores a la ruptura, los seis canales recuperanC77 en ambos casos, con error máximo2.19e-10segundos frente a la referencia. SemillasS=30853.5 y30862.5. La inferencia usa la familia de períodos y la semilla verificadas; no revelaCantesdelaruptura. ResultadosC_primera_muestra_un_update.json.

## Alcance y continuación

Sigue desconocida la fórmula generadoraC. Ahora hay un método para observarCdesde la primera publicación cuando la ruptura ocurre en la primera vela posterior aEND; no necesitamos dos muestras visibles en esos casos. Para contrastar estado o dependencia posterior conviene priorizar este tipo de control, fijando antes una hipótesis numérica. No usar la reconstrucción retrospectiva como prueba de cálculo enEND.

Scripts probar_C_contacto_ruptura21.py y probar_C_contacto_ruptura21_cota.py, ambos con --spec antes de ejecutar. Preregistros y resultados C_contacto_ruptura21_*.json y C_contacto_ruptura21_cota_*.json. Etiquetas conocidas y ventanas solapadas: exploratorio, no validación ciega.
