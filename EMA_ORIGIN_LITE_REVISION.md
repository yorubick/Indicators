# Revisión de PoiSzn EMA Origin Lite v1.2

13 octubre 2026. Fuente oficial revisada en navegador autenticado:
https://www.tradingview.com/script/B2yVeJKv-PoiSzn-EMA-Origin-Lite-v1-2/

## Hechos publicados

Autor: TCMTrader1. La publicación identifica el indicador como gratuito y de código protegido. La pestaña Source code está deshabilitada; no se dispone del Pine mediante esta publicación.

La descripción presenta dos puntos manuales para delimitar un rango y generar estructuras EMA desde su final. Enumera tres grupos de EMA con colores independientes, resolución de cálculo seleccionable y proyecciones de precio/arrays opcionales. Indica que el rango y la resolución afectan el resultado. No incluye señales de entrada o salida.

La descripción no revela una fórmula de Character/C, períodos numéricos, semilla, criterio de selección de ventana interna ni método de ajuste. El ejemplo visual muestra una caja y nubes que acompañan una caída; una imagen no establece cómo se calculan.

## Utilidad e incertidumbre

Es una posible referencia funcional más simple. No se ha demostrado que comparta el generador de C ni los períodos de Character Tree v6.5.36. Las conclusiones de la investigación previa no deben trasladarse a Lite sin comparar resultados.

La siguiente comparación pertinente sería aplicar ambos al mismo símbolo, sesión, resolución y START/END ya controlados. Exportar los plots disponibles de Lite, recuperar su recurrencia y períodos por separado y compararlos con Character Tree. Si coinciden en varios rangos —incluido el salto 118→67 y el barrido END— Lite podría ayudar a aislar el núcleo de cálculo. Si difieren, debe mantenerse como familia separada.

Esta revisión solo inspeccionó la publicación y su ejemplo. No añadió el indicador, cambió el layout de investigación ni realizó nuevas mediciones. No se accedió a código protegido.
