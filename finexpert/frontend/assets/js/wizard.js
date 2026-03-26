/* Lógica de navegación del wizard y construcción del perfil */

const wizard = (() => {
  let currentStep = 1;
  const TOTAL_STEPS = 4;

  /** Lee el valor de un campo del formulario como float (o 0 si vacío). */
  const num  = (id) => parseFloat(document.getElementById(id)?.value || "0") || 0;
  /** Lee el valor de un campo del formulario como string. */
  const str  = (id) => document.getElementById(id)?.value || "";
  /** Lee el valor de un campo del formulario como boolean. */
  const bool = (id) => document.getElementById(id)?.checked || false;

  /** Construye el objeto de perfil con todos los campos del wizard. */
  function buildProfile() {
    const tasaPct = num("tasa_promedio_anual");
    const rendPct = num("tasa_rendimiento_esperada");
    return {
      // Paso 1
      edad:                       num("edad"),
      estado_civil:               str("estado_civil"),
      num_dependientes:           num("num_dependientes"),
      nivel_educacion_financiera: num("nivel_educacion_financiera"),
      tipo_ingreso:               str("tipo_ingreso"),
      // Paso 2
      ingreso_mensual:            num("ingreso_mensual"),
      gastos_fijos:               num("gastos_fijos"),
      gastos_variables:           num("gastos_variables"),
      pago_mensual_deudas:        num("pago_mensual_deudas"),
      deuda_total:                num("deuda_total"),
      tasa_promedio_anual:        tasaPct > 1 ? tasaPct / 100 : tasaPct,
      num_creditos:               num("num_creditos"),
      tiene_tarjeta_credito:      bool("tiene_tarjeta_credito"),
      paga_minimo_tarjeta:        bool("paga_minimo_tarjeta"),
      tiene_hipoteca:             bool("tiene_hipoteca"),
      tiene_credito_nomina:       bool("tiene_credito_nomina"),
      tiene_deuda_tasa_variable:  bool("tiene_deuda_tasa_variable"),
      usa_credito_para_gastos_basicos: bool("usa_credito_para_gastos_basicos"),
      tendencia_tasas:            str("tendencia_tasas"),
      // Paso 3
      meses_fondo_emergencia:     num("meses_fondo_emergencia"),
      capital_disponible:         num("capital_disponible"),
      num_instrumentos:           num("num_instrumentos"),
      tasa_rendimiento_esperada:  rendPct > 1 ? rendPct / 100 : rendPct,
      ahorro_automatico:          bool("ahorro_automatico"),
      lleva_registro_gastos:      bool("lleva_registro_gastos"),
      paga_ISR:                   bool("paga_ISR"),
      objetivo_principal:         str("objetivo_principal"),
      horizonte_temporal:         num("horizonte_temporal"),
      meta_monto:                 num("meta_monto"),
      meses_deficit:              num("meses_deficit"),
      tendencia_gasto:            str("tendencia_gasto"),
      tendencia_ahorro:           str("tendencia_ahorro"),
      cambio_habitos:             bool("cambio_habitos"),
      mes_alto_gasto:             bool("mes_alto_gasto"),
      reserva_impuestos:          bool("reserva_impuestos"),
      pago_extra_deuda:           bool("pago_extra_deuda_check") ? 1 : 0,
    };
  }

  /** Valida el paso actual antes de avanzar; devuelve lista de errores. */
  function validateStep(step) {
    const errs = [];

    if (step === 1) {
      const edad = Math.trunc(num("edad"));
      if (edad < 18 || edad > 99)
        errs.push(i18n.t("err.age"));
      const dep = num("num_dependientes");
      if (dep < 0 || dep > 10)
        errs.push(i18n.t("err.dependents"));
    }

    if (step === 2) {
      if (num("ingreso_mensual") <= 0)
        errs.push(i18n.t("err.no_income"));
      if (num("gastos_fijos") < 0 || num("gastos_variables") < 0)
        errs.push(i18n.t("err.neg_expenses"));
      const tasa = num("tasa_promedio_anual");
      if (tasa < 0 || tasa > 200)
        errs.push(i18n.t("err.rate"));
    }

    if (step === 3) {
      const horizonte = Math.trunc(num("horizonte_temporal"));
      if (horizonte < 1 || horizonte > 600)
        errs.push(i18n.t("err.horizon"));
      const fondo = num("meses_fondo_emergencia");
      if (fondo < 0 || fondo > 36)
        errs.push(i18n.t("err.emergency_months"));
    }

    return errs;
  }

  /** Muestra u oculta el alerta de error. */
  function showError(msg) {
    const el = document.getElementById("errorAlert");
    if (!msg) { el.style.display = "none"; return; }
    el.textContent = msg;
    el.style.display = "block";
  }

  /** Activa visualmente el paso indicado en la barra de progreso. */
  function updateProgress(step) {
    document.querySelectorAll(".step-item").forEach((el, idx) => {
      const n = idx + 1;
      el.classList.toggle("active",    n === step);
      el.classList.toggle("completed", n < step);
    });
    // Resetear número en círculos de pasos completados (muestran ✓ vía CSS)
    document.querySelectorAll(".step-circle").forEach((el, idx) => {
      if (idx + 1 >= step) el.textContent = idx + 1;
      else el.textContent = "";
    });
  }

  /** Muestra el paso indicado y oculta los demás. */
  function showStep(step) {
    document.querySelectorAll(".wizard-step").forEach((el, idx) => {
      el.classList.toggle("active", idx + 1 === step);
    });
    updateProgress(step);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /** Avanza al siguiente paso (con validación). */
  function next() {
    showError("");
    const errs = validateStep(currentStep);
    if (errs.length) { showError(errs[0]); return; }
    if (currentStep < TOTAL_STEPS - 1) {
      currentStep++;
      showStep(currentStep);
    }
  }

  /** Retrocede al paso anterior. */
  function prev() {
    showError("");
    if (currentStep > 1) {
      currentStep--;
      showStep(currentStep);
    }
  }

  /** Envía el formulario y llama a la API. */
  async function submit() {
    showError("");
    const errs = validateStep(currentStep);
    if (errs.length) { showError(errs[0]); return; }

    const btn = document.getElementById("btnDiagnosticar");
    btn.innerHTML = `<span class="spinner"></span> ${i18n.t("btn.loading")}`;
    btn.disabled = true;

    try {
      const profile = buildProfile();
      const diagnosis = await fetchDiagnosis(profile);

      // Guardar perfil para el explainer
      explainer.setProfile(profile);

      // Ir al paso 4 y renderizar
      currentStep = TOTAL_STEPS;
      showStep(currentStep);
      renderDashboard(diagnosis);
      renderChart(diagnosis.proyeccion_6m || []);
    } catch (err) {
      showError(`${i18n.t("err.api")} ${err.message}`);
    } finally {
      btn.innerHTML = i18n.t("btn.diagnose");
      btn.disabled = false;
    }
  }

  /** Reinicia el wizard al paso 1. */
  function reset() {
    currentStep = 1;
    showStep(1);
    showError("");
  }

  return { next, prev, submit, reset };
})();
