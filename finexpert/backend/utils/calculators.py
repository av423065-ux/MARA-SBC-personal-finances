"""
Utilidades financieras de FinExpert.
Todos los cálculos son funciones puras sin efectos secundarios.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.user_profile import UserProfile


# ------------------------------------------------------------------
# Ratios derivados (también calculados en UserProfile.to_initial_facts)
# Expuestos aquí para pruebas unitarias independientes.
# ------------------------------------------------------------------
def calcular_ratio_gasto_fijo(gastos_fijos: float, ingreso: float) -> float:
    """Proporción del ingreso neto destinada a gastos fijos."""
    if ingreso <= 0:
        return 1.0
    return round(gastos_fijos / ingreso, 4)


def calcular_ratio_ahorro(ingreso: float, gastos_totales: float) -> float:
    """Proporción del ingreso neto disponible para ahorro."""
    if ingreso <= 0:
        return 0.0
    return round(max(0, (ingreso - gastos_totales) / ingreso), 4)


def calcular_DAI(pago_mensual_deudas: float, ingreso: float) -> float:
    """Deuda / Ingresos: porcentaje del ingreso bruto destinado a pagar deudas."""
    if ingreso <= 0:
        return 0.0
    return round(pago_mensual_deudas / ingreso, 4)


# ------------------------------------------------------------------
# Proyección financiera a 6 meses
# ------------------------------------------------------------------
def proyeccion_6_meses(profile: "UserProfile") -> list[float]:
    """
    Devuelve una lista de 7 valores (mes 0 al mes 6) representando
    el ahorro acumulado proyectado con las recomendaciones implementadas.

    Escenario actual:  ahorro_mensual_actual × n meses
    Escenario mejora:  se asume un incremento del 10% en la tasa de ahorro
    (suficiente para mostrar la diferencia sin sobre-prometer).

    El mes 0 es el estado actual (punto de partida).
    """
    ingreso = max(profile.ingreso_mensual, 1)
    gastos_totales = (
        profile.gastos_fijos
        + profile.gastos_variables
        + profile.pago_mensual_deudas
    )
    ahorro_actual = max(0, ingreso - gastos_totales)

    # Ahorro mensual mejorado: +10% si se aplican recomendaciones
    ahorro_mejorado = ahorro_actual * 1.10

    proyeccion: list[float] = []
    acumulado = 0.0
    for mes in range(7):
        acumulado = round(ahorro_mejorado * mes, 2)
        proyeccion.append(acumulado)

    return proyeccion


# ------------------------------------------------------------------
# Análisis de deuda
# ------------------------------------------------------------------
def meses_para_liquidar(deuda: float, tasa_mensual: float, pago_mensual: float) -> int:
    """
    Número de meses para liquidar una deuda dada tasa y pago mensual.
    Usa la fórmula de amortización estándar.
    Devuelve -1 si el pago no cubre los intereses.
    """
    if pago_mensual <= 0:
        return -1
    if tasa_mensual <= 0:
        return max(1, round(deuda / pago_mensual))
    if pago_mensual <= deuda * tasa_mensual:
        return -1   # pago insuficiente para cubrir intereses

    import math
    meses = math.log(pago_mensual / (pago_mensual - deuda * tasa_mensual)) / math.log(1 + tasa_mensual)
    return max(1, math.ceil(meses))


def interes_total_pagado(deuda: float, tasa_mensual: float, pago_mensual: float) -> float:
    """Total de intereses pagados durante la amortización completa."""
    n = meses_para_liquidar(deuda, tasa_mensual, pago_mensual)
    if n < 0:
        return float("inf")
    return round(pago_mensual * n - deuda, 2)


# ------------------------------------------------------------------
# Regla 50/30/20
# ------------------------------------------------------------------
def evaluar_50_30_20(
    ratio_necesidades: float,
    ratio_deseos: float,
    ratio_ahorro: float,
) -> dict:
    """Evalúa qué tan cerca está el usuario de la distribución óptima 50/30/20."""
    desviacion_necesidades = ratio_necesidades - 0.50
    desviacion_deseos      = ratio_deseos - 0.30
    desviacion_ahorro      = 0.20 - ratio_ahorro

    return {
        "necesidades_actual": round(ratio_necesidades * 100, 1),
        "deseos_actual":      round(ratio_deseos * 100, 1),
        "ahorro_actual":      round(ratio_ahorro * 100, 1),
        "exceso_necesidades": round(max(0, desviacion_necesidades) * 100, 1),
        "exceso_deseos":      round(max(0, desviacion_deseos) * 100, 1),
        "deficit_ahorro":     round(max(0, desviacion_ahorro) * 100, 1),
        "cumple_regla":       all([
            ratio_necesidades <= 0.50,
            ratio_deseos <= 0.30,
            ratio_ahorro >= 0.20,
        ]),
    }
