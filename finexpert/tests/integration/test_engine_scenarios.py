"""
Pruebas de integración: ciclo completo del motor para los tres perfiles canónicos.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

import pytest


# ================================================================
# Perfil CRÍTICO
# ================================================================
class TestPerfilCritico:
    def test_situacion_es_critica(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert diag.situacion in {"critica", "critica_extrema"}

    def test_semaforo_rojo(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert diag.semaforo == "rojo"

    def test_hay_recomendaciones(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert len(diag.recomendaciones) > 0

    def test_cadena_inferencia_no_vacia(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert len(diag.cadena_inferencia) > 0

    def test_nivel_certeza_alto(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert diag.nivel_certeza >= 80

    def test_proyeccion_tiene_7_puntos(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert diag.proyeccion_6m is not None
        assert len(diag.proyeccion_6m) == 7

    def test_hechos_derivados_contiene_dai(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        assert "DAI" in diag.hechos_derivados

    def test_to_dict_serializable(self, engine, perfil_critico):
        diag = engine.diagnose(perfil_critico)
        d = diag.to_dict()
        assert "situacion" in d
        assert "recomendaciones" in d
        assert isinstance(d["recomendaciones"], list)

    def test_r01_disparada(self, engine, perfil_critico):
        """La regla R01 (ratio_gasto_fijo > 0.70) debe dispararse."""
        diag = engine.diagnose(perfil_critico)
        ids_disparadas = {e["regla_id"] for e in diag.cadena_inferencia}
        assert "R01" in ids_disparadas

    def test_tarjeta_credito_minimo_detectado(self, engine, perfil_critico):
        """D07 debe dispararse: tiene tarjeta y paga solo el mínimo."""
        diag = engine.diagnose(perfil_critico)
        ids = {e["regla_id"] for e in diag.cadena_inferencia}
        assert "D07" in ids


# ================================================================
# Perfil EN RIESGO
# ================================================================
class TestPerfilEnRiesgo:
    def test_situacion_en_riesgo(self, engine, perfil_en_riesgo):
        diag = engine.diagnose(perfil_en_riesgo)
        assert diag.situacion in {"en_riesgo", "moderada"}

    def test_semaforo_amarillo(self, engine, perfil_en_riesgo):
        diag = engine.diagnose(perfil_en_riesgo)
        assert diag.semaforo == "amarillo"

    def test_hay_recomendaciones_ahorro(self, engine, perfil_en_riesgo):
        diag = engine.diagnose(perfil_en_riesgo)
        dominios = {r.dominio for r in diag.recomendaciones}
        assert "ahorro" in dominios or "diagnostico" in dominios

    def test_hechos_derivados_ratio_ahorro(self, engine, perfil_en_riesgo):
        diag = engine.diagnose(perfil_en_riesgo)
        ratio = diag.hechos_derivados.get("ratio_ahorro", None)
        assert ratio is not None
        assert ratio < 0.10   # característico del perfil en riesgo


# ================================================================
# Perfil SALUDABLE
# ================================================================
class TestPerfilSaludable:
    def test_situacion_saludable(self, engine, perfil_saludable):
        diag = engine.diagnose(perfil_saludable)
        assert diag.situacion == "saludable"

    def test_semaforo_verde(self, engine, perfil_saludable):
        diag = engine.diagnose(perfil_saludable)
        assert diag.semaforo == "verde"

    def test_proyeccion_creciente(self, engine, perfil_saludable):
        diag = engine.diagnose(perfil_saludable)
        proy = diag.proyeccion_6m
        assert proy[6] > proy[0]

    def test_recomendaciones_incluyen_inversion(self, engine, perfil_saludable):
        diag = engine.diagnose(perfil_saludable)
        dominios = {r.dominio for r in diag.recomendaciones}
        assert "inversion" in dominios or "pronostico" in dominios

    def test_dai_saludable(self, engine, perfil_saludable):
        diag = engine.diagnose(perfil_saludable)
        dai = diag.hechos_derivados.get("DAI", 1.0)
        assert dai < 0.20


# ================================================================
# Propiedades invariantes (todos los perfiles)
# ================================================================
class TestInvariantes:
    @pytest.mark.parametrize("perfil_fixture", [
        "perfil_critico", "perfil_en_riesgo", "perfil_saludable"
    ])
    def test_semaforo_valido(self, request, engine, perfil_fixture):
        perfil = request.getfixturevalue(perfil_fixture)
        diag = engine.diagnose(perfil)
        assert diag.semaforo in {"rojo", "amarillo", "verde", "gris"}

    @pytest.mark.parametrize("perfil_fixture", [
        "perfil_critico", "perfil_en_riesgo", "perfil_saludable"
    ])
    def test_certeza_en_rango(self, request, engine, perfil_fixture):
        perfil = request.getfixturevalue(perfil_fixture)
        diag = engine.diagnose(perfil)
        assert 0 <= diag.nivel_certeza <= 100

    @pytest.mark.parametrize("perfil_fixture", [
        "perfil_critico", "perfil_en_riesgo", "perfil_saludable"
    ])
    def test_max_cycles_no_excedido(self, request, engine, perfil_fixture):
        """El motor debe terminar en menos de 200 ciclos."""
        perfil = request.getfixturevalue(perfil_fixture)
        diag = engine.diagnose(perfil)
        # Si el motor excede el límite, cadena_inferencia tendría exactamente 200 entradas
        assert len(diag.cadena_inferencia) < 200
