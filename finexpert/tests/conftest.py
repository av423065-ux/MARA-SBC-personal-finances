"""
Fixtures compartidas para las pruebas de MARA.
Define los tres perfiles canónicos: crítico, en_riesgo y saludable.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "backend"))

import pytest
from models.user_profile import UserProfile
from knowledge.knowledge_base import KnowledgeBase
from knowledge.fact_base import FactBase
from engine.inference_engine import InferenceEngine

RULES_DIR  = pathlib.Path(__file__).parent.parent / "backend" / "knowledge" / "rules"
FACTS_FILE = pathlib.Path(__file__).parent.parent / "backend" / "knowledge" / "ontology" / "umbrales_financieros.json"


@pytest.fixture(scope="session")
def kb():
    return KnowledgeBase(RULES_DIR)

@pytest.fixture(scope="session")
def fb():
    return FactBase(FACTS_FILE)

@pytest.fixture(scope="session")
def engine(kb):
    return InferenceEngine(kb)


# ------------------------------------------------------------------
# Perfiles canónicos
# ------------------------------------------------------------------
@pytest.fixture
def perfil_critico():
    """Gastos fijos > 70% ingreso, sin ahorro, deuda alta."""
    return UserProfile(
        edad=32,
        ingreso_mensual=12_000,
        gastos_fijos=9_500,       # ratio_gasto_fijo = 0.79
        gastos_variables=2_000,
        pago_mensual_deudas=1_800,
        deuda_total=85_000,
        tasa_promedio_anual=0.42,
        num_creditos=3,
        tipo_ingreso="fijo",
        nivel_educacion_financiera=2,
        tiene_tarjeta_credito=True,
        paga_minimo_tarjeta=True,
        meses_fondo_emergencia=0,
        lleva_registro_gastos=False,
    )

@pytest.fixture
def perfil_en_riesgo():
    """Gastos controlados pero ahorro < 10%."""
    return UserProfile(
        edad=27,
        ingreso_mensual=18_000,
        gastos_fijos=9_000,       # ratio_gasto_fijo = 0.50
        gastos_variables=5_400,
        pago_mensual_deudas=2_500,
        deuda_total=40_000,
        tasa_promedio_anual=0.28,
        num_creditos=2,
        tipo_ingreso="fijo",
        nivel_educacion_financiera=3,
        meses_fondo_emergencia=1,
        lleva_registro_gastos=True,
        ahorro_automatico=False,
    )

@pytest.fixture
def perfil_saludable():
    """Gastos < 50%, ahorro ≥ 20%, sin deudas relevantes."""
    return UserProfile(
        edad=35,
        ingreso_mensual=35_000,
        gastos_fijos=12_000,      # ratio_gasto_fijo = 0.34
        gastos_variables=7_000,
        pago_mensual_deudas=0,
        deuda_total=0,
        tasa_promedio_anual=0.0,
        num_creditos=0,
        tipo_ingreso="fijo",
        nivel_educacion_financiera=5,
        meses_fondo_emergencia=5,
        lleva_registro_gastos=True,
        ahorro_automatico=True,
        capital_disponible=15_000,
        num_instrumentos=2,
    )
