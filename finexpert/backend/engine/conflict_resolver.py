"""
Resolución de conflictos en la agenda.
Estrategia: prioridad → especificidad → factor de certeza.
"""
from models.rule import Rule


class ConflictResolver:
    """
    Ordena las reglas activables aplicando tres criterios en cascada:
      1. Mayor prioridad (campo 'prioridad', 1-10).
      2. Mayor especificidad (número de condiciones en la cláusula IF).
      3. Mayor factor de certeza (campo 'factor_certeza', 0-100).
    """

    @staticmethod
    def sort_key(rule: Rule) -> tuple:
        """Clave de ordenamiento descendente (negamos para usar sort ascendente)."""
        return (
            -rule.prioridad,
            -rule.especificidad,
            -rule.factor_certeza,
        )

    def resolve(self, candidates: list[Rule]) -> Rule | None:
        """Devuelve la regla de mayor prioridad; None si la lista está vacía."""
        if not candidates:
            return None
        sorted_candidates = sorted(candidates, key=self.sort_key)
        return sorted_candidates[0]

    def rank(self, candidates: list[Rule]) -> list[Rule]:
        """Devuelve la lista ordenada de mayor a menor prioridad compuesta."""
        return sorted(candidates, key=self.sort_key)
