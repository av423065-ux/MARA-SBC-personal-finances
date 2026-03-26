"""Pruebas unitarias para las reglas del dominio deuda."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

import pytest
from models.user_profile import UserProfile
from engine.inference_engine import InferenceEngine
from knowledge.knowledge_base import KnowledgeBase

RULES_DIR = pathlib.Path(__file__).parent.parent.parent / "backend" / "knowledge" / "rules"


@pytest.fixture(scope="module")
def engine():
    return InferenceEngine(KnowledgeBase(RULES_DIR))


def _run(engine, **kw):
    return engine.diagnose(UserProfile(**kw))


class TestNivelEndeudamiento:

    def test_dai_alto_da_nivel_critico(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=3_000,
                 gastos_variables=1_000, pago_mensual_deudas=6_000)
        assert d.hechos_derivados.get("nivel_endeudamiento") == "critico"

    def test_dai_moderado(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=2_500)
        assert d.hechos_derivados.get("nivel_endeudamiento") == "moderado"

    def test_dai_saludable(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=1_000)
        assert d.hechos_derivados.get("nivel_endeudamiento") == "saludable"


class TestEstrategiaDeuda:

    def test_avalancha_con_deuda_alta_multiple(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=3_000,
                 gastos_variables=1_000, pago_mensual_deudas=4_000,
                 num_creditos=2)
        assert d.hechos_derivados.get("estrategia_deuda") == "avalancha"

    def test_snowball_con_deuda_moderada(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=2_500)
        assert d.hechos_derivados.get("estrategia_deuda") == "snowball"


class TestAlertasDeuda:

    def test_alerta_pago_extra_positivo(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=2_500,
                 pago_extra_deuda=500)
        assert d.hechos_derivados.get("impacto_pago_extra") == "positivo"

    def test_alerta_tasa_variable_en_alza(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=1_500,
                 tiene_deuda_tasa_variable=True, tendencia_tasas="alza")
        assert d.hechos_derivados.get("alerta_tasa_variable_riesgo") is True
