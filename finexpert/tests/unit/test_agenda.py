"""Pruebas unitarias para el módulo Agenda."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

from engine.agenda import Agenda
from engine.conflict_resolver import ConflictResolver
from engine.working_memory import WorkingMemory
from models.rule import Rule, Condition


def _rule(id_, prioridad=5, certeza=80, condiciones=None, conclusion=None):
    """Fábrica de reglas mínimas para pruebas."""
    return Rule(
        id=id_,
        dominio="test",
        descripcion="test",
        condiciones=condiciones or [Condition("x", ">", 0)],
        conclusion=conclusion or {"variable": "r", "valor": True},
        accion="accion",
        factor_certeza=certeza,
        prioridad=prioridad,
        explicacion="",
    )


def test_match_regla_activable():
    ag = Agenda()
    wm = WorkingMemory({"x": 5})
    rules = [_rule("R1")]
    result = ag.match(rules, wm)
    assert "R1" in [r.id for r in result]


def test_match_regla_no_activable():
    ag = Agenda()
    wm = WorkingMemory({"x": 0})  # condición x > 0 no cumple con x=0
    rules = [_rule("R1")]
    result = ag.match(rules, wm)
    assert result == []


def test_regla_disparada_no_se_reactiva():
    ag = Agenda()
    wm = WorkingMemory({"x": 5})
    rule = _rule("R1")
    ag.mark_fired(rule)
    result = ag.match([rule], wm)
    assert result == []


def test_select_retorna_regla_mayor_prioridad():
    ag = Agenda()
    r_low  = _rule("R_low",  prioridad=3)
    r_high = _rule("R_high", prioridad=9)
    selected = ag.select([r_low, r_high])
    assert selected.id == "R_high"


def test_reset_limpia_disparadas():
    ag = Agenda()
    rule = _rule("R1")
    ag.mark_fired(rule)
    ag.reset()
    wm = WorkingMemory({"x": 5})
    result = ag.match([rule], wm)
    assert len(result) == 1
