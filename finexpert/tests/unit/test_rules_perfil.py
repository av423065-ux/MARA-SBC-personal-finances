"""Pruebas unitarias para las reglas del dominio perfil_riesgo."""
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


class TestPerfilRiesgo:

    def test_joven_horizonte_largo_da_agresivo(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=7_000,
                 gastos_variables=4_000, edad=28, horizonte_temporal=72)
        assert d.hechos_derivados.get("perfil_riesgo") == "agresivo"

    def test_adulto_horizonte_medio_da_moderado(self, engine):
        d = _run(engine, ingreso_mensual=25_000, gastos_fijos=9_000,
                 gastos_variables=5_000, edad=40, horizonte_temporal=36)
        assert d.hechos_derivados.get("perfil_riesgo") == "moderado"

    def test_mayor_60_da_muy_conservador(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=8_000,
                 gastos_variables=4_000, edad=62)
        assert d.hechos_derivados.get("perfil_riesgo") == "muy_conservador"

    def test_perfil_agresivo_con_fondo_optimo_puede_renta_variable(self, engine):
        d = _run(engine, ingreso_mensual=30_000, gastos_fijos=10_000,
                 gastos_variables=5_000, edad=28, horizonte_temporal=120,
                 meses_fondo_emergencia=8)
        assert d.hechos_derivados.get("puede_invertir_renta_variable") is True


class TestToleranciaRiesgo:

    def test_educacion_baja_da_tolerancia_baja(self, engine):
        d = _run(engine, ingreso_mensual=15_000, gastos_fijos=6_000,
                 gastos_variables=3_000, nivel_educacion_financiera=2)
        assert d.hechos_derivados.get("tolerancia_riesgo") == "baja"

    def test_educacion_alta_horizonte_largo_da_tolerancia_alta(self, engine):
        d = _run(engine, ingreso_mensual=20_000, gastos_fijos=7_000,
                 gastos_variables=3_000, nivel_educacion_financiera=5,
                 horizonte_temporal=36)
        assert d.hechos_derivados.get("tolerancia_riesgo") == "alta"
