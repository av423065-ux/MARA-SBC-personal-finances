"""Memoria de trabajo: almacena hechos del usuario y hechos derivados durante la sesión."""
from typing import Any


class WorkingMemory:
    """
    Almacén mutable de hechos de la sesión activa de inferencia.
    Soporta aserción, actualización y consulta de hechos.
    """

    def __init__(self, initial_facts: dict[str, Any] | None = None):
        self._facts: dict[str, Any] = {}
        self._history: list[dict] = []   # registro de cambios para trazabilidad
        if initial_facts:
            for k, v in initial_facts.items():
                self.assert_fact(k, v, source="init")

    # ------------------------------------------------------------------
    # Operaciones básicas
    # ------------------------------------------------------------------
    def assert_fact(self, variable: str, valor: Any, source: str = "rule") -> bool:
        """
        Añade o actualiza un hecho.  Devuelve True si hubo un cambio real
        (variable nueva o valor diferente), False si ya existía con mismo valor.
        """
        previous = self._facts.get(variable)
        changed = (variable not in self._facts) or (previous != valor)
        self._facts[variable] = valor
        if changed:
            self._history.append({
                "variable": variable,
                "valor": valor,
                "anterior": previous,
                "source": source,
            })
        return changed

    def get(self, variable: str, default: Any = None) -> Any:
        return self._facts.get(variable, default)

    def contains(self, variable: str) -> bool:
        return variable in self._facts

    def all_facts(self) -> dict:
        return dict(self._facts)

    def history(self) -> list[dict]:
        return list(self._history)

    # ------------------------------------------------------------------
    # Utilidades para el motor de inferencia
    # ------------------------------------------------------------------
    def snapshot(self) -> dict:
        """Instantánea inmutable de los hechos actuales."""
        return dict(self._facts)

    def __repr__(self) -> str:
        return f"WorkingMemory({len(self._facts)} hechos)"
