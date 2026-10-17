// Volcado de los valores en memoria de TODOS los plots de un estudio (17-oct-2026),
// incluidos los que no salen en la exportación CSV (p. ej. el plot_0 sin título
// del Lite). Se ejecuta en la consola de DevTools (marco superior).
//
// Uso: cambia FILTRO si hace falta y ejecuta. Copia al portapapeles un JSON con
// las filas cuyo tiempo está entre DESDE y HASTA (UTC), con todos los valores.
(() => {
  const FILTRO = "PoiSzn EMA Origin Lite";          // parte de la descripción del estudio
  const DESDE = Date.parse("2026-10-16T16:20:00Z");  // ajustar a la ventana medida
  const HASTA = Date.parse("2026-10-16T17:40:00Z");

  const chart = window._exposed_chartWidgetCollection?.activeChartWidget?.value();
  const model = chart?.model()?.model();
  const study = (model?.allStudies() || []).find((s) => s.metaInfo()?.description?.includes(FILTRO));
  if (!study) return console.error("Estudio no encontrado");
  const meta = study.metaInfo();
  const inputs = study.properties?.().inputs?.state?.() || {};
  delete inputs.text;

  // Contenedores conocidos de la serie de datos; se prueba cada uno.
  const candidatos = [
    ["_data._items", study._data?._items],
    ["_data._data", study._data?._data],
    ["data()._items", study.data?.()?._items],
    ["_dataWindowView._data", study._dataWindowView?._data],
  ];
  let origen = null, items = null;
  for (const [nombre, c] of candidatos) {
    if (Array.isArray(c) && c.length) { origen = nombre; items = c; break; }
  }
  if (!items) {
    console.error("No se encontró el buffer. Claves de study._data:", Object.keys(study._data || {}));
    return;
  }
  // Cada elemento suele ser {index, value:[tiempo_s, plot_0, plot_1, ...]}.
  const filas = [];
  for (const it of items) {
    const v = it.value || it;
    const t = Array.isArray(v) ? v[0] * (v[0] < 1e12 ? 1000 : 1) : null;
    if (t !== null && (t < DESDE || t > HASTA)) continue;
    filas.push({ index: it.index, value: v });
  }
  const salida = {
    volcado_utc: new Date().toISOString(),
    estudio: meta.description,
    id: meta.id,
    inputs_actuales: inputs,
    plots: meta.plots,
    titulos: Object.fromEntries(Object.entries(meta.styles || {}).map(([k, s]) => [k, s.title])),
    origen_buffer: origen,
    nota: "value[0] = tiempo (s); value[1..] = plot_0, plot_1, ... en el orden de 'plots'",
    filas,
  };
  copy(JSON.stringify(salida));
  console.log(`Copiadas ${filas.length} filas desde ${origen}. Primera fila:`, filas[0]);
})();
