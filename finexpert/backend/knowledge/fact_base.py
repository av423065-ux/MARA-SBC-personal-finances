"""Base de hechos: umbrales, rangos y constantes del dominio financiero mexicano."""
import json
import pathlib

_DEFAULTS = {
    "umbrales_gasto": {
        "ratio_gasto_fijo_critico":   0.70,
        "ratio_gasto_fijo_atencion":  0.60,
        "ratio_gasto_fijo_saludable": 0.50,
    },
    "umbrales_ahorro": {
        "ratio_ahorro_minimo":              0.10,
        "ratio_ahorro_recomendado":         0.20,
        "ratio_ahorro_optimo":              0.30,
        "meses_fondo_emergencia_minimo":    3,
        "meses_fondo_emergencia_recomendado": 6,
        "meses_fondo_emergencia_freelance": 12,
    },
    "umbrales_deuda": {
        "DAI_saludable":     0.20,
        "DAI_moderado":      0.35,
        "DAI_alto":          0.50,
        "tasa_usuraria":     0.36,
        "num_creditos_maximo": 4,
    },
    "distribucion_presupuesto": {
        "regla_50_30_20": {"necesidades": 0.50, "deseos": 0.30, "ahorro": 0.20},
        "regla_70_20_10_critica": {"necesidades": 0.70, "deuda": 0.20, "ahorro": 0.10},
    },
    "instrumentos_referencia": {
        "CETES_28_dias_referencia": 0.105,
        "inflacion_objetivo_banxico": 0.03,
        "fuente_tasas": "https://www.banxico.org.mx",
    },
}


class FactBase:
    """Acceso centralizado a los umbrales y constantes financieras del dominio."""

    def __init__(self, path: str | pathlib.Path | None = None):
        self._data = dict(_DEFAULTS)
        if path:
            p = pathlib.Path(path)
            if p.exists():
                loaded = json.loads(p.read_text(encoding="utf-8"))
                self._data.update(loaded)

    # ------------------------------------------------------------------
    # Accesores de alto nivel (conveniencia para el motor)
    # ------------------------------------------------------------------
    @property
    def ratio_gasto_critico(self) -> float:
        return self._data["umbrales_gasto"]["ratio_gasto_fijo_critico"]

    @property
    def ratio_gasto_atencion(self) -> float:
        return self._data["umbrales_gasto"]["ratio_gasto_fijo_atencion"]

    @property
    def ratio_ahorro_minimo(self) -> float:
        return self._data["umbrales_ahorro"]["ratio_ahorro_minimo"]

    @property
    def DAI_moderado(self) -> float:
        return self._data["umbrales_deuda"]["DAI_moderado"]

    @property
    def DAI_alto(self) -> float:
        return self._data["umbrales_deuda"]["DAI_alto"]

    @property
    def tasa_usuraria(self) -> float:
        return self._data["umbrales_deuda"]["tasa_usuraria"]

    @property
    def CETES_referencia(self) -> float:
        return self._data["instrumentos_referencia"]["CETES_28_dias_referencia"]

    def get(self, *keys, default=None):
        """Acceso genérico anidado: fact_base.get('umbrales_deuda', 'DAI_saludable')."""
        node = self._data
        for k in keys:
            if not isinstance(node, dict) or k not in node:
                return default
            node = node[k]
        return node

    def as_dict(self) -> dict:
        return dict(self._data)
