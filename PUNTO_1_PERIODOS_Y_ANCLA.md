# Períodos y ancla: segunda fase

12 octubre 2026. Character Tree v6.5.36, perfil B, selección Manual. Investigación empírica mediante ajustes y exportaciones de TradingView, sin acceso al código privado.

Actualización: `OBTENCION_C.md` añade extracción automática de C, controles con END fijo y comparación entre replay y gráfico completo. La generación de C únicamente desde OHLC sigue abierta.

## Qué se resolvió y qué sigue abierto

Se identificó una fórmula compacta que explica los **100 períodos observados en diez configuraciones**: dos longitudes base, 72 y 89, escaladas por un tiempo Character, C. Las pruebas abarcan fuentes de 1 minuto y 15 segundos.

**Todavía no se identificó el algoritmo que obtiene C desde las velas del rango.** Por tanto, el primer punto no está totalmente resuelto. La fórmula siguiente recibe C como entrada; no permite elegir dos fechas y calcular automáticamente todas las curvas sin observar primero C.

También se comprobó que las curvas arrancan de una mecha de la vela END de la resolución usada: high en el caso bajista original y low en cinco configuraciones alcistas con OHLC del ancla disponibles. Una vela final roja puede usar low: el color de esa vela no determina por sí solo la mecha.

## Fórmula de la familia

Sea Δ el intervalo de datos fuente en segundos y C el tiempo Character, también en segundos. Para cada nube con multiplicador m:

```
N rápido = redondear(72 × C × m / Δ)
N lento  = redondear(89 × C × m / Δ)
```

| Nube | Multiplicador m |
| --- | ---: |
| Layer A | 1/3 |
| Layer B | 1/9 |
| Layer C | 1/27 |
| Extra cloud 1 | 1 |
| Extra cloud 2 | 3 |

El modelo implementado redondea al entero más cercano y limita los períodos a al menos 1. Los casos observados no distinguen todas las convenciones posibles en empates exactos de .5 ni prueban el límite de 1. Esas dos convenciones son decisiones explícitas del modelo, no reglas internas demostradas.

**Ejemplo:** C=80 s, Δ=60 s. A produce 32/40; B 11/13; C 4/4; extra 1 96/119; extra 2 288/356. Coinciden con el rango 19:11–19:31 UTC de la tabla.

La implementación está en `familia_ema.py`. No incorpora un algoritmo inventado para resolver C.

## Casos medidos

Todas las horas son UTC del 12 octubre 2026, NQ1!, ETH. Cada cambio se guardó y recalculó. Los CSV usados contienen valores de las curvas y cierres de la misma resolución fuente.

| START | END | Duración entre timestamps | Fuente Δ | C compatible (segundos) | Extra 1 rápido/lento |
| --- | --- | ---: | ---: | ---: | ---: |
| 04:45 | 04:50 | 5 min | 60 s | 60 | 72/89 |
| 04:45 | 05:00 | 15 min | 60 s | 60 | 72/89 |
| 04:45 | 05:05 | 20 min | 60 s | 75 | 90/111 |
| 04:45 | 05:15 | 30 min | 60 s | 116 | 139/172 |
| 04:45 | 05:25 | 40 min | 60 s | 113 | 136/168 |
| 19:00 | 19:20 | 20 min | 60 s | 77 | 92/114 |
| 18:50 | 19:20 | 30 min | 60 s | 118 | 142/175 |
| 19:11 | 19:31 | 20 min | 60 s | 80 | 96/119 |
| 19:11 | 19:31 | 20 min | 15 s | 66 | 317/392 |
| 19:18 | 19:20 | 2 min | 15 s | 15 | 72/89 |

C se identificó invirtiendo las restricciones de redondeo de los diez períodos. En cada configuración, la intersección admite un único número entero de segundos, indicado en la tabla. Eso no demuestra que internamente C siempre sea entero: el intervalo completo compatible se conserva en `familia_character.json`.

Tres conclusiones:

1. **C no es una función exclusiva de la duración del rango.** Tres rangos de 20 minutos, con fuente de 1 minuto, requieren 75, 77 y 80 segundos. Ampliar el rango de 30 a 40 minutos en la mañana redujo C.
2. **La fuente cambia el resultado.** Con los mismos timestamps 19:11–19:31, C pasa de 80 a 66 segundos al cambiar de 1 minuto a 15 segundos. La vela END también cambia de OHLC al cambiar su granularidad. No se puede atribuir esa diferencia solamente a un cambio de escala temporal.
3. Los rangos cortos probados saturan en C=Δ, dando las mismas longitudes base aunque representen horizontes físicos diferentes. Es compatible con un mínimo igual al intervalo fuente, pero todavía falta delimitar el umbral en otras condiciones.

## Mecha inicial y recorrido posterior

