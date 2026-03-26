"""Pruebas unitarias para las reglas del dominio ahorro."""
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


class TestNivelFondoEmergencia:

    def test_fondo_insuficiente_menor_3_meses(self, engine):
        d = _run(engine, ingreso_mensual=15_000, gastos_fijos=6_000,
                 gastos_variables=3_000, meses_fondo_emergencia=1)
        assert d.hechos_derivados.get("nivel_fondo_emergencia") == "insuficiente"

    def test_fondo_aceptable_entre_3_y_6_meses(self, engine):
        d = _run(engine, ingreso_mensual=15_000, gastos_fijos=6_000,
                 gastos_variables=3_000, meses_fondo_emergencia=4)
        assert d.hechos_derivados.get("nivel_fondo_emergencia") == "aceptable"

    def test_fondo_optimo_mayor_6_meses(self, engine):
        d = _run(engine, ingreso_mensual=15_000, gastos_fijos=5_000,
                 gastos_variables=2_000, meses_fondo_emergencia=8)
        assert d.hechos_derivados.get("nivel_fondo_emergencia") == "optimo"


class TestNivelAhorro:

    def test_ahorro_bajo_menor_10(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=5_000,
                 gastos_variables=4_500, pago_mensual_deudas=0)
        assert d.hechos_derivados.get("nivel_ahorro") == "bajo"

    def test_ahorro_optimo_mayor_20(self, engine):
        d = _run(engine, ingreso_mensual=10_000, gastos_fijos=4_000,
                 gastos_variables=2_000, pago_mensual_deudas=0)
        assert d.hechos_derivados.get("nivel_ahorro") == "optimo"


class TestUrgenciaFondo:

    def test_urgencia_critica_freelance_sin_fondo(self, engine):
        d = _run(engine, ingreso_mensual=18_000, gastos_fijos=7_000,
                 gastos_variables=4_000, tipo_ingreso="variable",
                 meses_fondo_emergencia=0)
        assert d.hechos_derivados.get("urgencia_fondo_emergencia") == "critica"

    def test_urgencia_alta_fijo_sin_fondo(self, engine):
        d = _run(engine, ingreso_mensual=15_000, gastos_fijos=6_000,
                 gastos_variables=3_000, tipo_ingreso="fijo",
                 meses_fondo_emergencia=1)
        assert d.hechos_derivados.get("urgencia_fondo_emergencia") == "alta"


class TestHabitosAhorro:

    def test_recomendacion_registro_sin_llevar(self, engine):
        d = _run(engine, ingreso_mensual=12_000, gastos_fijos=5_000,
                 gastos_variables=3_000, lleva_registro_gastos=False)
        assert d.hechos_derivados.get("recomendacion_iniciar_registro_gastos") is True

    def test_situacion_ahorro_excelente(self, engine):
        d = _run(engine, ingreso_mensual=30_000, gastos_fijos=8_000,
                 gastos_variables=5_000, meses_fondo_emergencia=8)
        assert d.hechos_derivados.get("situacion_ahorro") == "excelente"
