"""Pruebas de integración — escenario perfil saludable."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))


def test_perfil_saludable_situacion_verde(engine, perfil_saludable):
    d = engine.diagnose(perfil_saludable)
    assert d.situacion == "saludable"
    assert d.semaforo == "verde"


def test_perfil_saludable_certeza_alta(engine, perfil_saludable):
    d = engine.diagnose(perfil_saludable)
    assert d.nivel_certeza >= 60


def test_perfil_saludable_fondo_aceptable_o_optimo(engine, perfil_saludable):
    """perfil_saludable tiene 5 meses de fondo (aceptable: 3-6 meses)."""
    d = engine.diagnose(perfil_saludable)
    assert d.hechos_derivados.get("nivel_fondo_emergencia") in ("aceptable", "optimo")


def test_perfil_saludable_dai_saludable(engine, perfil_saludable):
    d = engine.diagnose(perfil_saludable)
    assert d.hechos_derivados.get("nivel_endeudamiento") == "saludable"


def test_perfil_saludable_proyeccion_creciente(engine, perfil_saludable):
    d = engine.diagnose(perfil_saludable)
    proj = d.proyeccion_6m
    assert proj[6] > proj[0]  # ahorro crece en 6 meses
