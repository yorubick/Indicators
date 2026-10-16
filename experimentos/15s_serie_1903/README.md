# Experimento EXP-20261014-1903-15S: Inversión de C con Fuente 15 s en Gráfico 1 m

> **Nota de revisión (16-oct-2026).** Las 13 mediciones e inversiones de este experimento son datos sólidos. La predicción ciega para END 19:36 **no llegó a evaluarse**: la lectura de 19:37 salió vacía porque no hubo ruptura ([CONTROL_1936_EVAL_1937.md](CONTROL_1936_EVAL_1937.md)). Los «hallazgos teóricos» de la sección 4 (escalones armónicos, cinemática intraminuto) son hipótesis formuladas con estos mismos 13 casos. Ver el [estado de la investigación](../../docs/RESEARCH_STATUS.md#revisión-de-afirmaciones-previas).

**Fecha de registro**: 14 de octubre de 2026  
**Identificador**: `EXP-20261014-1903-15S`  
**Estado**: Mediciones primarias e inversión completadas (13/13 confirmadas); predicción ciega para END 19:36 registrada y pendiente de verificación en TradingView.  
**Autores**: FrankyProfit (Pair programming con Antigravity y Luna de GPT-6).  
**Protocolo de referencia**: Cumple con [`docs/CONTRIBUTING.md`](../../docs/CONTRIBUTING.md) y [`docs/RESEARCH_STATUS.md`](../../docs/RESEARCH_STATUS.md).

---

## 1. Contexto y Configuración del Gráfico

- **Activo**: `NQ1!` (CME E-mini NASDAQ 100 Futures, contrato continuo).
- **Sesión**: ETH (Electronic Trading Hours).
- **Zona horaria**: UTC.
- **Ajustes de gráfico**: B-ADJ desactivado, Replay desactivado.
- **Intervalo del gráfico visible**: **1 minuto** (`1m`).
- **Indicador oficial**: `PoiSzn EMA Origin Lite v1.2 / v1.3`.
- **Entradas del indicador**:
  - `1. START`: `2026-10-12 19:03` (UTC).
  - `2. END (candle included)`: Variable de `19:23` a `19:35` (UTC).
  - `Source data resolution`: **`15 seconds`** (`15s`).

---

## 2. Telemetría Primaria Oficial (13 Mediciones)

Lecturas copiadas directamente de la Ventana de Datos de TradingView en la vela de evaluación de 1m indicada:

| n | END | Eval 1m (O / H / L / C) | Lane 3 A | Lane 3 B | Lane 2 A | Lane 2 B | Lane 1 A | Lane 1 B |
|---:|:---:|---|---:|---:|---:|---:|---:|---:|
| 21 | 19:23 | 19:26 · 30,868.75 / 30,873.00 / 30,867.25 / 30,872.50 | 30,864.97 | 30,864.84 | 30,866.12 | 30,865.82 | 30,868.16 | 30,867.73 |
| 22 | 19:24 | 19:26 · 30,868.75 / 30,873.00 / 30,867.25 / 30,872.50 | 30,866.67 | 30,866.59 | 30,867.37 | 30,867.18 | 30,868.74 | 30,868.43 |
| 23 | 19:25 | 19:26 · 30,868.75 / 30,873.00 / 30,867.25 / 30,872.50 | 30,867.16 | 30,867.13 | 30,867.46 | 30,867.38 | 30,868.23 | 30,868.03 |
| 24 | 19:26 | 19:30 · 30,875.25 / 30,877.50 / 30,871.00 / 30,876.50 | 30,868.47 | 30,868.26 | 30,870.30 | 30,869.85 | 30,873.03 | 30,872.50 |
| 25 | 19:27 | 19:30 · 30,875.25 / 30,877.50 / 30,871.00 / 30,876.50 | 30,871.42 | 30,871.35 | 30,872.13 | 30,871.94 | 30,873.52 | 30,873.21 |
| 26 | 19:28 | 19:30 · 30,875.25 / 30,877.50 / 30,871.00 / 30,876.50 | 30,869.92 | 30,869.84 | 30,870.67 | 30,870.47 | 30,872.35 | 30,871.94 |
| 27 | 19:29 | 19:30 · 30,875.25 / 30,877.50 / 30,871.00 / 30,876.50 | 30,870.68 | 30,870.65 | 30,871.03 | 30,870.93 | 30,871.94 | 30,871.69 |
| 28 | 19:30 | 19:32 · 30,874.75 / 30,880.75 / 30,874.50 / 30,879.25 | 30,871.78 | 30,871.64 | 30,873.09 | 30,872.75 | 30,875.60 | 30,875.04 |
| 29 | 19:31 | 19:32 · 30,874.75 / 30,880.75 / 30,874.50 / 30,879.25 | 30,872.59 | 30,872.53 | 30,873.22 | 30,873.04 | 30,874.76 | 30,874.37 |
| 30 | 19:32 | 19:33 · 30,879.25 / 30,886.25 / 30,877.00 / 30,885.75 | 30,874.84 | 30,874.77 | 30,875.47 | 30,875.29 | 30,877.10 | 30,876.67 |
| 31 | 19:33 | 19:34 · 30,886.00 / 30,898.00 / 30,885.75 / 30,897.25 | 30,877.88 | 30,877.71 | 30,879.51 | 30,879.06 | 30,883.53 | 30,882.49 |
| 32 | 19:34 | 19:35 · 30,897.50 / 30,908.00 / 30,895.50 / 30,904.25 | 30,886.45 | 30,886.32 | 30,887.77 | 30,887.40 | 30,891.16 | 30,890.27 |
| 33 | 19:35 | 19:36 · 30,905.00 / 30,911.00 / 30,902.25 / 30,908.25 | 30,896.10 | 30,895.99 | 30,897.22 | 30,896.91 | 30,899.97 | 30,899.26 |

---

## 3. Método de Inversión Numérica de C

- **Modelo**: EMA estándar con $\alpha = \frac{2}{\frac{b_0 \cdot C}{\Delta t} + 1}$, donde $\Delta t = 15.0\text{ s}$ y los coeficientes son:
  - Lane 3 A: $b_0 = 24.0$
  - Lane 3 B: $b_0 = 89/3 \approx 29.6667$
  - Lane 2 A: $b_0 = 8.0$
  - Lane 2 B: $b_0 = 89/9 \approx 9.8889$
  - Lane 1 A: $b_0 = 72/27 = 8/3 \approx 2.6667$
  - Lane 1 B: $b_0 = 89/27 \approx 3.2963$
- **Semilla**: Mínimo de la barra de 1m en END (correspondiente a la mecha opuesta en impulso alcista).
- **Actualizaciones**: 4 cierres nativos de 15s por cada minuto transcurrido entre END y la vela de evaluación.
- **Optimizador**: Raíz univariada de Brent (`scipy.optimize.brentq`) con cota $[5.0, 1500.0]$.

### Resultados Invertidos

| n | END | C 1m previo | C 15s (Entero) | C 15s Media 6 Lanes | Spread Lanes | Residuo Máx. Simulado vs Oficial (pts) |
|---:|:---:|---:|---:|---:|:---:|:---:|
| 21 | 19:23 | 50 | **88** | 87.94 | 0.71 | 0.0036 |
| 22 | 19:24 | 52 | **67** | 66.95 | 0.75 | 0.0029 |
| 23 | 19:25 | 71 | **88** | 87.77 | 0.85 | 0.0038 |
| 24 | 19:26 | 135 | **88** | 87.99 | 0.51 | 0.0049 |
| 25 | 19:27 | 130 | **79** | 79.08 | 1.50 | 0.0050 |
| 26 | 19:28 | 88 | **102** | 102.33 | 1.19 | 0.0045 |
| 27 | 19:29 | 135 | **123** | 122.99 | 3.29 | 0.0049 |
| 28 | 19:30 | 112 | **67** | 67.14 | 0.47 | 0.0046 |
| 29 | 19:31 | 136 | **87** | 86.85 | 1.82 | 0.0049 |
| 30 | 19:32 | 112 | **106** | 105.92 | 2.40 | 0.0046 |
| 31 | 19:33 | 112 | **87** | 87.07 | 0.67 | 0.0047 |
| 32 | 19:34 | 135 | **123** | 123.01 | 0.54 | 0.0041 |
| 33 | 19:35 | 112 | **87** | 87.07 | 0.41 | 0.0043 |

**Conclusión técnica**: En las 13 ventanas, la simulación con el $C_{15\text{s}}$ entero recuperado reproduce las 6 lecturas oficiales con un error estrictamente menor a **0.0050 puntos** ($< 0.5$ centavo).

---

## 4. Hallazgos Teóricos y Cuantización

1. **La resolución de fuente cambia el valor intrínseco de $C$**:
   $C_{15\text{s}} \neq C_{1\text{m}}$. El cálculo de $C$ opera sobre las barras de la fuente elegida.
2. **Escalón armónico en Lane C**:
   El período discreto en Lane C ($N_C = \frac{8}{3} \frac{C}{\Delta t}$) produce:
   $$C = \operatorname{round}\left( N_C \cdot \frac{3 \cdot \Delta t}{8} \right)$$
   - En 1m ($\Delta t = 60\text{ s}$), el escalón unitario es $22.5\text{ s}$:
     $N_C = 5 \implies C = 112$ (Meseta base); $N_C = 6 \implies C = 135$ (Pico).
   - En 15s ($\Delta t = 15\text{ s}$), el escalón unitario es $5.625\text{ s}$:
     $N_C \approx 15.5 \implies C = 87$ (Meseta base); $N_C = 22 \implies C = 123$ (Pico).
3. **Cinemática intraminuto (Hipótesis Luna / FrankyProfit)**:
   - Los picos mayores (19:29 y 19:34) se producen cuando la vela hace nuevo máximo y cierra en el decil superior ($\ge 93\%$) con el máximo del minuto ubicado en la última subbarra (`:45`).
   - Las mesetas (19:31, 19:33, 19:35) sufren pérdida de impulso, mechas superiores de freno o retrocesos internos, manteniendo $C$ en la meseta base de 87 s.

---

## 5. Predicción Ciega Registrada para Falsación

Registrada formalmente el 14-oct-2026 antes de consultar la lectura oficial:

- **Selección**: `START = 19:03 UTC`, `END = 19:36 UTC`, gráfico 1m, fuente oficial 15s.
- **Barra de evaluación**: `19:37 UTC`.
- **Condición evaluada en 19:36**: Rango 8.75 pts, mecha superior de 2.75 pts, retroceso en última subbarra (:45) $\implies$ No cumple condición de expansión.
- **Predicción del modelo**:
  $$\mathbf{C_{15\text{s}}(19:36) = 87\text{ s}}$$
- **Valores predichos de las curvas oficiales en 19:37**:
  - Lane 1 A: **`30,903.32`** (frente a `30,903.05` si fuera pico de 123).
  - Lane 1 B: **`30,903.15`**
  - Lane 2 A: **`30,902.65`**
  - Lane 2 B: **`30,902.58`**
  - Lane 3 A: **`30,902.39`**
  - Lane 3 B: **`30,902.36`**
- **Estado**: Pendiente de lectura en TradingView.
