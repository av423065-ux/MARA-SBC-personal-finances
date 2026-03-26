"""Pruebas unitarias para las reglas del dominio diagnóstico."""
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


def _diagnose(engine, **kwargs):
    """Helper: crea un UserProfile con los kwargs dados y ejecuta el motor."""
    profile = UserProfile(**kwargs)
    return engine.diagnose(profile)


class TestSituacionCriticaExtrema:

    def test_gastos_totales_superan_ingreso_da_zona_roja(self, engine):
        """Gastos fijos 80% del ingreso con deficit total → zona roja (critica_extrema o critica).
        Nota: to_initial_facts() hace max(0, ratio_ahorro), así ratio_ahorro=0 cuando hay déficit;
        la situación se determina por ratio_gasto_fijo = 0.80, que activa D03 → critica."""
        d = _diagnose(engine, ingreso_mensual=10_000, gastos_fijos=8_000,
                      gastos_variables=3_000, pago_mensual_deudas=0)
        assert d.situacion in ("critica_extrema", "critica")
        assert d.semaforo == "rojo"

    def test_ratio_gasto_fijo_mayor_80_da_critica_extrema(self, engine):
        """ratio_gasto_fijo > 0.80 con ingreso positivo → critica_extrema."""
        d = _diagnose(engine, ingreso_mensual=10_000, gastos_fijos=8_500,
                      gastos_variables=500, pago_mensual_deudas=0)
        assert d.situacion == "critica_extrema"


class TestSituacionCritica:

    def test_ratio_gasto_fijo_entre_70_80(self, engine):
        """ratio_gasto_fijo entre 0.70 y 0.80 → critica."""
        d = _diagnose(engine, ingreso_mensual=10_000, gastos_fijos=7_500,
                      gastos_variables=1_000, pago_mensual_deudas=0)
        assert d.situacion == "critica"
        assert d.semaforo == "rojo"

    def test_dai_mayor_50_da_critica(self, engine):
        """DAI > 0.50 → situacion en zona roja."""
        d = _diagnose(engine, ingreso_mensual=10_000, gastos_fijos=3_000,
                      gastos_variables=1_000, pago_mensual_deudas=6_000)
        assert d.situacion in ("critica", "critica_extrema")


class TestSituacionEnRiesgo:

    def test_ahorro_menor_10_da_en_riesgo(self, engine):
        """ratio_ahorro < 0.10 y gastos controlados → en_riesgo."""
        d = _diagnose(engine, ingreso_mensual=10_000, gastos_fijos=5_000,
                      gastos_variables=4_500, pago_mensual_deudas=0)
        assert d.situacion == "en_riesgo"
        assert d.semaforo == "amarillo"


class TestSituacionSaludable:

    def test_gastos_bajo_50_ahorro_mayor_20(self, engine):
        """Gastos fijos ≤ 50% e ingreso con ahorro ≥ 20% → saludable."""
        d = _diagnose(engine, ingreso_mensual=20_000, gastos_fijos=7_000,
                      gastos_variables=4_000, pago_mensual_deudas=0)
        assert d.situacion == "saludable"
        assert d.semaforo == "verde"


class TestAlertasSecundarias:

    def test_alerta_pago_minimo_tarjeta(self, engine):
        """paga_minimo_tarjeta=True → recomendación relacionada en la respuesta."""
        d = _diagnose(engine, ingreso_mensual=15_000, gastos_fijos=6_000,
                      gastos_variables=3_000, paga_minimo_tarjeta=True,
                      tiene_tarjeta_credito=True)
        ids = [r.regla_id for r in d.recomendaciones]
        assert "D11" in ids or any("minimo" in r.accion.lower() for r in d.recomendaciones)

    def test_alerta_tasa_usuraria(self, engine):
        """tasa_promedio_anual > 36% → regla D14 debe disparar."""
        d = _diagnose(engine, ingreso_mensual=12_000, gastos_fijos=5_000,
                      gastos_variables=2_000, tasa_promedio_anual=0.48,
                      deuda_total=30_000, pago_mensual_deudas=1_500)
        assert d.hechos_derivados.get("alerta_tasa_usuraria") is True

    def test_ingreso_variable_sin_fondo(self, engine):
        """tipo_ingreso variable + fondo < 6 meses → alerta D20."""
        d = _diagnose(engine, ingreso_mensual=20_000, gastos_fijos=8_000,
                      gastos_variables=4_000, tipo_ingreso="variable",
                      meses_fondo_emergencia=1)
        assert d.hechos_derivados.get("alerta_fondo_insuficiente_freelance") is True
