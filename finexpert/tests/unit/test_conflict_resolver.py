"""Pruebas unitarias para ConflictResolver."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

from engine.conflict_resolver import ConflictResolver
from models.rule import Rule, Condition


def _rule(id_, prioridad=5, certeza=80, n_conds=1):
    condiciones = [Condition(f"v{i}", ">", 0) for i in range(n_conds)]
    return Rule(
        id=id_, dominio="test", descripcion="",
        condiciones=condiciones,
        conclusion={"variable": "r", "valor": True},
        accion="", factor_certeza=certeza,
        prioridad=prioridad, explicacion="",
    )


def test_resuelve_por_prioridad():
    cr = ConflictResolver()
    r1 = _rule("R1", prioridad=3)
    r2 = _rule("R2", prioridad=8)
    assert cr.resolve([r1, r2]).id == "R2"


def test_resuelve_por_especificidad_con_misma_prioridad():
    cr = ConflictResolver()
    r_gen  = _rule("Rgen",  prioridad=5, n_conds=1)
    r_spec = _rule("Rspec", prioridad=5, n_conds=4)
    assert cr.resolve([r_gen, r_spec]).id == "Rspec"


def test_resuelve_por_certeza_con_misma_prio_y_especificidad():
    cr = ConflictResolver()
    r_low  = _rule("Rlow",  prioridad=5, certeza=60)
    r_high = _rule("Rhigh", prioridad=5, certeza=90)
    assert cr.resolve([r_low, r_high]).id == "Rhigh"


def test_resolve_lista_vacia_retorna_none():
    cr = ConflictResolver()
    assert cr.resolve([]) is None


def test_rank_mantiene_orden_correcto():
    cr = ConflictResolver()
    rules = [_rule("R1", prioridad=3), _rule("R2", prioridad=7), _rule("R3", prioridad=5)]
    ranked = cr.rank(rules)
    assert [r.id for r in ranked] == ["R2", "R3", "R1"]
