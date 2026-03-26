"""Pruebas de integración para los endpoints REST de MARA."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

import json
import pytest

# Importar la app Flask directamente (sin servidor)
import app as flask_app


@pytest.fixture(scope="module")
def client():
    """Cliente de prueba de Flask sin servidor HTTP."""
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


def test_health_ok(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert data["reglas_cargadas"] > 0


def test_diagnose_perfil_saludable(client):
    payload = {
        "ingreso_mensual": 30_000,
        "gastos_fijos": 9_000,
        "gastos_variables": 5_000,
        "pago_mensual_deudas": 0,
        "meses_fondo_emergencia": 7,
    }
    res = client.post("/diagnose", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["situacion"] == "saludable"
    assert data["semaforo"] == "verde"
    assert "recomendaciones" in data
    assert "proyeccion_6m" in data


def test_diagnose_perfil_critico(client):
    payload = {
        "ingreso_mensual": 10_000,
        "gastos_fijos": 9_000,
        "gastos_variables": 2_000,
        "pago_mensual_deudas": 0,
    }
    res = client.post("/diagnose", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["situacion"] in ("critica_extrema", "critica")
    assert data["semaforo"] == "rojo"


def test_diagnose_sin_body_retorna_400(client):
    res = client.post("/diagnose", data="no-json", content_type="text/plain")
    assert res.status_code == 400


def test_diagnose_campos_faltantes_retorna_400(client):
    res = client.post("/diagnose", json={"ingreso_mensual": 10_000})
    assert res.status_code == 400


def test_explain_retorna_explicacion(client):
    perfil = {
        "ingreso_mensual": 10_000,
        "gastos_fijos": 8_500,
        "gastos_variables": 500,
        "pago_mensual_deudas": 0,
    }
    payload = {"perfil": perfil, "regla": "D01"}
    res = client.post("/explain", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "explicacion_global" in data
    assert "cadena_inferencia" in data


def test_diagnose_response_schema(client):
    """Verifica que la respuesta incluye todos los campos esperados."""
    payload = {
        "ingreso_mensual": 15_000,
        "gastos_fijos": 6_000,
        "gastos_variables": 3_000,
    }
    res = client.post("/diagnose", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    required_keys = {"situacion", "nivel_certeza", "semaforo",
                     "recomendaciones", "hechos_derivados",
                     "cadena_inferencia", "proyeccion_6m"}
    assert required_keys.issubset(data.keys())
