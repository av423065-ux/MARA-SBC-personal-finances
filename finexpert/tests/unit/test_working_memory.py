"""Pruebas unitarias para WorkingMemory."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent / "backend"))

from engine.working_memory import WorkingMemory


def test_assert_fact_nuevo():
    wm = WorkingMemory()
    changed = wm.assert_fact("x", 42)
    assert changed is True
    assert wm.get("x") == 42


def test_assert_fact_mismo_valor_no_cambia():
    wm = WorkingMemory({"x": 10})
    changed = wm.assert_fact("x", 10)
    assert changed is False


def test_assert_fact_valor_diferente_cambia():
    wm = WorkingMemory({"x": 10})
    changed = wm.assert_fact("x", 20)
    assert changed is True
    assert wm.get("x") == 20


def test_contains():
    wm = WorkingMemory({"a": 1})
    assert wm.contains("a") is True
    assert wm.contains("z") is False


def test_snapshot_es_copia():
    wm = WorkingMemory({"a": 1})
    snap = wm.snapshot()
    snap["a"] = 999
    assert wm.get("a") == 1  # no se modificó el original


def test_history_registra_cambios():
    wm = WorkingMemory()
    wm.assert_fact("y", 5)
    wm.assert_fact("y", 10)
    h = wm.history()
    assert len(h) == 2
    assert h[-1]["valor"] == 10
    assert h[-1]["anterior"] == 5


def test_initial_facts_cargados():
    wm = WorkingMemory({"a": 1, "b": 2})
    assert wm.get("a") == 1
    assert wm.get("b") == 2


def test_get_default():
    wm = WorkingMemory()
    assert wm.get("inexistente", "default") == "default"
