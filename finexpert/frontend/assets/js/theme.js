/* Módulo de tema claro/oscuro para MARA */

const theme = (() => {
  let _current = localStorage.getItem("mara-theme") || "light";

  /** Aplica el tema al documento y actualiza el botón. */
  function apply(t) {
    document.documentElement.setAttribute("data-theme", t);
    const btn = document.getElementById("btnTheme");
    if (!btn) return;
    btn.textContent = t === "dark" ? "☀" : "☾";
    // Actualizar tooltip si i18n ya está disponible
    if (typeof i18n !== "undefined") {
      btn.title = i18n.t(t === "dark" ? "ctrl.theme_dark" : "ctrl.theme_light");
    }
  }

  /** Establece el tema y lo persiste. */
  function setTheme(t) {
    _current = t;
    localStorage.setItem("mara-theme", t);
    apply(t);
  }

  /** Alterna entre claro y oscuro. */
  function toggle() {
    setTheme(_current === "dark" ? "light" : "dark");
  }

  /** Devuelve el tema activo. */
  function get() { return _current; }

  // Aplicar en carga para evitar flash
  apply(_current);

  return { setTheme, toggle, get };
})();
