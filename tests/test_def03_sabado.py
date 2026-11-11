"""Reproducción DEF-03: el sábado (6) debe cobrar el recargo de fin de semana (R5)."""

from envios import calc


def test_sabado_cobra_recargo():
    assert calc(5, "urbana", "ninguno", 6) == 11000
