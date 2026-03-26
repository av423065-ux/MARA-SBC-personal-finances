"""Pruebas de integración — escenario perfil en riesgo."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))


def test_perfil_en_riesgo_semaforo_amarillo(engine, perfil_en_riesgo):
    d = engine.diagnose(perfil_en_riesgo)
    assert d.semaforo == "amarillo"


def test_perfil_en_riesgo_situacion_correcta(engine, perfil_en_riesgo):
    d = engine.diagnose(perfil_en_riesgo)
    assert d.situacion in ("en_riesgo", "moderada")


def test_perfil_en_riesgo_ratio_ahorro_bajo(engine, perfil_en_riesgo):
    d = engine.diagnose(perfil_en_riesgo)
    assert d.hechos_derivados.get("ratio_ahorro", 1) < 0.10


def test_perfil_en_riesgo_tiene_cadena_inferencia(engine, perfil_en_riesgo):
    d = engine.diagnose(perfil_en_riesgo)
    assert len(d.cadena_inferencia) > 0


def test_perfil_en_riesgo_proyeccion_no_nula(engine, perfil_en_riesgo):
    d = engine.diagnose(perfil_en_riesgo)
    assert d.proyeccion_6m is not None
    assert len(d.proyeccion_6m) == 7
