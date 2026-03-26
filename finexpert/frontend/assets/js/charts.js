/* Gráfica de proyección de ahorro a 6 meses con Chart.js */

let _chartInstance = null;

/** Renderiza la gráfica de línea con la proyección de ahorro a 6 meses. */
function renderChart(proyeccion) {
  const ctx = document.getElementById("chartProyeccion");
  if (!ctx || !proyeccion || proyeccion.length === 0) return;

  // Destruir instancia previa si existe (necesario al hacer nuevo diagnóstico)
  if (_chartInstance) {
    _chartInstance.destroy();
    _chartInstance = null;
  }

  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const gridColor  = isDark ? "rgba(255,255,255,0.07)" : "rgba(0,0,0,0.05)";
  const tickColor  = isDark ? "#94a3b8" : "#64748b";
  const todayLabel = i18n.t("chart.today") || "Hoy";
  const labels = proyeccion.map((_, i) => i === 0 ? todayLabel : `${i18n.t("chart.month") || "Mes"} ${i}`);

  _chartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: i18n.t("chart.dataset_label") || "Ahorro acumulado proyectado ($)",
        data: proyeccion,
        borderColor: "#2563eb",
        backgroundColor: "rgba(37,99,235,0.08)",
        borderWidth: 2.5,
        pointBackgroundColor: "#2563eb",
        pointRadius: 4,
        tension: 0.35,
        fill: true,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => ` $${ctx.parsed.y.toLocaleString("es-MX", { minimumFractionDigits: 0 })}`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: (v) => `$${(v / 1000).toFixed(0)}k`,
            font: { size: 11 },
            color: tickColor,
          },
          grid: { color: gridColor },
        },
        x: {
          ticks: { font: { size: 11 }, color: tickColor },
          grid: { display: false },
        },
      },
    },
  });
}
