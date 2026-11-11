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
]


@pytest.mark.parametrize(
    "cid,peso,zona,cliente,dia,cupon,esperado",
    CASOS_VALIDOS,
    ids=[c[0] for c in CASOS_VALIDOS],
)
def test_costo_tramos_y_zonas(cid, peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado
