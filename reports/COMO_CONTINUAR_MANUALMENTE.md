# Investigación PoiSzn: ubicación y trabajo manual

Proyecto general: `G:\trading`. Esta investigación concreta está en **`G:\trading\guias\analisis`**. Otras carpetas del proyecto general corresponden a trabajos diferentes.

## Por dónde empezar

- `C_PRUEBAS_15_SEGUNDOS.md`: informe acumulado de pruebas y enlaces a los informes posteriores.
- `PUNTO_1_PERIODOS_Y_ANCLA.md`: familia EMA y ancla ya reconstruidas.
- `OBTENCION_C.md`: diferencia entre extraer C del indicador original y generar C solo con OHLC.
- `C_BARRIDO_AMPLIADO.md`: mediciones repetidas y problema de exportación durante recálculo.
- `C_GIROS_INTERNOS.md` y `C_BALANCE_RECORRIDO.md`: últimas familias de hipótesis contrastadas.

Los `.csv` conservan exportaciones de TradingView; los `.json`, resultados y metadatos; los `.py`, análisis reproducibles; los `.jpg`/`.png`, evidencia visual. Algunos archivos son diagnósticos inválidos o incompletos. No uses todo el directorio como un conjunto de datos automáticamente: cada informe indica qué archivos fueron aceptados y cuáles se excluyeron.

Las dos guías descargadas están un nivel arriba: `G:\trading\guias\Character-Tree-081026.mp4` y `Auto-Zoom-081026.mp4`. El procedimiento de descarga está en `DESCARGAR_VIDEOS_WHOP.md`. Los modelos y herramientas auxiliares están en `G:\trading\.tools`.

## Medición manual de C

1. En TradingView utiliza el layout de investigación `EMA - investigacion PoiSzn`. Trabaja con Character Tree v6.5.36, perfil B y modo Manual. Mantén esa versión para comparar con estas mediciones.
2. Elige símbolo, fecha, START y END; anota todo. Usa una zona horaria explícita, preferentemente UTC. La referencia es NQ1!, ETH, sin ajuste de contratos, 12 octubre 2026, START 18:55:00 UTC y END 19:20:00 UTC.
3. En `Manual data resolution` selecciona `Chart` y usa inicialmente gráfico de un minuto. Activa `Show extra EMA clouds` para tener las diez curvas. El extractor requiere que fuente y gráfico coincidan y no está validado para Auto Balanced.
4. Visita START y END para cargar el historial. Debe haber OHLC para todo el rango y suficientes curvas posteriores a la ruptura. Al menos cinco pares consecutivos por cada curva; es preferible conservar más.
5. Tras cambiar las anclas, deja que termine el recálculo. La caja y los inputs pueden actualizarse antes que las EMAs. Comprueba las anclas aplicadas y las etiquetas de la familia. En subminuto, los campos de hora pueden recortar segundos: verifica el timestamp exacto del control azul del gráfico.
6. Abre la flecha de `Manage layouts`, junto al nombre del layout, y elige `Download chart data`; descarga el CSV con los plots del indicador. Guarda un nombre único dentro de `G:\trading\guias\analisis\manual`. No sobrescribas las exportaciones de las pruebas anteriores.
7. Sin cambiar los inputs, repite la descarga después de completar el recálculo. Guarda una captura de las anclas y ajustes. Para comprobar el procedimiento, la referencia anterior debe dar C entero compatible = 62. Dos exportaciones iguales hechas demasiado pronto todavía podrían ser del rango anterior.
8. Ejecuta el extractor de abajo y conserva el JSON de ambas descargas. Comprueba que períodos e intervalo de C coincidan. Anota la medición junto con sus nombres de archivo.

## Ejecutar el extractor en PowerShell

Este script solo necesita la biblioteca estándar de Python. Puede usarse el Python que ya está instalado para este proyecto:

```powershell
Set-Location 'G:\trading'
$researchPython = 'C:\Users\PC\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $researchPython '.\guias\analisis\obtener_C.py' '.\guias\analisis\C_referencia_restaurada_barrido.csv'
```

Para tu propio archivo, cambia únicamente el último argumento por la ruta de tu CSV. Ejemplo con un nombre que debes sustituir por el de tu exportación:

```powershell
& $researchPython '.\guias\analisis\obtener_C.py' '.\guias\analisis\manual\mi_medicion_01.csv'
```

El resultado muestra `C_seconds_interval`, `compatible_integer_C_seconds`, los diez `periods`, la cantidad de pares y el error del ajuste. Un entero compatible único no demuestra que el cálculo interno siempre utilice enteros.

Si el extractor falla, conserva el error. Puede faltar historial o curvas, haber fuentes distintas, un recálculo en curso o un modo fuera del alcance comprobado. No conviertas el error en una medición de C ni fuerces un ajuste aproximado.

## Registro mínimo de cada prueba

Copiar este bloque a un archivo nuevo dentro de `manual`, con la fecha y un identificador único:

```text
ID:
Fecha de la medición:
Símbolo / sesión / ajuste de contratos:
Versión del indicador / perfil / modo:
Zona horaria:
START (fecha y HH:MM:SS):
END (fecha y HH:MM:SS):
Resolución del gráfico y fuente:
Único parámetro cambiado respecto al control:
CSV inicial / repetición / captura:
OHLC completo en el rango: sí/no/no comprobado
Intervalo C / enteros compatibles / períodos:
Control de referencia reproducido:
Observación e hipótesis que se pone a prueba:
```

Si hacemos pruebas simultáneamente, usa una copia del layout para tus mediciones. Dos personas cambiando el mismo gráfico pueden mezclar las anclas y los archivos. Mis análisis locales de los CSV ya guardados pueden continuar mientras trabajas en tu copia.

## Estado real

Podemos extraer C de los plots originales y reproducir la familia EMA cuando se proporciona C. **Todavía no se identificó la fórmula que genera C únicamente desde el rango OHLC.** Los análisis nuevos sirven para contrastar reglas concretas, no como una réplica terminada.
