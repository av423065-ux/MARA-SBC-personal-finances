/* Renderiza los resultados del diagnóstico en el dashboard */

/** Retorna la etiqueta traducida para una situación financiera. */
function situacionLabel(key) {
  return i18n.t(`sit.${key}`) || key;
}

const SEMAFORO_COLOR = {
  rojo:     "rojo",
  amarillo: "amarillo",
  verde:    "verde",
  gris:     "gris",
};

/** Actualiza el widget semáforo y el badge de situación. */
function renderSemaforo(diagnosis) {
  const widget = document.getElementById("semaforoWidget");
  const badge  = document.getElementById("situacionBadge");
  const certeza = document.getElementById("certezaVal");

  const color = SEMAFORO_COLOR[diagnosis.semaforo] || "gris";
  widget.className = `semaforo ${color}`;
  badge.className  = `situacion-badge ${color}`;
  badge.textContent = situacionLabel(diagnosis.situacion);
  certeza.textContent = `${diagnosis.nivel_certeza}%`;
}

/** Calcula el estilo de una métrica según su valor y umbral. */
function metricStyle(value, goodThreshold, warnThreshold, higherIsBetter) {
  if (higherIsBetter) {
    if (value >= goodThreshold) return "good";
    if (value >= warnThreshold) return "warn";
    return "danger";
  } else {
    if (value <= goodThreshold) return "good";
    if (value <= warnThreshold) return "warn";
    return "danger";
  }
}

/** Renderiza las tarjetas de métricas clave. */
function renderMetrics(facts) {
  const grid = document.getElementById("metricsGrid");
  const pct  = (v) => `${(v * 100).toFixed(1)}%`;

  const metrics = [
    {
      label: i18n.t("metric.ratio_ahorro.label"),
      value: pct(facts.ratio_ahorro ?? 0),
      ref:   i18n.t("metric.ratio_ahorro.ref"),
      style: metricStyle(facts.ratio_ahorro ?? 0, 0.20, 0.10, true),
    },
    {
      label: i18n.t("metric.gasto_fijo.label"),
      value: pct(facts.ratio_gasto_fijo ?? 0),
      ref:   i18n.t("metric.gasto_fijo.ref"),
      style: metricStyle(facts.ratio_gasto_fijo ?? 0, 0.50, 0.65, false),
    },
    {
      label: i18n.t("metric.dai.label"),
      value: pct(facts.DAI ?? 0),
      ref:   i18n.t("metric.dai.ref"),
      style: metricStyle(facts.DAI ?? 0, 0.20, 0.35, false),
    },
  ];

  grid.innerHTML = metrics.map(m => `
    <div class="metric-card ${m.style}">
      <div class="metric-label">${m.label}</div>
      <div class="metric-value">${m.value}</div>
      <div class="metric-ref">${m.ref}</div>
    </div>
  `).join("");
}

/** Renderiza la lista de recomendaciones. */
function renderRecomendaciones(recs) {
  const list = document.getElementById("recList");
  if (!recs || recs.length === 0) {
    list.innerHTML = `<li style='color:var(--color-muted);font-size:.9rem;'>${i18n.t("dash.no_recs")}</li>`;
    return;
  }

  list.innerHTML = recs.map(r => `
    <li class="rec-item">
      <span class="rec-badge ${r.dominio}">${r.dominio}</span>
      <div class="rec-content">
        <div class="rec-accion">${r.accion}</div>
        <div class="rec-explica">${r.explicacion}</div>
        <button class="btn-explainer" onclick="explainer.toggle('${r.regla_id}', this)">
          ${i18n.t("dash.why")} (${r.regla_id})
        </button>
        <div class="explainer-panel" id="exp-${r.regla_id}"></div>
      </div>
      <span class="rec-certeza">${r.factor_certeza}%</span>
    </li>
  `).join("");
}

/** Punto de entrada principal — renderiza todo el dashboard. */
function renderDashboard(diagnosis) {
  renderSemaforo(diagnosis);
  renderMetrics(diagnosis.hechos_derivados || {});
  renderRecomendaciones(diagnosis.recomendaciones || []);
}
