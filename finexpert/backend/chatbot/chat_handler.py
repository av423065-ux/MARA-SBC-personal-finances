"""
Módulo de chatbot para MARA.
Ensambla el contexto en tres capas y llama a OpenRouter con el modelo más económico disponible.
"""
from __future__ import annotations
import json
import os
import pathlib
import urllib.request
import urllib.error
import logging

logger = logging.getLogger("mara.chat")

_KNOWLEDGE_DIR = pathlib.Path(__file__).parent.parent / "knowledge"
_INSTRUCTIONS_FILE = _KNOWLEDGE_DIR / "chat_instructions.md"
_SBC_CONTEXT_FILE  = _KNOWLEDGE_DIR / "sbc_context.md"

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Cargamos los archivos estáticos una sola vez al importar el módulo
def _load_text(path: pathlib.Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        logger.warning("Archivo de contexto no encontrado: %s", path)
        return ""

_INSTRUCTIONS = _load_text(_INSTRUCTIONS_FILE)
_SBC_CONTEXT  = _load_text(_SBC_CONTEXT_FILE)


def _format_user_context(ctx: dict) -> str:
    """Convierte el contexto del usuario en texto compacto para el system prompt."""
    lines = ["## Perfil financiero del usuario (resultado del diagnóstico MARA)"]

    semaforo_map = {"rojo": "🔴 CRÍTICO", "amarillo": "🟡 EN RIESGO", "verde": "🟢 SALUDABLE", "gris": "⚫ SIN DATOS"}
    situacion = ctx.get("situacion", "")
    semaforo  = ctx.get("semaforo", "")
    lines.append(f"- Situación: {situacion} ({semaforo_map.get(semaforo, semaforo)}), certeza: {ctx.get('certeza', '?')}%")

    if ctx.get("ingreso"):
        lines.append(f"- Ingreso mensual neto: ${ctx['ingreso']:,.0f} MXN")
    if ctx.get("tipo_ingreso"):
        lines.append(f"- Tipo de ingreso: {ctx['tipo_ingreso']}")
    if ctx.get("ratio_ahorro") is not None:
        pct = ctx["ratio_ahorro"] * 100
        lines.append(f"- Tasa de ahorro: {pct:.1f}%")
    if ctx.get("ratio_gasto_fijo") is not None:
        pct = ctx["ratio_gasto_fijo"] * 100
        lines.append(f"- Gasto fijo / ingreso: {pct:.1f}%")
    if ctx.get("DAI") is not None:
        pct = ctx["DAI"] * 100
        lines.append(f"- DAI (deuda/ingreso): {pct:.1f}%")
    if ctx.get("fondo_emergencia_meses") is not None:
        lines.append(f"- Fondo de emergencia: {ctx['fondo_emergencia_meses']} meses")
    if ctx.get("objetivo"):
        lines.append(f"- Objetivo principal: {ctx['objetivo']}")
    if ctx.get("perfil_riesgo"):
        lines.append(f"- Perfil de inversión: {ctx['perfil_riesgo']}")

    recs = ctx.get("top_recomendaciones", [])
    if recs:
        lines.append("- Top recomendaciones del sistema:")
        for r in recs[:3]:
            lines.append(f"  · {r}")

    return "\n".join(lines)


def _build_system_prompt(user_context: dict | None) -> str:
    parts = [_INSTRUCTIONS, "\n\n---\n\n# Conocimiento base del SBC MARA\n", _SBC_CONTEXT]
    if user_context:
        parts.append("\n\n---\n\n")
        parts.append(_format_user_context(user_context))
    return "".join(parts)


def _build_messages(user_message: str, history: list[dict], user_context: dict | None) -> list[dict]:
    system_prompt = _build_system_prompt(user_context)
    messages = [{"role": "system", "content": system_prompt}]
    # Ventana deslizante: últimas 6 interacciones (3 pares user/assistant)
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": user_message})
    return messages


def call_chat(user_message: str, history: list[dict], user_context: dict | None = None) -> str:
    """
    Llama a OpenRouter y devuelve la respuesta del asistente como string.
    Lanza RuntimeError si la API falla.
    """
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY no configurada.")

    model = os.getenv("CHAT_MODEL", "openai/gpt-oss-20b:free")
    max_tokens = int(os.getenv("CHAT_MAX_TOKENS", "300"))

    messages = _build_messages(user_message, history, user_context)

    payload = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.4,
    }).encode("utf-8")

    req = urllib.request.Request(
        _OPENROUTER_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mara-sbc.local",
            "X-Title": "MARA Asistente Financiero",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        logger.error("OpenRouter HTTP %s: %s", exc.code, error_body)
        raise RuntimeError(f"Error de API ({exc.code}): {error_body[:200]}")
    except urllib.error.URLError as exc:
        logger.error("OpenRouter URLError: %s", exc.reason)
        raise RuntimeError("No se pudo conectar con el servicio de chat.")

    try:
        reply = body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as exc:
        logger.error("Respuesta inesperada de OpenRouter: %s", body)
        raise RuntimeError("Respuesta inesperada del servicio de chat.")

    logger.info("Chat completado. Modelo: %s, tokens aprox.: %s",
                model, body.get("usage", {}).get("total_tokens", "?"))
    return reply
