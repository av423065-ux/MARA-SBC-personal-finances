"""Dataclass que representa una regla de producción IF-THEN de la base de conocimiento."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Condition:
    """Una condición individual de la cláusula IF."""
    variable: str
    operador: str   # >, <, >=, <=, ==, !=
    valor: Any

    def evaluate(self, facts: dict) -> bool:
        """Evalúa la condición contra los hechos de la memoria de trabajo.
        
        Nota semántica: si la variable no existe en la memoria de trabajo,
        el operador '!=' devuelve True (algo desconocido ≠ cualquier valor concreto).
        Todos los demás operadores devuelven False ante una variable ausente.
        """
        if self.variable not in facts:
            return self.operador == "!="
        fact_val = facts[self.variable]
        op = self.operador
        val = self.valor
        try:
            if op == ">":   return fact_val > val
            if op == "<":   return fact_val < val
            if op == ">=":  return fact_val >= val
            if op == "<=":  return fact_val <= val
            if op == "==":  return fact_val == val
            if op == "!=":  return fact_val != val
        except TypeError:
            return False
        return False


@dataclass
class Rule:
    """Regla de producción completa."""
    id: str
    dominio: str
    descripcion: str
    condiciones: list[Condition]
    conclusion: dict      # {"variable": str, "valor": Any}
    accion: str
    factor_certeza: int   # 0-100
    prioridad: int        # 1-10
    explicacion: str

    @property
    def especificidad(self) -> int:
        """Número de condiciones — usado para resolver empates en la agenda."""
        return len(self.condiciones)

    @classmethod
    def from_dict(cls, data: dict) -> "Rule":
        condiciones = [
            Condition(
                variable=c["variable"],
                operador=c["operador"],
                valor=c["valor"],
            )
            for c in data["condiciones"]
        ]
        return cls(
            id=data["id"],
            dominio=data["dominio"],
            descripcion=data.get("descripcion", ""),
            condiciones=condiciones,
            conclusion=data["conclusion"],
            accion=data.get("accion", ""),
            factor_certeza=data.get("factor_certeza", 80),
            prioridad=data.get("prioridad", 5),
            explicacion=data.get("explicacion", ""),
        )
