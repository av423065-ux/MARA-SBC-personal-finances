"""Pruebas unitarias para las reglas del dominio inversion."""
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


class TestInstrumentoRecomendado:

    def test_capital_alto_agresivo_recomienda_acciones(self, engine):
        d = _run(engine, ingreso_mensual=40_000, gastos_fijos=12_000,
                 gastos_variables=6_000, edad=28, horizonte_temporal=120,
                 capital_disponible=60_000, meses_fondo_emergencia=8)
        assert d.hechos_derivados.get("instrumento") == "acciones_etf"

    def test_capital_medio_moderado_recomienda_fondos_mixtos(self, engine):
        d = _run(engine, ingreso_mensual=25_000, gastos_fijos=9_000,
                 gastos_variables=4_000, edad=40, horizonte_temporal=36,
                 capital_disponible=20_000, meses_fondo_emergencia=5)
        assert d.hechos_derivados.get("instrumento") == "fondos_mixtos"

    def test_conservador_recomienda_cetes(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=8_000,
                 gastos_variables=4_000, edad=55, horizonte_temporal=24,
                 capital_disponible=15_000)
        assert d.hechos_derivados.get("instrumento") == "cetes"


class TestRecomendacionesDiversificacion:

    def test_capital_alto_sin_diversificacion(self, engine):
        d = _run(engine, ingreso_mensual=30_000, gastos_fijos=10_000,
                 gastos_variables=5_000, capital_disponible=15_000,
                 num_instrumentos=1)
        assert d.hechos_derivados.get("recomendacion_diversificar_portafolio") is True

    def test_sin_inversion_con_capital_recomienda_iniciar(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=7_000,
                 gastos_variables=4_000, capital_disponible=5_000,
                 num_instrumentos=0)
        assert d.hechos_derivados.get("recomendacion_iniciar_inversion") is True
