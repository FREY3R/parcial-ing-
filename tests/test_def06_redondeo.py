"""Reproducción DEF-06: redondeo half-up al múltiplo de 100 (R8)."""

from envios import calc


def test_redondeo_half_up():
    assert calc(5, "rural", "ninguno", 3) == 10400
    assert calc(5, "urbana", "frecuente", 3) == 8600
