# Ajustes del Lite oficial (PS EMA LITE), 17-oct-2026

Capturas tomadas en la sesión de Luna (16-17 oct) y guardadas por Claude desde las imágenes compartidas en la conversación. NQ1!, 1 m, ETH, UTC. Instancia «PS EMA LITE» con START 2026-10-12 14:00 y END 14:22.

## Inputs (`01_inputs.png`)

| Sección | Ajuste | Valor |
|---|---|---|
| Manual range | 1. START | 2026-10-12 14:00 |
| | 2. END (candle included) | 2026-10-12 14:22 |
| | Source data resolution | 1 minute |
| | Show PDA (FVG / IFVG / VI) | no |
| Appearance | Theme | Dark |
| EMA colours | Colour 1 / 2 / 3 | cian / magenta / naranja |
| Price projections | Show box-height projections | sí (con icono de ayuda) |

## Style (`02_style.png`, `03_style_precision.png`)

Graphic objects: Boxes, Pane labels, Lines y Polylines activados. Output values: Precision «Default» (opciones Default y 0–8), Labels on price scale y Values in status line activados. Input values: Inputs in status line activado.

## Conclusión para C

Las únicas entradas del Lite que pueden afectar a C son **START, END y la resolución de la fuente**. No hay modo de selección, dirección, tope ni ajuste visibles: el Lite usa valores internos fijos. Que el Lite dibuje Lines y Polylines encaja con que la parte inicial de las curvas no aparezca en la exportación CSV en algunos casos.
