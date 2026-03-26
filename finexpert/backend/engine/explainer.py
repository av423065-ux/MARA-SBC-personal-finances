"""
Módulo explicativo de MARA.
Convierte la bitácora de trazabilidad del motor de inferencia
en explicaciones en lenguaje natural accesibles para el usuario.
"""
from models.rule import Rule


class Explainer:
    """
    Registra cada disparo de regla durante el ciclo Match-Select-Execute
    y genera explicaciones en lenguaje natural bajo demanda.
    """

    def __init__(self):
        self._trace: list[dict] = []    # bitácora de reglas disparadas

    # ------------------------------------------------------------------
    # Registro durante la inferencia
    # ------------------------------------------------------------------
    def record(
        self,
        rule: Rule,
        activating_facts: dict,
        derived_fact: dict,
    ) -> None:
        """Registra el disparo de una regla con su contexto."""
        self._trace.append({
            "regla_id":        rule.id,
            "dominio":         rule.dominio,
            "descripcion":     rule.descripcion,
            "accion":          rule.accion,
            "factor_certeza":  rule.factor_certeza,
            "prioridad":       rule.prioridad,
            "explicacion":     rule.explicacion,
            "hechos_activadores": {
                k: v for k, v in activating_facts.items()
                if any(c.variable == k for c in rule.condiciones)
            },
            "hecho_derivado":  derived_fact,
        })

    # ------------------------------------------------------------------
    # Generación de explicaciones
    # ------------------------------------------------------------------
    def explain_all(self) -> list[dict]:
        """Devuelve la bitácora completa (para el panel ¿Por qué? del dashboard)."""
        return list(self._trace)

    def explain_rule(self, rule_id: str) -> dict | None:
        """Explicación detallada de una regla específica."""
        for entry in self._trace:
            if entry["regla_id"] == rule_id:
                return self._format_entry(entry)
        return None

    def summary(self) -> str:
        """Resumen de texto plano de la cadena de inferencia."""
        if not self._trace:
            return "No se dispararon reglas durante esta sesión."

        lines = ["Cadena de razonamiento:\n"]
        for i, entry in enumerate(self._trace, 1):
            facts_str = ", ".join(
                f"{k}={v}" for k, v in entry["hechos_activadores"].items()
            )
            derived = entry["hecho_derivado"]
            derived_str = f"{derived.get('variable')} = {derived.get('valor')}"
            lines.append(
                f"  {entry['regla_id']} → {entry['explicacion']}\n"
                f"        Hechos: [{facts_str}] → {derived_str} "
                f"(certeza: {entry['factor_certeza']}%)\n"
            )
        return "\n".join(lines)

    def to_natural_language(self, situation: str, certainty: int) -> str:
        """
        Genera el bloque completo de explicación en lenguaje natural
        que aparece en el dashboard del usuario.
        """
        header = (
            f"Diagnóstico: situación financiera {situation.upper().replace('_', ' ')} "
            f"(certeza: {certainty}%)\n\n"
        )
        return header + self.summary()

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    @staticmethod
    def _format_entry(entry: dict) -> dict:
        return {
            "regla":          entry["regla_id"],
            "dominio":        entry["dominio"],
            "descripcion":    entry["descripcion"],
            "explicacion":    entry["explicacion"],
            "certeza":        f"{entry['factor_certeza']}%",
            "hechos":         entry["hechos_activadores"],
            "resultado":      entry["hecho_derivado"],
        }

    def reset(self) -> None:
        self._trace.clear()
