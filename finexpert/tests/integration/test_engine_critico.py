"""Pruebas de integración — escenario perfil crítico."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))


def test_perfil_critico_situacion_roja(engine, perfil_critico):
    d = engine.diagnose(perfil_critico)
    assert d.situacion in ("critica_extrema", "critica")
    assert d.semaforo == "rojo"


def test_perfil_critico_certeza_alta(engine, perfil_critico):
    d = engine.diagnose(perfil_critico)
    assert d.nivel_certeza >= 70


def test_perfil_critico_tiene_recomendaciones(engine, perfil_critico):
    d = engine.diagnose(perfil_critico)
    assert len(d.recomendaciones) > 0


def test_perfil_critico_proyeccion_valida(engine, perfil_critico):
    d = engine.diagnose(perfil_critico)
    assert d.proyeccion_6m is not None
    assert len(d.proyeccion_6m) == 7
    assert d.proyeccion_6m[0] == 0.0  # mes 0 = ahorro acumulado inicial


def test_perfil_critico_cadena_inferencia_no_vacia(engine, perfil_critico):
    d = engine.diagnose(perfil_critico)
    assert len(d.cadena_inferencia) > 0


def test_perfil_critico_dai_calculado(engine, perfil_critico):
    """DAI = 1800/12000 = 0.15 pero con gastos > ingreso, la situación domina."""
    d = engine.diagnose(perfil_critico)
    assert "DAI" in d.hechos_derivados
    assert abs(d.hechos_derivados["DAI"] - 0.15) < 0.01
