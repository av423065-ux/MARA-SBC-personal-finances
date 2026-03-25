"""
Motor de Inferencia de FinExpert — implementación RETE simplificada.
Ciclo: Match → Select → Execute, con encadenamiento hacia adelante.
"""
import logging
from typing import Optional

from models.rule import Rule
from models.user_profile import UserProfile, Diagnosis, Recommendation
from knowledge.knowledge_base import KnowledgeBase
from engine.working_memory import WorkingMemory
from engine.agenda import Agenda
from engine.conflict_resolver import ConflictResolver
from engine.explainer import Explainer
from utils.calculators import proyeccion_6_meses

logger = logging.getLogger(__name__)

# Límite de ciclos para evitar bucles infinitos
MAX_CYCLES = 200

# Mapa de situación → semáforo
_SEMAFORO = {
    "critica_extrema": "rojo",
    "critica":         "rojo",
    "en_riesgo":       "amarillo",
    "moderada":        "amarillo",
    "saludable":       "verde",
}


class InferenceEngine:
    """
    Orquesta el ciclo Match-Select-Execute sobre la base de conocimiento
    y la memoria de trabajo para producir un diagnóstico financiero completo.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        self._kb = knowledge_base
        self._resolver = ConflictResolver()

    # ------------------------------------------------------------------
    # Punto de entrada principal
    # ------------------------------------------------------------------
    def diagnose(self, profile: UserProfile) -> Diagnosis:
        """
        Ejecuta el ciclo de inferencia completo para el perfil dado.
        Devuelve un objeto Diagnosis con diagnóstico, recomendaciones,
        proyección y cadena de razonamiento.
        """
        # Inicialización de la sesión
        memory   = WorkingMemory(profile.to_initial_facts())
        agenda   = Agenda(self._resolver)
        explainer = Explainer()
        recommendations: list[Recommendation] = []
        rules    = self._kb.rules

        cycles = 0
        while cycles < MAX_CYCLES:
            cycles += 1

            # --- Fase MATCH ---
            candidates = agenda.match(rules, memory)
            if not candidates:
                logger.debug("Ciclo %d: sin reglas activables. Fin de inferencia.", cycles)
                break

            # --- Fase SELECT ---
            selected: Optional[Rule] = agenda.select(candidates)
            if selected is None:
                break

            # --- Fase EXECUTE ---
            facts_snapshot = memory.snapshot()

            # Asertar la conclusión en la memoria de trabajo
            conclusion = selected.conclusion
            memory.assert_fact(
                conclusion["variable"],
                conclusion["valor"],
                source=selected.id,
            )

            # Registrar en el módulo explicativo
            explainer.record(
                rule=selected,
                activating_facts=facts_snapshot,
                derived_fact=conclusion,
            )

            # Acumular recomendación
            activating = [
                f"{c.variable} {c.operador} {c.valor}"
                for c in selected.condiciones
            ]
            recommendations.append(
                Recommendation(
                    regla_id=selected.id,
                    dominio=selected.dominio,
                    accion=selected.accion,
                    explicacion=selected.explicacion,
                    factor_certeza=selected.factor_certeza,
                    hechos_activadores=activating,
                )
            )

            # Marcar como disparada (no se re-dispara)
            agenda.mark_fired(selected)
            logger.debug(
                "Ciclo %d: disparada %s → %s=%s (certeza %d%%)",
                cycles, selected.id,
                conclusion["variable"], conclusion["valor"],
                selected.factor_certeza,
            )

        # ------------------------------------------------------------------
        # Post-procesamiento
        # ------------------------------------------------------------------
        final_facts = memory.all_facts()
        situacion   = final_facts.get("situacion", "sin_datos")
        semaforo    = _SEMAFORO.get(situacion, "gris")

        # Certeza del diagnóstico: promedio ponderado por prioridad de reglas disparadas
        certeza = self._calculate_certainty(recommendations)

        # Proyección financiera a 6 meses
        proyeccion = proyeccion_6_meses(profile)

        return Diagnosis(
            situacion=situacion,
            nivel_certeza=certeza,
            semaforo=semaforo,
            recomendaciones=self._prioritize(recommendations),
            hechos_derivados=final_facts,
            cadena_inferencia=explainer.explain_all(),
            proyeccion_6m=proyeccion,
        )

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    @staticmethod
    def _calculate_certainty(recs: list[Recommendation]) -> int:
        """Certeza global: promedio ponderado por factor_certeza de cada regla."""
        if not recs:
            return 0
        total = sum(r.factor_certeza for r in recs)
        return round(total / len(recs))

    @staticmethod
    def _prioritize(recs: list[Recommendation]) -> list[Recommendation]:
        """Ordena las recomendaciones por factor_certeza descendente."""
        return sorted(recs, key=lambda r: -r.factor_certeza)
