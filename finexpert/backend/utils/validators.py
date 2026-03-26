"""Validadores de entrada para el wizard de MARA."""
from typing import Any


def validar_ingreso(valor: Any) -> tuple[float, str]:
    """Valida que el ingreso mensual sea un número positivo."""
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.0, "El ingreso mensual debe ser un número."
    if v < 0:
        return 0.0, "El ingreso mensual no puede ser negativo."
    return v, ""


def validar_gasto(nombre: str, valor: Any) -> tuple[float, str]:
    """Valida que un gasto sea un número no negativo."""
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.0, f"{nombre} debe ser un número."
    if v < 0:
        return 0.0, f"{nombre} no puede ser negativo."
    return v, ""


def validar_edad(valor: Any) -> tuple[int, str]:
    """Valida que la edad esté en el rango 18-99."""
    try:
        v = int(valor)
    except (TypeError, ValueError):
        return 30, "La edad debe ser un número entero."
    if not (18 <= v <= 99):
        return 30, "La edad debe estar entre 18 y 99 años."
    return v, ""


def validar_porcentaje(nombre: str, valor: Any) -> tuple[float, str]:
    """Valida que un porcentaje esté entre 0 y 1 (o 0 y 100 como conveniencia)."""
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return 0.0, f"{nombre} debe ser un número."
    if v > 1:
        v = v / 100  # aceptar también formato 0-100
    if not (0 <= v <= 1):
        return 0.0, f"{nombre} debe estar entre 0 y 1."
    return v, ""


def validar_horizonte(valor: Any) -> tuple[int, str]:
    """Valida el horizonte temporal en meses (1 a 600)."""
    try:
        v = int(valor)
    except (TypeError, ValueError):
        return 12, "El horizonte temporal debe ser un número entero de meses."
    if not (1 <= v <= 600):
        return 12, "El horizonte temporal debe estar entre 1 y 600 meses."
    return v, ""


def validar_perfil_completo(data: dict) -> list[str]:
    """Valida todos los campos del perfil y devuelve lista de errores."""
    errores: list[str] = []

    for campo in ["ingreso_mensual", "gastos_fijos", "gastos_variables"]:
        if campo not in data:
            errores.append(f"Campo requerido faltante: {campo}")
        elif float(data.get(campo, -1)) < 0:
            errores.append(f"{campo} no puede ser negativo.")

    if "edad" in data:
        _, e = validar_edad(data["edad"])
        if e:
            errores.append(e)

    if "tasa_promedio_anual" in data:
        _, e = validar_porcentaje("tasa_promedio_anual", data["tasa_promedio_anual"])
        if e:
            errores.append(e)

    return errores
