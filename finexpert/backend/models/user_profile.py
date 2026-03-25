"""Dataclasses para el perfil del usuario y el resultado del diagnóstico."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserProfile:
    """Perfil financiero completo del usuario (input del wizard)."""
    # Paso 1 – Perfil básico
    edad: int = 30
    estado_civil: str = "soltero"       # soltero, casado, divorciado, viudo
    num_dependientes: int = 0
    nivel_educacion_financiera: int = 3  # 1-5

    # Paso 2 – Ingresos y gastos
    ingreso_mensual: float = 0.0
    gastos_fijos: float = 0.0           # renta, servicios, transporte
    gastos_variables: float = 0.0       # alimentación, entretenimiento
    deuda_total: float = 0.0
    tasa_promedio_anual: float = 0.0    # tasa de interés promedio de deudas
    num_creditos: int = 0
    pago_mensual_deudas: float = 0.0
    tipo_ingreso: str = "fijo"          # fijo | variable (freelance)

    # Banderas de deuda
    tiene_tarjeta_credito: bool = False
    paga_minimo_tarjeta: bool = False
    tiene_hipoteca: bool = False
    tiene_credito_nomina: bool = False
    tiene_deuda_tasa_variable: bool = False
    usa_credito_para_gastos_basicos: bool = False
    tendencia_tasas: str = "estable"    # alza | baja | estable

    # Paso 3 – Metas
    objetivo_principal: str = "ahorro"  # ahorro, deuda, emergencia, inversion, retiro
    horizonte_temporal: int = 12        # meses
    meta_monto: float = 0.0

    # Estado del ahorro
    meses_fondo_emergencia: float = 0.0
    ahorro_automatico: bool = False
    lleva_registro_gastos: bool = False
    paga_ISR: bool = False
    num_instrumentos: int = 0
    capital_disponible: float = 0.0
    tasa_rendimiento_esperada: float = 0.0
    tasa_inflacion: float = 0.04        # referencia Banxico
    tendencia_ahorro: str = "estable"   # creciente | decreciente | estable
    tendencia_gasto: str = "estable"
    meses_deficit: int = 0
    mes_alto_gasto: bool = False
    pago_extra_deuda: float = 0.0
    cambio_habitos: bool = False
    reserva_impuestos: bool = False

    def to_initial_facts(self) -> dict:
        """Convierte el perfil en hechos calculados para la memoria de trabajo."""
        ingreso = max(self.ingreso_mensual, 1)  # evitar división por cero
        gastos_totales = self.gastos_fijos + self.gastos_variables + self.pago_mensual_deudas

        ratio_gasto_fijo    = self.gastos_fijos / ingreso
        ratio_gasto_variable = self.gastos_variables / ingreso
        ratio_ahorro        = max(0, (ingreso - gastos_totales) / ingreso)
        ratio_necesidades   = ratio_gasto_fijo
        ratio_deseos        = ratio_gasto_variable
        dai                 = self.pago_mensual_deudas / ingreso
        ahorro_proyectado_6m = max(0, ingreso - gastos_totales) * 6

        return {
            # Datos crudos del perfil
            "edad":                       self.edad,
            "estado_civil":               self.estado_civil,
            "num_dependientes":           self.num_dependientes,
            "nivel_educacion_financiera": self.nivel_educacion_financiera,
            "ingreso_mensual":            self.ingreso_mensual,
            "gastos_fijos":               self.gastos_fijos,
            "gastos_variables":           self.gastos_variables,
            "deuda_total":                self.deuda_total,
            "tasa_promedio_anual":        self.tasa_promedio_anual,
            "num_creditos":               self.num_creditos,
            "pago_mensual_deudas":        self.pago_mensual_deudas,
            "tipo_ingreso":               self.tipo_ingreso,
            "tiene_tarjeta_credito":      self.tiene_tarjeta_credito,
            "paga_minimo_tarjeta":        self.paga_minimo_tarjeta,
            "tiene_hipoteca":             self.tiene_hipoteca,
            "tiene_credito_nomina":       self.tiene_credito_nomina,
            "tiene_deuda_tasa_variable":  self.tiene_deuda_tasa_variable,
            "usa_credito_para_gastos_basicos": self.usa_credito_para_gastos_basicos,
            "tendencia_tasas":            self.tendencia_tasas,
            "objetivo_principal":         self.objetivo_principal,
            "horizonte_temporal":         self.horizonte_temporal,
            "meta_monto":                 self.meta_monto,
            "horizonte_meta":             self.horizonte_temporal,
            "meses_fondo_emergencia":     self.meses_fondo_emergencia,
            "ahorro_automatico":          self.ahorro_automatico,
            "lleva_registro_gastos":      self.lleva_registro_gastos,
            "paga_ISR":                   self.paga_ISR,
            "num_instrumentos":           self.num_instrumentos,
            "capital_disponible":         self.capital_disponible,
            "tasa_rendimiento_esperada":  self.tasa_rendimiento_esperada,
            "tasa_inflacion":             self.tasa_inflacion,
            "tendencia_ahorro":           self.tendencia_ahorro,
            "tendencia_gasto":            self.tendencia_gasto,
            "meses_deficit":              self.meses_deficit,
            "mes_alto_gasto":             self.mes_alto_gasto,
            "pago_extra_deuda":           self.pago_extra_deuda,
            "cambio_habitos":             self.cambio_habitos,
            "reserva_impuestos":          self.reserva_impuestos,
            # Hechos derivados (calculados)
            "ratio_gasto_fijo":           round(ratio_gasto_fijo, 4),
            "ratio_gasto_variable":       round(ratio_gasto_variable, 4),
            "ratio_ahorro":               round(ratio_ahorro, 4),
            "ratio_necesidades":          round(ratio_necesidades, 4),
            "ratio_deseos":               round(ratio_deseos, 4),
            "DAI":                        round(dai, 4),
            "ahorro_proyectado_6m":       round(ahorro_proyectado_6m, 2),
            "instrumento":                "cuenta_bancaria",   # default inicial
        }


@dataclass
class Recommendation:
    """Una recomendación generada por el motor."""
    regla_id: str
    dominio: str
    accion: str
    explicacion: str
    factor_certeza: int
    hechos_activadores: list[str] = field(default_factory=list)


@dataclass
class Diagnosis:
    """Resultado completo devuelto por el motor de inferencia."""
    situacion: str = "sin_datos"
    nivel_certeza: int = 0
    semaforo: str = "gris"          # rojo | amarillo | verde | gris
    recomendaciones: list[Recommendation] = field(default_factory=list)
    hechos_derivados: dict = field(default_factory=dict)
    cadena_inferencia: list[dict] = field(default_factory=list)
    proyeccion_6m: Optional[list[float]] = None

    def to_dict(self) -> dict:
        return {
            "situacion": self.situacion,
            "nivel_certeza": self.nivel_certeza,
            "semaforo": self.semaforo,
            "recomendaciones": [
                {
                    "regla_id": r.regla_id,
                    "dominio": r.dominio,
                    "accion": r.accion,
                    "explicacion": r.explicacion,
                    "factor_certeza": r.factor_certeza,
                    "hechos_activadores": r.hechos_activadores,
                }
                for r in self.recomendaciones
            ],
            "hechos_derivados": self.hechos_derivados,
            "cadena_inferencia": self.cadena_inferencia,
            "proyeccion_6m": self.proyeccion_6m,
        }
