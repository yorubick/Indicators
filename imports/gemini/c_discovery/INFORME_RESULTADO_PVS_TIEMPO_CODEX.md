# Informe Técnico: Verificación del Motor de Curvas y Prueba de Invarianza de Extremos de Precio en PoiSzn Lite v1.3

**Para:** Codex / Auditoría Matemática y de Código  
**Fecha:** 14 de octubre de 2026  
**Entorno de Validación:** TradingView en vivo (`CME_MINI:NQ1!`, 1m, UTC) y replicación analítica en Python contra `Lite_1903_192300_1m_b.csv`.  

---

## 1. Validación del Motor de Curvas (100% Resuelto y Reproducido al Céntimo)

Se implementó el emulador de ingeniería inversa en **Pine Script v5** (`PoiSzn Lab`) y se contrastó en tiempo real contra el indicador oficial **PoiSzn EMA Origin Lite v1.3**.

### Especificación Operacional Demostrada:
1. **Recurrencia Exponencial Continua:**
   $$\alpha_k = \frac{2}{\frac{b_0 \cdot C}{\Delta} + 1}$$
   donde $\Delta$ es la resolución en segundos y $b_0$ son las bases de tiempo exactas por unidad de $C$:
   * **Lane A (Divisor 3):** Fast = $24.0$ ($72/3$), Slow = $89/3 \approx 29.6667$
   * **Lane B (Divisor 9):** Fast = $8.0$ ($72/9$), Slow = $89/9 \approx 9.8889$
   * **Lane C (Divisor 27):** Fast = $72/27 \approx 2.6667$, Slow = $89/27 \approx 3.2963$

2. **Captura de Semilla y Disparo de Visibilidad:**
   * La memoria recursiva corre en paralelo tras la barra exacta de `END`: una rama inicializada con el `Low` de la barra `END` (hipótesis alcista) y otra con el `High` de `END` (hipótesis bajista).
   * Las curvas permanecen ocultas hasta la **primera vela posterior a `END` que cierra fuera del rango** $[L_{\text{rango}}, H_{\text{rango}}]$.
   * Si rompe al alza (`Close > High`), se proyecta la rama con semilla `Low` de `END`. Si rompe a la baja, la rama con semilla `High` de `END`.

### Contrastes en Vivo en TradingView (Vela 12-oct 19:26 UTC, NQ1! 1m):
* **Caso 1 (START 19:03, END 19:23, C = 50):**  
  * Lane 3 A/B: `30,865.83` / `30,865.56` (Error: **0.00**)  
  * Lane 2 A/B: `30,868.02` / `30,867.50` (Error: **0.00**)  
  * Lane 1 A/B: `30,870.90` / `30,870.38` (Error: **0.00**)
* **Caso 2 (START 19:03, END 19:24, C = 52):**  
  * Lane 3 A/B: `30,867.03` / `30,866.89` (Error: **0.00**)  
  * Lane 2 A/B: `30,868.30` / `30,867.97` (Error: **0.00**)  
  * Lane 1 A/B: `30,870.62` / `30,870.12` (Error: **0.00**)
* **Caso 3 (START 19:03, END 19:25, C = 71):**  
  * Lane 3 A/B: `30,867.37` / `30,867.30` (Error: **0.00**)  
  * Lane 2 A/B: `30,868.05` / `30,867.87` (Error: **0.00**)  
  * Lane 1 A/B: `30,869.65` / `30,869.24` (Error: **0.00**)

---

## 2. Experimento Controlado: Desacoplamiento Tiempo vs. Mechas de Precio

Para evaluar si el salto de $C$ está determinado por la mecha/extremo de precio de las velas entrantes o por la escala temporal acumulada, se analizó el barrido retrospectivo de `START` manteniendo **fijo el `END` en 19:23:00 UTC** (resolución 60s):

| START UTC | END UTC | Velas ($n$) | Duración ($T$) | High Rango | Low Rango | Rango ($H - L$) | $C$ Oficial |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **19:03:00** | 19:23:00 | $n = 21$ | $1260\text{ s}$ | `30,870.75` | `30,849.00` | **21.75 ptos** | **$50$** |
| **19:02:00** | 19:23:00 | $n = 22$ | $1320\text{ s}$ | `30,870.75` | `30,849.00` | **21.75 ptos** | **$52$** |
| **19:01:00** | 19:23:00 | $n = 23$ | $1380\text{ s}$ | `30,870.75` | `30,849.00` | **21.75 ptos** | **$77$** |

### Observaciones Físicas:
1. Las velas de las 19:02 (`H: 30862.75, L: 30857.50`) y 19:01 (`H: 30863.50, L: 30852.00`) están **estrictamente contenidas dentro del rango previo**.
2. **El High, el Low y la amplitud total del rango son 100% idénticos en los tres casos (21.75 puntos)**.
3. A pesar de que los extremos y la amplitud de precio no variaron en lo absoluto, **$C$ varió de $50 \to 52 \to 77$**.
4. La magnitud del salto entre $n=21$ y $n=23$ es exactamente **$77 - 50 = 27 = 3^3$** (la potencia cúbica del divisor fractal de la capa C).

---

## 3. Auditoría Crítica y Preguntas Abiertas (Por qué NO es "así de sencillo")

Compartimos la sospecha escéptica: **un salto armónico de $+27$ describe la distancia entre niveles, pero NO explica qué condición interna dispara la transición**.

### Hechos que refutan un modelo puramente lineal o puramente temporal:
1. **Déficit respecto al tiempo continuo:**
   * En $n = 21$: $\frac{1260\text{ s}}{18.3} = 68.85$, pero $C = 50$ (déficit de $-18.85\text{ s}$).
   * En $n = 22$: $\frac{1320\text{ s}}{18.3} = 72.13$, pero $C = 52$ (déficit de $-20.13\text{ s}$).
   * En $n = 23$: $\frac{1380\text{ s}}{18.3} = 75.41$, y $C$ salta bruscamente a $77$ (exceso de $+1.59\text{ s}$).
   * ¿Por qué el estado colapsa a la meseta $C \approx 50..52$ en $n=21, 22$ y "despierta" a la escala macroscópica de $\approx 77$ justo en $n=23$?
2. **Colisiones formales previas:**
   * En 15 segundos, `START 19:03:15` da $C = 88$ y `START 19:03:30` da $C = 61$ con el mismo `END 19:23:45`, compartiendo 76 velas idénticas con los mismos extremos globales.
   * La diferencia $88 - 61 = 27$ vuelve a ser exactamente $3^3$.

### Pregunta Específica para Codex:
Dado que el motor de curvas y la independencia de la amplitud del rango están empíricamente demostrados al céntimo en TradingView, **¿cuál es la condición necesaria y suficiente en Pine Script que hace bifurcar el estado entre los armónicos $C_{\text{base}} \pm k \cdot 27$ cuando el rango de precio no cambia?**
