/* Panel ¿Por qué? — muestra la explicación de cada regla disparada */

const explainer = (() => {
  // Perfil actual almacenado para llamadas a /explain
  let _currentProfile = null;

  /** Almacena el perfil para poder llamar a /explain bajo demanda. */
  function setProfile(profile) {
    _currentProfile = profile;
  }

  /**
   * Alterna el panel de explicación de una regla.
   * Si ya está abierto, lo cierra; si no, llama a la API y lo abre.
   */
  async function toggle(reglaId, btnEl) {
    const panel = document.getElementById(`exp-${reglaId}`);
    if (!panel) return;

    if (panel.classList.contains("open")) {
      panel.classList.remove("open");
      btnEl.textContent = `¿Por qué? (${reglaId})`;
      return;
    }

    btnEl.textContent = "Cargando…";
    btnEl.disabled = true;

    try {
      const data = await fetchExplain(_currentProfile, reglaId);
      const detalle = data.regla_detalle;
      if (detalle) {
        const hechos = Object.entries(detalle.hechos || {})
          .map(([k, v]) => `<strong>${k}</strong> = ${v}`)
          .join(", ") || "—";
        panel.innerHTML = `
          <strong>${detalle.descripcion || detalle.regla}</strong><br/>
          <em>Dominio:</em> ${detalle.dominio} &nbsp;|&nbsp; <em>Certeza:</em> ${detalle.certeza}<br/>
          <em>Hechos activadores:</em> ${hechos}<br/>
          <em>Explicación:</em> ${detalle.explicacion}
        `;
      } else {
        panel.innerHTML = `<em>No se encontró detalle para ${reglaId}.</em>`;
      }
      panel.classList.add("open");
      btnEl.textContent = `Cerrar (${reglaId})`;
    } catch (err) {
      panel.innerHTML = `<em>Error: ${err.message}</em>`;
      panel.classList.add("open");
      btnEl.textContent = `¿Por qué? (${reglaId})`;
    } finally {
      btnEl.disabled = false;
    }
  }

  return { setProfile, toggle };
})();
