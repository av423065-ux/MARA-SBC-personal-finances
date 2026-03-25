"""Cargador y validador de reglas JSON desde los archivos de dominio."""
import json
import logging
import pathlib
from typing import Optional

from models.rule import Rule

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = {"id", "dominio", "condiciones", "conclusion", "accion",
                   "factor_certeza", "prioridad", "explicacion"}

VALID_DOMAINS = {
    "diagnostico", "deuda", "ahorro",
    "perfil_riesgo", "inversion", "pronostico",
}

VALID_OPERATORS = {">", "<", ">=", "<=", "==", "!="}


class KnowledgeBase:
    """Repositorio central de reglas de producción de FinExpert."""

    def __init__(self, rules_dir: str | pathlib.Path):
        self._rules_dir = pathlib.Path(rules_dir)
        self._rules: list[Rule] = []
        self._load_all()

    # ------------------------------------------------------------------
    # Carga
    # ------------------------------------------------------------------
    def _load_all(self) -> None:
        for domain in VALID_DOMAINS:
            path = self._rules_dir / f"{domain}.json"
            if not path.exists():
                logger.warning("Archivo de reglas no encontrado: %s", path)
                continue
            try:
                raw: list[dict] = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                logger.error("JSON inválido en %s: %s", path, exc)
                continue

            for data in raw:
                errors = self._validate(data, domain)
                if errors:
                    logger.error("Regla inválida %s: %s", data.get("id", "?"), errors)
                    continue
                self._rules.append(Rule.from_dict(data))

        logger.info("KnowledgeBase: %d reglas cargadas.", len(self._rules))

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------
    def _validate(self, data: dict, expected_domain: str) -> list[str]:
        errors: list[str] = []
        missing = REQUIRED_FIELDS - data.keys()
        if missing:
            errors.append(f"Campos faltantes: {missing}")
            return errors  # No tiene sentido seguir

        if data["dominio"] != expected_domain:
            errors.append(
                f"Dominio declarado '{data['dominio']}' no coincide con archivo '{expected_domain}'"
            )
        if not (0 <= data["factor_certeza"] <= 100):
            errors.append("factor_certeza debe estar entre 0 y 100")
        if not (1 <= data["prioridad"] <= 10):
            errors.append("prioridad debe estar entre 1 y 10")

        for i, cond in enumerate(data.get("condiciones", [])):
            if "operador" in cond and cond["operador"] not in VALID_OPERATORS:
                errors.append(
                    f"Condición {i}: operador '{cond['operador']}' no válido"
                )
        return errors

    # ------------------------------------------------------------------
    # Consulta
    # ------------------------------------------------------------------
    @property
    def rules(self) -> list[Rule]:
        return list(self._rules)

    def by_domain(self, domain: str) -> list[Rule]:
        return [r for r in self._rules if r.dominio == domain]

    def by_id(self, rule_id: str) -> Optional[Rule]:
        for r in self._rules:
            if r.id == rule_id:
                return r
        return None

    def stats(self) -> dict:
        from collections import Counter
        counts = Counter(r.dominio for r in self._rules)
        return {
            "total": len(self._rules),
            "por_dominio": dict(counts),
        }
