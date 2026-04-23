/* Chatbot flotante MARA — lógica de UI y comunicación con /chat */

const chatbot = (() => {
  const API_BASE = "http://localhost:5000";

  // Estado de sesión (no persiste entre recargas)
  const history = [];
  let isOpen    = false;
  let isLoading = false;

  // ── Elementos del DOM (se asignan en init) ──────────────────────
  let bubble, window_, messages, input, sendBtn;

  const WELCOME_MSG =
    "¡Hola! Soy el asistente de MARA. Puedes preguntarme cualquier duda sobre finanzas personales, " +
    "interpretar los resultados de tu diagnóstico o pedir orientación sobre ahorro, deuda e inversión.";

  // ── Helpers ─────────────────────────────────────────────────────

  function escapeHtml(str) {
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  function scrollBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  function appendMsg(role, text) {
    const el = document.createElement("div");
    el.className = `chat-msg ${role}`;
    el.textContent = text;
    messages.appendChild(el);
    scrollBottom();
    return el;
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "chat-msg assistant typing";
    el.id = "chatTyping";
    el.innerHTML = "<span></span><span></span><span></span>";
    messages.appendChild(el);
    scrollBottom();
  }

  function hideTyping() {
    const el = document.getElementById("chatTyping");
    if (el) el.remove();
  }

  function setLoading(val) {
    isLoading = val;
    sendBtn.disabled = val;
    input.disabled   = val;
  }

  // ── Contexto del usuario ─────────────────────────────────────────
  function getUserContext() {
    // window.maraContext es asignado por wizard.js al completar el diagnóstico
    return window.maraContext || null;
  }

  // ── Envío de mensajes ────────────────────────────────────────────
  async function sendMessage() {
    const text = input.value.trim();
    if (!text || isLoading) return;

    input.value = "";
    input.style.height = "auto";
    appendMsg("user", text);
    history.push({ role: "user", content: text });

    setLoading(true);
    showTyping();

    try {
      const body = {
        message:      text,
        history:      history.slice(0, -1), // historial anterior al mensaje actual
        user_context: getUserContext(),
      };

      const res = await fetch(`${API_BASE}/chat`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(body),
      });

      const data = await res.json();
      hideTyping();

      if (!res.ok) {
        const errMsg = data.error || `Error ${res.status}`;
        appendMsg("assistant", `⚠️ ${errMsg}`);
        history.pop(); // no guardar en historial si falló
        return;
      }

      const reply = data.reply || "Sin respuesta.";
      appendMsg("assistant", reply);
      history.push({ role: "assistant", content: reply });

      // Limitar historial a 20 mensajes para no crecer indefinidamente
      while (history.length > 20) history.shift();

    } catch (err) {
      hideTyping();
      appendMsg("assistant", "⚠️ No se pudo conectar con el asistente. Verifica que el servidor esté activo.");
      history.pop();
    } finally {
      setLoading(false);
      input.focus();
    }
  }

  // ── Toggle de la ventana ─────────────────────────────────────────
  function open() {
    isOpen = true;
    window_.classList.add("open");
    bubble.setAttribute("aria-expanded", "true");
    bubble.setAttribute("aria-label", "Cerrar asistente");
    // Reemplazar ícono de chat por X
    bubble.innerHTML = `
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>`;
    input.focus();
  }

  function close() {
    isOpen = false;
    window_.classList.remove("open");
    bubble.setAttribute("aria-expanded", "false");
    bubble.setAttribute("aria-label", "Abrir asistente financiero");
    bubble.innerHTML = BUBBLE_ICON;
  }

  function toggle() {
    isOpen ? close() : open();
  }

  // ── Ícono SVG de la burbuja ──────────────────────────────────────
  const BUBBLE_ICON = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>`;

  // ── Inicialización ────────────────────────────────────────────────
  function init() {
    bubble   = document.getElementById("chatBubble");
    window_  = document.getElementById("chatWindow");
    messages = document.getElementById("chatMessages");
    input    = document.getElementById("chatInput");
    sendBtn  = document.getElementById("chatSend");

    if (!bubble || !window_) return; // No está en la página

    // Burbuja — toggle al clic
    bubble.innerHTML = BUBBLE_ICON;
    bubble.addEventListener("click", toggle);

    // Botón cerrar en el header
    const closeBtn = document.getElementById("chatClose");
    if (closeBtn) closeBtn.addEventListener("click", close);

    // Enviar con botón
    sendBtn.addEventListener("click", sendMessage);

    // Enviar con Enter (Shift+Enter = nueva línea)
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

    // Auto-resize del textarea
    input.addEventListener("input", () => {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 100) + "px";
    });

    // Cerrar con Escape
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && isOpen) close();
    });

    // Mensaje de bienvenida (solo si el historial está vacío)
    appendMsg("assistant", WELCOME_MSG);

    // Pulso de atención inicial
    bubble.classList.add("pulse");
    setTimeout(() => bubble.classList.remove("pulse"), 7000);
  }

  // Esperar a que el DOM esté listo
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  return { open, close, toggle };
})();
