/* Módulo de internacionalización ES/EN para MARA */

const TRANSLATIONS = {
  es: {
    /* App */
    "app.subtitle": "Monitor y Asesor de Finanzas Personales y Ahorro",
    "app.results_lang_note": "",

    /* Progress steps */
    "step.label.1": "Perfil",
    "step.label.2": "Finanzas",
    "step.label.3": "Metas",
    "step.label.4": "Diagnóstico",
    "step.counter.1": "Paso 1 de 4",
    "step.counter.2": "Paso 2 de 4",
    "step.counter.3": "Paso 3 de 4",

    /* Step 1 */
    "s1.title":    "Perfil personal",
    "s1.subtitle": "Cuéntanos un poco sobre ti para personalizar el diagnóstico.",
    "s1.age":      "Edad",
    "s1.marital":  "Estado civil",
    "s1.m.single":    "Soltero/a",
    "s1.m.married":   "Casado/a",
    "s1.m.divorced":  "Divorciado/a",
    "s1.m.widowed":   "Viudo/a",
    "s1.dependents":       "Número de dependientes",
    "s1.dependents.hint":  "Personas que dependen económicamente de ti",
    "s1.edu":    "Educación financiera (1-5)",
    "s1.edu.1":  "1 – Básica (no conozco mucho)",
    "s1.edu.2":  "2 – Media-baja",
    "s1.edu.3":  "3 – Media",
    "s1.edu.4":  "4 – Media-alta",
    "s1.edu.5":  "5 – Avanzada",
    "s1.income_type": "Tipo de ingreso",
    "s1.i.fixed":    "Fijo (empleado, salario)",
    "s1.i.variable": "Variable (freelance, comisiones, negocio)",

    /* Step 2 */
    "s2.title":    "Ingresos, gastos y deudas",
    "s2.subtitle": "Usa tus promedios mensuales en pesos mexicanos (MXN).",
    "s2.sec.income": "Ingresos",
    "s2.sec.expenses": "Gastos",
    "s2.sec.debts": "Deudas",
    "s2.sec.debt_status": "Situación de deuda",
    "s2.income":       "Ingreso mensual neto ($)",
    "s2.income.hint":  "Lo que recibes después de impuestos y deducciones",
    "s2.income.ph":    "Ej: 15000",
    "s2.fixed_exp":      "Gastos fijos mensuales ($)",
    "s2.fixed_exp.hint": "Renta, servicios, transporte fijo",
    "s2.fixed_exp.ph":   "Ej: 7000",
    "s2.var_exp":      "Gastos variables mensuales ($)",
    "s2.var_exp.hint": "Alimentación, entretenimiento, ropa",
    "s2.var_exp.ph":   "Ej: 3000",
    "s2.debt_pay":      "Pago mensual de deudas ($)",
    "s2.debt_pay.hint": "Suma de todos tus pagos mensuales de créditos",
    "s2.debt_pay.ph":   "Ej: 2500",
    "s2.debt_total":    "Deuda total acumulada ($)",
    "s2.debt_total.ph": "Ej: 50000",
    "s2.rate":       "Tasa de interés promedio anual (%)",
    "s2.rate.hint":  "Ingresa el porcentaje (ej: 28 para 28%)",
    "s2.rate.ph":    "Ej: 28",
    "s2.credits":    "Número de créditos activos",
    "s2.has_card":      "Tengo tarjeta(s) de crédito",
    "s2.pays_min":      "Solo pago el mínimo de mi(s) tarjeta(s)",
    "s2.has_mortgage":  "Tengo hipoteca (crédito de vivienda)",
    "s2.has_payroll":   "Tengo crédito de nómina",
    "s2.variable_rate": "Alguna deuda tiene tasa variable",
    "s2.credit_basics": "Uso crédito para pagar gastos básicos",

    /* Step 3 */
    "s3.title":    "Ahorro, metas e inversión",
    "s3.subtitle": "Esta información define tu perfil de riesgo y pronóstico financiero.",
    "s3.sec.savings": "Situación de ahorro",
    "s3.sec.goal":    "Meta financiera",
    "s3.sec.trends":  "Tendencias y hábitos",
    "s3.emergency":      "Fondo de emergencia (meses)",
    "s3.emergency.hint": "Meses de gastos cubiertos si perdieras el ingreso",
    "s3.capital":      "Capital disponible para invertir ($)",
    "s3.capital.hint": "Ahorro acumulado disponible, no el fondo de emergencia",
    "s3.instruments":      "Instrumentos de inversión activos",
    "s3.instruments.hint": "CETES, fondos, acciones, etc.",
    "s3.return":   "Rendimiento esperado anual (%)",
    "s3.auto_save":  "Tengo ahorro automático configurado",
    "s3.tracks_exp": "Llevo registro de mis gastos",
    "s3.pays_isr":   "Considero el ISR en mis inversiones",
    "s3.goal_type":  "Objetivo principal",
    "s3.g.savings":    "Crear fondo de emergencia",
    "s3.g.debt":       "Liquidar deudas",
    "s3.g.invest":     "Empezar a invertir",
    "s3.g.retirement": "Ahorro para el retiro",
    "s3.g.emergency":  "Cubrir una emergencia actual",
    "s3.horizon":      "Horizonte temporal (meses)",
    "s3.goal_amount":  "Monto de la meta ($)",
    "s3.deficit_months":      "Meses con déficit reciente",
    "s3.deficit_months.hint": "Meses recientes en que gastaste más de lo que ganaste",
    "s3.expense_trend": "Tendencia de gastos últimos 3 meses",
    "s3.savings_trend": "Tendencia de ahorro últimos 3 meses",
    "s3.rates_trend":   "Tendencia de tasas de interés",
    "s3.t.stable":      "Estable",
    "s3.t.rising":      "Creciente",
    "s3.t.falling":     "Decreciente",
    "s3.t.rising_exp":  "Creciente (han aumentado)",
    "s3.t.falling_exp": "Decreciente (han bajado)",
    "s3.t.stable_exp":  "Estable (sin cambios)",
    "s3.t.up":   "Alza",
    "s3.t.down": "Baja",
    "s3.changing_habits": "Estoy implementando cambios en mis hábitos financieros",
    "s3.high_month":      "Este mes tuve gastos extraordinarios",
    "s3.tax_reserve":     "Reservo dinero para impuestos (freelance/negocio)",
    "s3.extra_payment":   "Hago pagos extras a mis deudas",

    /* Buttons */
    "btn.next":     "Siguiente →",
    "btn.prev":     "← Anterior",
    "btn.diagnose": "Obtener Diagnóstico",
    "btn.loading":  "Analizando…",
    "btn.reset":    "← Nuevo diagnóstico",

    /* Dashboard */
    "dash.semaforo":       "Semáforo",
    "dash.certainty":      "Certeza del diagnóstico:",
    "dash.recommendations":"Recomendaciones del sistema",
    "dash.no_recs":        "No se generaron recomendaciones.",
    "dash.chart_title":    "Proyección de ahorro acumulado — 6 meses",
    "dash.why":            "¿Por qué?",
    "dash.close":          "Cerrar",
    "dash.loading_why":    "Cargando…",
    "dash.no_detail":      "No se encontró detalle para esta regla.",

    /* Situaciones */
    "sit.critica_extrema": "Situación Crítica Extrema",
    "sit.critica":         "Situación Crítica",
    "sit.en_riesgo":       "En Riesgo",
    "sit.moderada":        "Situación Moderada",
    "sit.saludable":       "Situación Saludable",
    "sit.sin_datos":       "Sin Datos Suficientes",

    /* Métricas */
    "metric.ratio_ahorro.label": "Ratio de ahorro",
    "metric.ratio_ahorro.ref":   "Óptimo: ≥ 20%",
    "metric.gasto_fijo.label":   "Gasto fijo / Ingreso",
    "metric.gasto_fijo.ref":     "Saludable: ≤ 50%",
    "metric.dai.label":          "DAI (Deuda/Ingreso)",
    "metric.dai.ref":            "Saludable: ≤ 20%",

    /* Errores */
    "err.no_body":   "Se requiere un perfil financiero.",
    "err.no_income": "El ingreso mensual debe ser mayor a cero.",
    "err.api":       "Error al obtener el diagnóstico:",

    /* Chart */
    "chart.today":         "Hoy",
    "chart.month":         "Mes",
    "chart.dataset_label": "Ahorro acumulado proyectado ($)",

    /* Errores adicionales */
    "err.neg_expenses":     "Los gastos no pueden ser negativos.",
    "err.age":              "La edad debe estar entre 18 y 99 años.",
    "err.dependents":       "El número de dependientes debe ser entre 0 y 10.",
    "err.rate":             "La tasa de interés debe estar entre 0 y 200%.",
    "err.horizon":          "El horizonte temporal debe estar entre 1 y 600 meses.",
    "err.emergency_months": "El fondo de emergencia debe estar entre 0 y 36 meses.",

    /* Controls */
    "ctrl.theme_light": "Cambiar a modo oscuro",
    "ctrl.theme_dark":  "Cambiar a modo claro",
  },

  en: {
    /* App */
    "app.subtitle": "Personal Finance Monitor and Advisor",
    "app.results_lang_note": "Recommendations are provided in Spanish by the knowledge engine.",

    /* Progress steps */
    "step.label.1": "Profile",
    "step.label.2": "Finances",
    "step.label.3": "Goals",
    "step.label.4": "Diagnosis",
    "step.counter.1": "Step 1 of 4",
    "step.counter.2": "Step 2 of 4",
    "step.counter.3": "Step 3 of 4",

    /* Step 1 */
    "s1.title":    "Personal Profile",
    "s1.subtitle": "Tell us a bit about yourself to personalize the diagnosis.",
    "s1.age":      "Age",
    "s1.marital":  "Marital status",
    "s1.m.single":    "Single",
    "s1.m.married":   "Married",
    "s1.m.divorced":  "Divorced",
    "s1.m.widowed":   "Widowed",
    "s1.dependents":       "Number of dependents",
    "s1.dependents.hint":  "People who financially depend on you",
    "s1.edu":    "Financial literacy (1-5)",
    "s1.edu.1":  "1 – Basic (I don't know much)",
    "s1.edu.2":  "2 – Below average",
    "s1.edu.3":  "3 – Average",
    "s1.edu.4":  "4 – Above average",
    "s1.edu.5":  "5 – Advanced",
    "s1.income_type": "Income type",
    "s1.i.fixed":    "Fixed (employee, salary)",
    "s1.i.variable": "Variable (freelance, commissions, business)",

    /* Step 2 */
    "s2.title":    "Income, Expenses & Debt",
    "s2.subtitle": "Use your monthly averages in Mexican pesos (MXN).",
    "s2.sec.income": "Income",
    "s2.sec.expenses": "Expenses",
    "s2.sec.debts": "Debt",
    "s2.sec.debt_status": "Debt situation",
    "s2.income":       "Monthly net income ($)",
    "s2.income.hint":  "What you receive after taxes and deductions",
    "s2.income.ph":    "e.g. 15000",
    "s2.fixed_exp":      "Monthly fixed expenses ($)",
    "s2.fixed_exp.hint": "Rent, utilities, fixed transport",
    "s2.fixed_exp.ph":   "e.g. 7000",
    "s2.var_exp":      "Monthly variable expenses ($)",
    "s2.var_exp.hint": "Food, entertainment, clothing",
    "s2.var_exp.ph":   "e.g. 3000",
    "s2.debt_pay":      "Monthly debt payments ($)",
    "s2.debt_pay.hint": "Sum of all your monthly loan payments",
    "s2.debt_pay.ph":   "e.g. 2500",
    "s2.debt_total":    "Total accumulated debt ($)",
    "s2.debt_total.ph": "e.g. 50000",
    "s2.rate":       "Average annual interest rate (%)",
    "s2.rate.hint":  "Enter as a percentage (e.g. 28 for 28%)",
    "s2.rate.ph":    "e.g. 28",
    "s2.credits":    "Number of active credit accounts",
    "s2.has_card":      "I have credit card(s)",
    "s2.pays_min":      "I only pay the minimum on my card(s)",
    "s2.has_mortgage":  "I have a mortgage",
    "s2.has_payroll":   "I have a payroll loan",
    "s2.variable_rate": "Some debt has a variable interest rate",
    "s2.credit_basics": "I use credit to pay for basic necessities",

    /* Step 3 */
    "s3.title":    "Savings, Goals & Investment",
    "s3.subtitle": "This information shapes your risk profile and financial forecast.",
    "s3.sec.savings": "Savings status",
    "s3.sec.goal":    "Financial goal",
    "s3.sec.trends":  "Trends & habits",
    "s3.emergency":      "Emergency fund (months)",
    "s3.emergency.hint": "Months of expenses covered if you lost your income",
    "s3.capital":      "Capital available to invest ($)",
    "s3.capital.hint": "Available savings, not your emergency fund",
    "s3.instruments":      "Active investment vehicles",
    "s3.instruments.hint": "CETES, funds, stocks, etc.",
    "s3.return":   "Expected annual return (%)",
    "s3.auto_save":  "I have automatic savings set up",
    "s3.tracks_exp": "I track my expenses",
    "s3.pays_isr":   "I account for taxes on my investments",
    "s3.goal_type":  "Main goal",
    "s3.g.savings":    "Build an emergency fund",
    "s3.g.debt":       "Pay off debt",
    "s3.g.invest":     "Start investing",
    "s3.g.retirement": "Save for retirement",
    "s3.g.emergency":  "Cover a current emergency",
    "s3.horizon":      "Time horizon (months)",
    "s3.goal_amount":  "Goal amount ($)",
    "s3.deficit_months":      "Months with recent deficit",
    "s3.deficit_months.hint": "Recent months where you spent more than you earned",
    "s3.expense_trend": "Expense trend — last 3 months",
    "s3.savings_trend": "Savings trend — last 3 months",
    "s3.rates_trend":   "Interest rate trend",
    "s3.t.stable":      "Stable",
    "s3.t.rising":      "Rising",
    "s3.t.falling":     "Falling",
    "s3.t.rising_exp":  "Rising (they've increased)",
    "s3.t.falling_exp": "Falling (they've decreased)",
    "s3.t.stable_exp":  "Stable (no changes)",
    "s3.t.up":   "Rising",
    "s3.t.down": "Falling",
    "s3.changing_habits": "I'm implementing changes in my financial habits",
    "s3.high_month":      "This month I had extraordinary expenses",
    "s3.tax_reserve":     "I set aside money for taxes (freelance/business)",
    "s3.extra_payment":   "I make extra payments on my debts",

    /* Buttons */
    "btn.next":     "Next →",
    "btn.prev":     "← Back",
    "btn.diagnose": "Get Diagnosis",
    "btn.loading":  "Analyzing…",
    "btn.reset":    "← New diagnosis",

    /* Dashboard */
    "dash.semaforo":       "Status",
    "dash.certainty":      "Diagnosis certainty:",
    "dash.recommendations":"System Recommendations",
    "dash.no_recs":        "No recommendations were generated.",
    "dash.chart_title":    "Projected cumulative savings — 6 months",
    "dash.why":            "Why?",
    "dash.close":          "Close",
    "dash.loading_why":    "Loading…",
    "dash.no_detail":      "No detail found for this rule.",

    /* Situaciones */
    "sit.critica_extrema": "Extreme Critical Situation",
    "sit.critica":         "Critical Situation",
    "sit.en_riesgo":       "At Risk",
    "sit.moderada":        "Moderate Situation",
    "sit.saludable":       "Healthy Finances",
    "sit.sin_datos":       "Insufficient Data",

    /* Métricas */
    "metric.ratio_ahorro.label": "Savings ratio",
    "metric.ratio_ahorro.ref":   "Optimal: ≥ 20%",
    "metric.gasto_fijo.label":   "Fixed expense / Income",
    "metric.gasto_fijo.ref":     "Healthy: ≤ 50%",
    "metric.dai.label":          "DTI (Debt/Income)",
    "metric.dai.ref":            "Healthy: ≤ 20%",

    /* Errores */
    "err.no_body":   "A financial profile is required.",
    "err.no_income": "Monthly income must be greater than zero.",
    "err.api":       "Error fetching diagnosis:",

    /* Chart */
    "chart.today":         "Today",
    "chart.month":         "Month",
    "chart.dataset_label": "Projected cumulative savings ($)",

    /* Errores adicionales */
    "err.neg_expenses":     "Expenses cannot be negative.",
    "err.age":              "Age must be between 18 and 99.",
    "err.dependents":       "Number of dependents must be between 0 and 10.",
    "err.rate":             "Interest rate must be between 0 and 200%.",
    "err.horizon":          "Time horizon must be between 1 and 600 months.",
    "err.emergency_months": "Emergency fund must be between 0 and 36 months.",

    /* Controls */
    "ctrl.theme_light": "Switch to dark mode",
    "ctrl.theme_dark":  "Switch to light mode",
  },
};