La EMA sigue usando close después del ancla. La semilla es una condición inicial diferente de su fuente.

| Configuración | Semilla común recuperada | Comparación con END |
| --- | ---: | --- |
| 04:45–05:00, Δ=60 s | 31,254.25 | high |
| 19:00–19:20, Δ=60 s | 30,864.50 | low |
| 18:50–19:20, Δ=60 s | 30,864.50 | low |
| 19:11–19:31, Δ=60 s | 30,872.25 | low, aunque END tiene cuerpo bajista |
| 19:11–19:31, Δ=15 s | 30,875.00 | low de la vela de 15 s |
| 19:18–19:20, Δ=15 s | 30,866.00 | low de la vela de 15 s |

Para recuperar la semilla se invirtieron todas las actualizaciones entre END y la primera muestra visible, incluyendo los cierres que no tienen plots visibles. Las diez curvas dan la misma semilla en cada caso. Luego se reconstruyeron hacia delante desde el high/low OHLC correspondiente, usando los períodos de la fórmula familiar.

Se compararon **13,670 valores** en seis configuraciones con el ancla presente en los datos. El error máximo fue **3.64 × 10^-11 puntos**. Los restantes cuatro CSV, que comienzan después del ancla, permiten comprobar los períodos y la recurrencia pero no toda la inicialización.

El clasificador que escoge automáticamente high o low todavía está abierto. La posición del cierre dentro del rango es una hipótesis compatible con los casos observados; aún no se ha probado como regla general. No se debe sustituir por «vela verde = low, vela roja = high».

## Disponibilidad de los plots

En 19:00–19:20, Δ=60 s, el CSV comienza a mostrar las curvas a las 19:26, después de la ruptura alcista de la caja. Sin embargo, los valores equivalen a haber actualizado las EMAs desde las 19:21 con semilla low de END.

El control 19:17–19:37 dibujó la caja pero mantuvo todas las columnas de curvas vacías en el tramo observado. En ese tramo no hubo ruptura del máximo o mínimo de la caja. Forzar Direction mode a Bull generó etiquetas, pero no hizo aparecer las curvas. La exportación está en `character_recent_bear_body.csv`; se conserva como control sin plots y se excluye del ajuste de períodos.

Esto apoya una condición de visibilidad ligada a la ruptura del rango. Sus reglas exactas, y si la ruptura debe confirmar al cierre, requieren replay. Estas observaciones estáticas no demuestran repintado.

En la continuación posterior se comprobó la primera aparición en 22 rangos Manual con OHLC completo: en todos coincidió con el primer cierre posterior a END estrictamente fuera del high/low global del rango. También se tomaron cortes tempranos de replay para C≈134; los valores anteriores a la última fila coincidieron exactamente con el histórico, mientras la última fila de plots repetía el estado previo. Véase `C_PRUEBAS_15_SEGUNDOS.md`, sección de historial previo, replay temprano y aparición de curvas. Esto valida una regla empírica de visibilidad para esas muestras, sin demostrar todas las condiciones intravela ni definir C.

## Próxima pregunta técnica concreta

La incógnita se redujo a:

```
velas del rango + resolución fuente → C y lado inicial
C + resolución fuente → diez períodos (modelo identificado)
mecha END + períodos + cierres posteriores → curvas (reconstrucción validada)
```

Para resolver la primera flecha hay que contrastar el ajuste al recorrido de precio del rango y a la mecha END. Ya se descartaron una regla lineal basada solo en duración y varios ajustes simples de una EMA al wick, tanto desde el inicio del rango como desde el historial previo. Ninguno explicó todos los casos.

No se ha confirmado una fórmula de ajuste alternativa. Tampoco se ha extendido la familia a otros perfiles o al modo Auto Balanced.

## Reproducción y archivos

Desde esta carpeta:

```powershell
python estudiar_rangos.py
python inferir_familia.py
python validar_familia.py
```

Los scripts solo usan la biblioteca estándar. Los archivos `estudio_rangos.json`, `familia_character.json` y `validacion_familia.json` conservan los ajustes, intervalos compatibles de C y errores de reconstrucción.

`validar_familia.py` comprueba los 100 períodos y reconstruye las seis configuraciones completas. **No es una validación independiente de la generación de C**: C fue inferido de los plots, que es precisamente la parte todavía desconocida.

Los scripts `probar_ajuste_mecha.py`, `probar_ema_historica.py` y `probar_fuentes_rango.py` son pruebas exploratorias de hipótesis descartadas, no la implementación del indicador. La guía de Whop se consultó, pero sus pistas de subtítulos permanecieron sin contenido accesible; no se atribuye al autor una explicación hablada que no se haya leído.

El layout de investigación se dejó con el caso 19:11–19:31, fuente y gráfico de 1 minuto, Direction mode Auto. Seven Cloud y CCII siguen añadidos y ocultos.
