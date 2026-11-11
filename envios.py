"""Cálculo de costos de envío — v2.0.0.

Especificación R1–R8 particularizada para el código estudiantil 0182410093.

Diseño:
- Constantes con nombre (sin números mágicos).
- Validaciones en funciones pequeñas de una sola responsabilidad.
- Patrón Estrategia para zonas y para descuentos.
- Aritmética Decimal de extremo a extremo.
- Sin parámetro `flag` ni `CONFIG` global (cambio incompatible → v2.0.0).
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Protocol

# ---------------------------------------------------------------------------
# Parámetros del estudiante (código 0182410093)
# ---------------------------------------------------------------------------
PMAX: Decimal = Decimal("50")
L1: Decimal = Decimal("3")
L2: Decimal = Decimal("10")

RECARGO_RURAL: Decimal = Decimal("0.15")
RECARGO_NACIONAL: Decimal = Decimal("0.40")
DESC_FRECUENTE: Decimal = Decimal("0.05")
DESC_VIP: Decimal = Decimal("0.15")
DESC_CUPON: Decimal = Decimal("0.10")
RECARGO_FINDE: Decimal = Decimal("2000")

COSTO_TRAMO_1: Decimal = Decimal("6000")
COSTO_TRAMO_2: Decimal = Decimal("9000")
COSTO_POR_KG_EXTRA: Decimal = Decimal("800")
COSTO_MINIMO: Decimal = Decimal("5000")
PASO_REDONDEO: Decimal = Decimal("100")

ZONAS_VALIDAS: tuple[str, ...] = ("urbana", "rural", "nacional")
CUPON_VALIDO: str = "ENVIO10"
DIAS_FIN_DE_SEMANA: tuple[int, int] = (6, 7)


class ErrorEnvio(ValueError):
    """Error de validación de los datos de un envío."""


# ---------------------------------------------------------------------------
# Validaciones (R1, R2, R7)
# ---------------------------------------------------------------------------
def validar_peso(peso: Decimal) -> None:
    if not (Decimal("0") < peso <= PMAX):
        raise ErrorEnvio("peso inválido")


def validar_zona(zona: str) -> None:
    if zona not in ZONAS_VALIDAS:
        raise ErrorEnvio("zona inválida")


def validar_dia(dia: int) -> None:
    if not isinstance(dia, int) or not (1 <= dia <= 7):
        raise ErrorEnvio("día inválido")


def validar_cupon(cupon: Optional[str]) -> None:
    if cupon is not None and cupon != CUPON_VALIDO:
        raise ErrorEnvio("cupón inválido")


# ---------------------------------------------------------------------------
# Patrón Estrategia: recargos por zona (R4)
# ---------------------------------------------------------------------------
class EstrategiaZona(Protocol):
    def recargo(self, costo: Decimal) -> Decimal:  # pragma: no cover
        ...


class ZonaUrbana:
    def recargo(self, costo: Decimal) -> Decimal:
        return costo


class ZonaRural:
    def recargo(self, costo: Decimal) -> Decimal:
        return costo * (Decimal("1") + RECARGO_RURAL)


class ZonaNacional:
    def recargo(self, costo: Decimal) -> Decimal:
        return costo * (Decimal("1") + RECARGO_NACIONAL)


ESTRATEGIAS_ZONA: dict[str, EstrategiaZona] = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# ---------------------------------------------------------------------------
# Patrón Estrategia: descuentos por cliente (R6)
# ---------------------------------------------------------------------------
class EstrategiaDescuento(Protocol):
    def aplicar(self, costo: Decimal) -> Decimal:  # pragma: no cover
        ...


class SinDescuento:
    def aplicar(self, costo: Decimal) -> Decimal:
        return costo


class DescuentoFrecuente:
    def aplicar(self, costo: Decimal) -> Decimal:
        return costo * (Decimal("1") - DESC_FRECUENTE)


class DescuentoVip:
    def aplicar(self, costo: Decimal) -> Decimal:
        return costo * (Decimal("1") - DESC_VIP)


ESTRATEGIAS_CLIENTE: dict[str, EstrategiaDescuento] = {
    "ninguno": SinDescuento(),
    "frecuente": DescuentoFrecuente(),
    "vip": DescuentoVip(),
}


# ---------------------------------------------------------------------------
# Cálculo (R3, R5, R6, R8)
# ---------------------------------------------------------------------------
def costo_base(peso: Decimal) -> Decimal:
    """Devuelve el costo del tramo de peso (R3)."""
    if peso <= L1:
        return COSTO_TRAMO_1
    if peso <= L2:
        return COSTO_TRAMO_2
    return COSTO_TRAMO_2 + (peso - L2) * COSTO_POR_KG_EXTRA


def aplicar_descuentos(
    costo: Decimal, cliente: str, cupon: Optional[str]
) -> Decimal:
    """Aplica descuento de cliente y luego cupón (B impar: ambos)."""
    estrategia = ESTRATEGIAS_CLIENTE.get(cliente, SinDescuento())
    costo = estrategia.aplicar(costo)
    if cupon == CUPON_VALIDO:
        costo *= Decimal("1") - DESC_CUPON
    return costo


def redondear_half_up(costo: Decimal) -> int:
    """Redondea al múltiplo de $100 más cercano; los $50 suben (R8)."""
    pasos = (costo / PASO_REDONDEO).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(pasos * PASO_REDONDEO)


def calc(
    peso: float | int | Decimal,
    zona: str,
    cliente: str = "ninguno",
    dia: int = 1,
    cupon: Optional[str] = None,
) -> int:
    """Calcula el costo final de un envío.

    Args:
        peso: peso en kg; debe cumplir ``0 < peso <= 50``.
        zona: ``"urbana"``, ``"rural"`` o ``"nacional"``.
        cliente: ``"ninguno"``, ``"frecuente"`` o ``"vip"``.
        dia: entero de 1 a 7 (6 = sábado, 7 = domingo).
        cupon: ``None`` o ``"ENVIO10"``; cualquier otro valor es error.

    Returns:
        Costo final en pesos, múltiplo de 100.

    Raises:
        ErrorEnvio: si una entrada no cumple R1, R2 o R7.
    """
    peso_dec = Decimal(str(peso))
    validar_peso(peso_dec)
    validar_zona(zona)
    validar_dia(dia)
    validar_cupon(cupon)

    costo = costo_base(peso_dec)
    costo = ESTRATEGIAS_ZONA[zona].recargo(costo)
    costo = aplicar_descuentos(costo, cliente, cupon)

    if dia in DIAS_FIN_DE_SEMANA:
        costo += RECARGO_FINDE

    if costo < COSTO_MINIMO:
        costo = COSTO_MINIMO

    return redondear_half_up(costo)
