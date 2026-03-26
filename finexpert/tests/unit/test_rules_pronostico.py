"""Pruebas unitarias para las reglas del dominio pronostico."""
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


class TestPronostico6m:

    def test_gasto_creciente_con_deficit_da_deterioro(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=5_000,
                 gastos_variables=4_000, tendencia_gasto="creciente",
                 meses_deficit=3)
        assert d.hechos_derivados.get("pronostico_6m") == "deterioro"

    def test_gasto_estable_ahorro_bajo_da_estancamiento(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=5_500,
                 gastos_variables=5_500, tendencia_gasto="estable")
        assert d.hechos_derivados.get("pronostico_6m") == "estancamiento"

    def test_ahorro_creciente_15_da_mejora_significativa(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=7_000,
                 gastos_variables=4_000, tendencia_ahorro="creciente")
        assert d.hechos_derivados.get("pronostico_6m") == "mejora_significativa"


class TestAlertasPronostico:

    def test_deficit_mas_4_meses_alerta_insolvencia(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=4_000,
                 gastos_variables=3_000, meses_deficit=5)
        assert d.hechos_derivados.get("alerta_riesgo_insolvencia") is True

    def test_freelance_sin_reserva_impuestos(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=8_000,
                 gastos_variables=4_000, tipo_ingreso="variable",
                 reserva_impuestos=False)
        assert d.hechos_derivados.get("alerta_sin_reserva_impuestos") is True

    def test_urgencia_intervencion_critica_sin_cambios(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=5_000,
                 gastos_variables=4_000, tendencia_gasto="creciente",
                 meses_deficit=4, cambio_habitos=False)
        assert d.hechos_derivados.get("urgencia_intervencion") == "critica"
