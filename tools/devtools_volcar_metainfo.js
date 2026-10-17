// Volcado de metadatos de los estudios del gráfico activo de TradingView (17-oct-2026).
//
// Se ejecuta en la consola de DevTools (marco superior) con el gráfico abierto.
// Copia al portapapeles un JSON con, por cada estudio: descripción, id, inputs
// (con tooltips, valores por defecto, opciones, ocultos), plots, estilos,
// valores por defecto, pineFeatures y los valores actuales de los inputs.
//
// NO incluye el ILScript (bytecode cifrado del autor): se sustituye por su
// longitud. No se intenta descifrar ni ejecutar nada; solo se leen metadatos
// que el navegador ya tiene para mostrar el panel de ajustes.
(() => {
  const chart = window._exposed_chartWidgetCollection?.activeChartWidget?.value();
  const studies = chart?.model()?.model()?.allStudies() || [];
  const limpiar = (inp) => {
    const copia = { ...inp };
    if (copia.name === "ILScript" || copia.id === "text") {
      copia.defval = `(omitido: ${String(copia.defval || "").length} caracteres)`;
    }
    return copia;
  };
  const salida = studies.map((s, idx) => {
    const meta = s.metaInfo?.() || {};
    let actuales = null;
    try { actuales = s.properties?.().inputs?.state?.() ?? null; } catch (e) { actuales = String(e); }
    if (actuales && actuales.text) actuales.text = "(omitido)";
    let pineFeatures = null;
    try {
      const f = (meta.inputs || []).find((i) => i.id === "pineFeatures")?.defval;
      pineFeatures = f ? JSON.parse(f) : null;
    } catch (e) { pineFeatures = "no se pudo leer"; }
    return {
      indice: idx,
      descripcion: meta.description,
      descripcion_corta: meta.shortDescription,
      id: meta.id,
      version: meta.version,
      pineFeatures,
      inputs: (meta.inputs || []).map(limpiar),
      plots: meta.plots,
      estilos: meta.styles,
      valores_por_defecto: meta.defaults,
      inputs_actuales: actuales,
    };
  });
  const json = JSON.stringify({ volcado_utc: new Date().toISOString(), estudios: salida }, null, 1);
  copy(json);
  console.log(`Copiados ${salida.length} estudios (${json.length} caracteres) al portapapeles.`);
})();
