"""
FinExpert — Punto de entrada Flask.
Expone dos endpoints REST:
  POST /diagnose  → ejecuta el motor de inferencia y devuelve el diagnóstico
  POST /explain   → devuelve la cadena de razonamiento de una regla específica
  GET  /health    → verificación de disponibilidad del servicio
"""
from __future__ import annotations
import logging
import pathlib
import sys

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# Ajuste de ruta para imports relativos desde backend/
BASE_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from knowledge.knowledge_base import KnowledgeBase
from knowledge.fact_base import FactBase
from engine.inference_engine import InferenceEngine
from engine.explainer import Explainer
from models.user_profile import UserProfile

# ------------------------------------------------------------------
# Configuración de logging
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger("finexpert.api")

# ------------------------------------------------------------------
# Inicialización del sistema (se hace una sola vez al arrancar)
# ------------------------------------------------------------------
RULES_DIR   = BASE_DIR / "knowledge" / "rules"
FACTS_FILE  = BASE_DIR / "knowledge" / "ontology" / "umbrales_financieros.json"

try:
    kb      = KnowledgeBase(RULES_DIR)
    fb      = FactBase(FACTS_FILE)
    engine  = InferenceEngine(kb)
    logger.info("Sistema FinExpert inicializado: %s", kb.stats())
except Exception as exc:
    logger.critical("Error crítico al inicializar FinExpert: %s", exc)
    raise

# ------------------------------------------------------------------
# Aplicación Flask
# ------------------------------------------------------------------
app = Flask(__name__)
CORS(app)   # Permite peticiones desde el front-end local


# ------------------------------------------------------------------
# Helpers de validación
# ------------------------------------------------------------------
def _parse_profile(data: dict) -> tuple[UserProfile | None, str]:
    """Construye un UserProfile desde el JSON del request; devuelve error si falla."""
    required = ["ingreso_mensual", "gastos_fijos", "gastos_variables"]
    missing = [f for f in required if f not in data]
    if missing:
        return None, f"Campos requeridos faltantes: {missing}"
    try:
        profile = UserProfile(**{
            k: v for k, v in data.items()
            if k in UserProfile.__dataclass_fields__
        })
        return profile, ""
    except (TypeError, ValueError) as exc:
        return None, str(exc)


def _error(msg: str, code: int = 400) -> tuple[Response, int]:
    return jsonify({"error": msg}), code


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------
@app.get("/health")
def health():
    """Verificación de disponibilidad."""
    return jsonify({
        "status": "ok",
        "sistema": "FinExpert",
        "reglas_cargadas": kb.stats()["total"],
    })


@app.post("/diagnose")
def diagnose():
    """
    Ejecuta el diagnóstico financiero completo.

    Body JSON:
        ingreso_mensual       float  (requerido)
        gastos_fijos          float  (requerido)
        gastos_variables      float  (requerido)
        pago_mensual_deudas   float  (opcional, default 0)
        deuda_total           float  (opcional)
        tasa_promedio_anual   float  (opcional)
        num_creditos          int    (opcional)
        edad                  int    (opcional)
        num_dependientes      int    (opcional)
        nivel_educacion_financiera  int  (opcional, 1-5)
        tipo_ingreso          str    (opcional: "fijo"|"variable")
        horizonte_temporal    int    (opcional, meses)
        meta_monto            float  (opcional)
        meses_fondo_emergencia float (opcional)
        lleva_registro_gastos bool  (opcional)
        ahorro_automatico     bool  (opcional)
        ... (resto de campos de UserProfile)

    Respuesta JSON:
        situacion       str
        nivel_certeza   int
        semaforo        str  (rojo|amarillo|verde|gris)
        recomendaciones list[{regla_id, dominio, accion, explicacion, ...}]
        hechos_derivados dict
        cadena_inferencia list[{...}]
        proyeccion_6m   list[float]
    """
    data = request.get_json(silent=True)
    if not data:
        return _error("Se requiere un body JSON con el perfil financiero.")

    profile, err = _parse_profile(data)
    if err:
        return _error(err)

    try:
        diagnosis = engine.diagnose(profile)
        logger.info(
            "Diagnóstico completado: %s (certeza %d%%)",
            diagnosis.situacion, diagnosis.nivel_certeza,
        )
        return jsonify(diagnosis.to_dict())
    except Exception as exc:
        logger.exception("Error durante el diagnóstico: %s", exc)
        return _error("Error interno del motor de inferencia.", 500)


@app.post("/explain")
def explain():
    """
    Devuelve la explicación detallada de una regla específica
    disparada en la sesión más reciente.

    Body JSON:
        perfil  dict   (mismo que /diagnose)
        regla   str    (ID de la regla, ej. "R01")

    Respuesta JSON:
        explicacion_global  str    (texto completo de la cadena de inferencia)
        regla_detalle       dict   (info de la regla solicitada, null si no disparó)
        cadena_inferencia   list
    """
    data = request.get_json(silent=True)
    if not data:
        return _error("Se requiere body JSON con {perfil, regla}.")

    perfil_data = data.get("perfil", {})
    regla_id    = data.get("regla", "")

    profile, err = _parse_profile(perfil_data)
    if err:
        return _error(err)

    try:
        diagnosis = engine.diagnose(profile)

        # Reconstruir explicaciones desde la cadena
        local_explainer = Explainer()
        for entry in diagnosis.cadena_inferencia:
            rule = kb.by_id(entry["regla_id"])
            if rule:
                local_explainer.record(
                    rule=rule,
                    activating_facts=entry.get("hechos_activadores", {}),
                    derived_fact=entry.get("hecho_derivado", {}),
                )

        return jsonify({
            "explicacion_global": local_explainer.to_natural_language(
                diagnosis.situacion, diagnosis.nivel_certeza
            ),
            "regla_detalle": local_explainer.explain_rule(regla_id),
            "cadena_inferencia": diagnosis.cadena_inferencia,
        })
    except Exception as exc:
        logger.exception("Error en /explain: %s", exc)
        return _error("Error interno al generar la explicación.", 500)


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
