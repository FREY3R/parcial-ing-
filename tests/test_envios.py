"""Suite de pruebas de caja negra para envios.calc.

Los resultados esperados se calcularon a mano desde la especificación R1-R8 con
aritmética Decimal (docs/referencia_calculo.py), NO ejecutando el código heredado.

Código 0182410093: PMAX=50, L1=3 (incluido), L2=10, RR=15%, RN=40%, V=15%,
S=2000. D par, E impar (finde después), B impar (ambos descuentos), F impar
(cupón inexistente = ValueError).

Todas las llamadas son posicionales (p, z, c, d, cup) para que la suite siga
siendo válida después de eliminar el parámetro `flag` en v2.0.0.
"""

import pytest

from envios import calc


# (id, peso, zona, cliente, dia, cupon, esperado)
CASOS_VALIDOS = [
    # --- Tramos de peso (R3) ---
    ("C01", 2, "urbana", "ninguno", 3, None, 6000),
    ("C02", 3, "urbana", "ninguno", 3, None, 6000),      # L1 incluido (D par)
    ("C03", 4, "urbana", "ninguno", 3, None, 9000),
    ("C04", 10, "urbana", "ninguno", 3, None, 9000),     # L2 incluido
    ("C05", 11, "urbana", "ninguno", 3, None, 9800),
    ("C06", 12.5, "urbana", "ninguno", 3, None, 11000),  # proporcional
    # --- Zonas (R4) ---
    ("C07", 5, "rural", "ninguno", 3, None, 10400),      # 10350 -> half-up
    ("C08", 5, "nacional", "ninguno", 3, None, 12600),
    ("C09", 5, "urbana", "ninguno", 3, None, 9000),
    # --- Descuentos (R6, B impar: ambos) ---
    ("C10", 5, "urbana", "frecuente", 3, None, 8600),      # 8550 -> half-up
    ("C11", 5, "urbana", "vip", 3, None, 7700),            # 7650 -> half-up
    ("C12", 5, "urbana", "ninguno", 3, "ENVIO10", 8100),
    ("C13", 5, "urbana", "vip", 3, "ENVIO10", 6900),       # 6885
    ("C14", 5, "urbana", "frecuente", 3, "ENVIO10", 7700), # 7695
    # --- Fin de semana (R5, E impar: después de descuentos) ---
    ("C15", 5, "urbana", "ninguno", 6, None, 11000),       # sábado
    ("C16", 5, "urbana", "ninguno", 7, None, 11000),       # domingo
    ("C17", 5, "urbana", "vip", 6, None, 9700),            # 7650+2000
    ("C18", 5, "urbana", "vip", 6, "ENVIO10", 8900),       # 6885+2000
    # --- Límite superior y casos integradores ---
    ("C24", 50, "urbana", "ninguno", 3, None, 41000),      # PMAX válido
    ("C30", 2, "urbana", "vip", 3, "ENVIO10", 5000),       # mínimo
    ("C31", 10.1, "urbana", "ninguno", 3, None, 9100),     # float + half-up
    ("C32", 2, "rural", "frecuente", 6, "ENVIO10", 7900),  # integración
    ("C33", 10.1, "nacional", "ninguno", 3, None, 12700),  # integración
]


@pytest.mark.parametrize(
    "cid,peso,zona,cliente,dia,cupon,esperado",
    CASOS_VALIDOS,
    ids=[c[0] for c in CASOS_VALIDOS],
)
def test_costos_validos(cid, peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado


# (id, peso, zona, cliente, dia, cupon, mensaje esperado)
CASOS_ERROR = [
    ("C19", 5, "urbana", "ninguno", 3, "OTRO", "cupón inválido"),
    ("C20", 5, "urbana", "ninguno", 3, "ENVIO20", "cupón inválido"),
    ("C21", 0, "urbana", "ninguno", 3, None, "peso inválido"),
    ("C22", -1, "urbana", "ninguno", 3, None, "peso inválido"),
    ("C23", 51, "urbana", "ninguno", 3, None, "peso inválido"),
    ("C25", 5, "express", "ninguno", 3, None, "zona inválida"),
    ("C26", 5, "Urbana", "ninguno", 3, None, "zona inválida"),
    ("C27", 5, "urbana", "ninguno", 0, None, "día inválido"),
    ("C28", 5, "urbana", "ninguno", 8, None, "día inválido"),
    ("C29", 5, "urbana", "ninguno", 6.5, None, "día inválido"),
]


@pytest.mark.parametrize(
    "cid,peso,zona,cliente,dia,cupon,mensaje",
    CASOS_ERROR,
    ids=[c[0] for c in CASOS_ERROR],
)
def test_entradas_invalidas(cid, peso, zona, cliente, dia, cupon, mensaje):
    with pytest.raises(ValueError, match=mensaje):
        calc(peso, zona, cliente, dia, cupon)


def test_minimo_5000():
    assert calc(2, "urbana", "vip", 3, "ENVIO10") == 5000


def test_redondeo_half_up_sube():
    assert calc(5, "rural", "ninguno", 3, None) == 10400
    assert calc(5, "urbana", "frecuente", 3, None) == 8600


def test_sabado_y_domingo():
    assert calc(5, "urbana", "ninguno", 6, None) == 11000
    assert calc(5, "urbana", "ninguno", 7, None) == 11000
