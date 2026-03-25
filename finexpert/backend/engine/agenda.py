"""
Agenda del motor de inferencia.
Mantiene el conjunto de reglas activables (conflict set) en cada ciclo
y delega la selección al ConflictResolver.
"""
from models.rule import Rule
from engine.conflict_resolver import ConflictResolver
from engine.working_memory import WorkingMemory


class Agenda:
    """
    Fase MATCH: compara cada regla de la base de conocimiento
    contra los hechos actuales de la memoria de trabajo.
    Una regla se añade a la agenda si TODAS sus condiciones se satisfacen.
    """

    def __init__(self, resolver: ConflictResolver | None = None):
        self._resolver = resolver or ConflictResolver()
        self._fired: set[str] = set()   # IDs de reglas ya disparadas (no se re-disparan)

    def match(self, rules: list[Rule], memory: WorkingMemory) -> list[Rule]:
        """
        Devuelve las reglas activables según los hechos actuales,
        excluyendo las ya disparadas.
        Aplica evaluación de cortocircuito: si la primera condición falla,
        no se evalúan las siguientes.
        """
        facts = memory.all_facts()
        activatable: list[Rule] = []

        for rule in rules:
            if rule.id in self._fired:
                continue
            if all(cond.evaluate(facts) for cond in rule.condiciones):
                activatable.append(rule)

        return activatable

    def select(self, candidates: list[Rule]) -> Rule | None:
        """Fase SELECT: elige la regla de mayor prioridad compuesta."""
        return self._resolver.resolve(candidates)

    def mark_fired(self, rule: Rule) -> None:
        """Registra una regla como disparada para evitar bucles infinitos."""
        self._fired.add(rule.id)

    def reset(self) -> None:
        """Reinicia el registro de reglas disparadas (nueva sesión)."""
        self._fired.clear()

    @property
    def fired_ids(self) -> set[str]:
        return frozenset(self._fired)