const i18n = (() => {
  let _lang = localStorage.getItem("mara-lang") || "es";

  /** Retorna la traducción para una clave, con soporte de fallback a ES. */
  function t(key) {
    return TRANSLATIONS[_lang]?.[key] ?? TRANSLATIONS["es"]?.[key] ?? key;
  }

  /** Aplica todas las traducciones al DOM. */
  function applyTranslations() {
    document.documentElement.lang = _lang;

    document.querySelectorAll("[data-i18n]").forEach(el => {
      el.textContent = t(el.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(el => {
      el.placeholder = t(el.dataset.i18nPh);
    });
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
      el.title = t(el.dataset.i18nTitle);
    });

    // Nota de idioma en el dashboard (solo visible en EN)
    const note = document.getElementById("langNote");
    if (note) {
      const text = t("app.results_lang_note");
      note.textContent = text;
      note.style.display = text ? "block" : "none";
    }

    // Sincronizar botones de idioma
    document.querySelectorAll(".lang-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.lang === _lang);
    });
  }

  /** Cambia el idioma y aplica. */
  function setLang(lang) {
    _lang = lang;
    localStorage.setItem("mara-lang", lang);
    applyTranslations();
  }

  /** Devuelve el idioma activo. */
  function get() { return _lang; }

  return { t, setLang, applyTranslations, get };
})();
