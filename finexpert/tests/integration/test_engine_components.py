"""
Pruebas unitarias del motor de inferencia de FinExpert.
Cubre: WorkingMemory, ConflictResolver, Agenda, Explainer,
       KnowledgeBase (carga y validación) y calculators.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

import pytest
from models.rule import Rule, Condition
from engine.working_memory import WorkingMemory
from engine.conflict_resolver import ConflictResolver
from engine.agenda import Agenda
from engine.explainer import Explainer
from utils.calculators import (
    calcular_ratio_gasto_fijo, calcular_ratio_ahorro,
    calcular_DAI, proyeccion_6_meses, meses_para_liquidar,
    evaluar_50_30_20,
)


# ================================================================
# WorkingMemory
# ================================================================
class TestWorkingMemory:
    def test_assert_new_fact(self):
        wm = WorkingMemory()
        changed = wm.assert_fact("ratio_gasto_fijo", 0.75)
        assert changed is True
        assert wm.get("ratio_gasto_fijo") == 0.75

    def test_assert_same_value_not_changed(self):
        wm = WorkingMemory({"x": 1})
        changed = wm.assert_fact("x", 1)
        assert changed is False

    def test_update_existing_fact(self):
        wm = WorkingMemory({"situacion": "critica"})
        wm.assert_fact("situacion", "saludable")
        assert wm.get("situacion") == "saludable"

    def test_contains(self):
        wm = WorkingMemory({"DAI": 0.30})
        assert wm.contains("DAI")
        assert not wm.contains("ratio_ahorro")

    def test_snapshot_is_copy(self):
        wm = WorkingMemory({"a": 1})
        snap = wm.snapshot()
        snap["a"] = 99
        assert wm.get("a") == 1  # original no modificado

    def test_initial_facts_loaded(self):
        wm = WorkingMemory({"a": 1, "b": 2})
        assert len(wm.all_facts()) == 2


# ================================================================
# Condition.evaluate
# ================================================================
class TestCondition:
    def test_greater_than_true(self):
        cond = Condition("ratio_gasto_fijo", ">", 0.70)
        assert cond.evaluate({"ratio_gasto_fijo": 0.75}) is True

    def test_greater_than_false(self):
        cond = Condition("ratio_gasto_fijo", ">", 0.70)
        assert cond.evaluate({"ratio_gasto_fijo": 0.65}) is False

    def test_equal_bool(self):
        cond = Condition("lleva_registro_gastos", "==", False)
        assert cond.evaluate({"lleva_registro_gastos": False}) is True

    def test_not_equal(self):
        cond = Condition("situacion", "!=", "critica")
        assert cond.evaluate({"situacion": "saludable"}) is True

    def test_missing_variable_returns_false(self):
        cond = Condition("variable_inexistente", ">", 0)
        assert cond.evaluate({}) is False


# ================================================================
# ConflictResolver
# ================================================================
def _make_rule(id, prioridad, num_condiciones, factor_certeza):
    condiciones = [
        Condition(f"v{i}", ">", 0) for i in range(num_condiciones)
    ]
    return Rule(
        id=id, dominio="test", descripcion="",
        condiciones=condiciones, conclusion={},
        accion="", factor_certeza=factor_certeza,
        prioridad=prioridad, explicacion="",
    )

class TestConflictResolver:
    def test_higher_priority_wins(self):
        r1 = _make_rule("R1", prioridad=8, num_condiciones=1, factor_certeza=80)
        r2 = _make_rule("R2", prioridad=5, num_condiciones=3, factor_certeza=95)
        result = ConflictResolver().resolve([r1, r2])
        assert result.id == "R1"

    def test_specificity_breaks_tie(self):
        r1 = _make_rule("R1", prioridad=8, num_condiciones=1, factor_certeza=90)
        r2 = _make_rule("R2", prioridad=8, num_condiciones=3, factor_certeza=80)
        result = ConflictResolver().resolve([r1, r2])
        assert result.id == "R2"

    def test_certeza_breaks_double_tie(self):
        r1 = _make_rule("R1", prioridad=8, num_condiciones=2, factor_certeza=75)
        r2 = _make_rule("R2", prioridad=8, num_condiciones=2, factor_certeza=95)
        result = ConflictResolver().resolve([r1, r2])
        assert result.id == "R2"

    def test_empty_returns_none(self):
        assert ConflictResolver().resolve([]) is None


# ================================================================
# Agenda
# ================================================================
class TestAgenda:
    def _simple_rule(self, id, variable, operador, valor, prioridad=5):
        c = Condition(variable, operador, valor)
        return Rule(
            id=id, dominio="test", descripcion="",
            condiciones=[c],
            conclusion={"variable": "x", "valor": "y"},
            accion="", factor_certeza=80,
            prioridad=prioridad, explicacion="",
        )

    def test_match_returns_activatable_rules(self):
        rule = self._simple_rule("R1", "ratio_gasto_fijo", ">", 0.70)
        wm = WorkingMemory({"ratio_gasto_fijo": 0.80})
        agenda = Agenda()
        candidates = agenda.match([rule], wm)
        assert len(candidates) == 1

    def test_match_excludes_unmet_conditions(self):
        rule = self._simple_rule("R1", "ratio_gasto_fijo", ">", 0.70)
        wm = WorkingMemory({"ratio_gasto_fijo": 0.60})
        agenda = Agenda()
        candidates = agenda.match([rule], wm)
        assert len(candidates) == 0

    def test_fired_rules_excluded(self):
        rule = self._simple_rule("R1", "ratio_gasto_fijo", ">", 0.70)
        wm = WorkingMemory({"ratio_gasto_fijo": 0.80})
        agenda = Agenda()
        agenda.mark_fired(rule)
        candidates = agenda.match([rule], wm)
        assert len(candidates) == 0

    def test_reset_clears_fired(self):
        rule = self._simple_rule("R1", "ratio_gasto_fijo", ">", 0.70)
        wm = WorkingMemory({"ratio_gasto_fijo": 0.80})
        agenda = Agenda()
        agenda.mark_fired(rule)
        agenda.reset()
        candidates = agenda.match([rule], wm)
        assert len(candidates) == 1


# ================================================================
# Explainer
# ================================================================
class TestExplainer:
    def _rule(self):
        return Rule(
            id="R01", dominio="diagnostico",
            descripcion="Test", condiciones=[Condition("x", ">", 0)],
            conclusion={"variable": "situacion", "valor": "critica"},
            accion="accion_test", factor_certeza=95, prioridad=10,
            explicacion="Tus gastos son críticos.",
        )

    def test_record_and_explain_all(self):
        exp = Explainer()
        rule = self._rule()
        exp.record(rule, {"x": 0.80}, {"variable": "situacion", "valor": "critica"})
        trace = exp.explain_all()
        assert len(trace) == 1
        assert trace[0]["regla_id"] == "R01"

    def test_explain_rule_by_id(self):
        exp = Explainer()
        rule = self._rule()
        exp.record(rule, {"x": 0.80}, {"variable": "situacion", "valor": "critica"})
        detail = exp.explain_rule("R01")
        assert detail is not None
        assert detail["certeza"] == "95%"

    def test_explain_unknown_rule_returns_none(self):
        exp = Explainer()
        assert exp.explain_rule("R99") is None

    def test_natural_language_includes_situation(self):
        exp = Explainer()
        rule = self._rule()
        exp.record(rule, {"x": 0.80}, {"variable": "situacion", "valor": "critica"})
        nl = exp.to_natural_language("critica", 95)
        assert "CRITICA" in nl
        assert "95%" in nl


# ================================================================
# KnowledgeBase (carga y stats)
# ================================================================
class TestKnowledgeBase:
    def test_total_rules(self, kb):
        assert kb.stats()["total"] == 80

    def test_six_domains(self, kb):
        stats = kb.stats()["por_dominio"]
        assert len(stats) == 6

    def test_domain_counts(self, kb):
        stats = kb.stats()["por_dominio"]
        assert stats["diagnostico"] == 20
        assert stats["deuda"] == 15
        assert stats["ahorro"] == 15
        assert stats["perfil_riesgo"] == 10
        assert stats["inversion"] == 10
        assert stats["pronostico"] == 10

    def test_by_id_found(self, kb):
        rule = kb.by_id("R01")
        assert rule is not None
        assert rule.dominio == "diagnostico"

    def test_by_id_not_found(self, kb):
        assert kb.by_id("ZZZZ") is None

    def test_by_domain(self, kb):
        deudas = kb.by_domain("deuda")
        assert len(deudas) == 15


# ================================================================
# Calculators
# ================================================================
class TestCalculators:
    def test_ratio_gasto_fijo(self):
        assert calcular_ratio_gasto_fijo(7_000, 10_000) == 0.70

    def test_ratio_gasto_fijo_cero_ingreso(self):
        assert calcular_ratio_gasto_fijo(5_000, 0) == 1.0

    def test_ratio_ahorro(self):
        assert calcular_ratio_ahorro(10_000, 8_000) == 0.20

    def test_ratio_ahorro_negativo_clipped(self):
        assert calcular_ratio_ahorro(10_000, 12_000) == 0.0

    def test_DAI(self):
        assert calcular_DAI(3_500, 10_000) == 0.35

    def test_meses_para_liquidar_sin_interes(self):
        assert meses_para_liquidar(12_000, 0, 1_000) == 12

    def test_meses_para_liquidar_insuficiente(self):
        # Pago mensual menor que los intereses
        assert meses_para_liquidar(100_000, 0.05, 100) == -1

    def test_evaluar_50_30_20_cumple(self):
        result = evaluar_50_30_20(0.45, 0.25, 0.25)
        assert result["cumple_regla"] is True

    def test_evaluar_50_30_20_no_cumple(self):
        result = evaluar_50_30_20(0.75, 0.20, 0.05)
        assert result["cumple_regla"] is False
        assert result["deficit_ahorro"] == 15.0

    def test_proyeccion_6_meses_longitud(self, perfil_saludable):
        proy = proyeccion_6_meses(perfil_saludable)
        assert len(proy) == 7  # mes 0 al 6

    def test_proyeccion_mes_cero_es_cero(self, perfil_saludable):
        proy = proyeccion_6_meses(perfil_saludable)
        assert proy[0] == 0.0

    def test_proyeccion_creciente(self, perfil_saludable):
        proy = proyeccion_6_meses(perfil_saludable)
        assert all(proy[i] <= proy[i+1] for i in range(len(proy)-1))
