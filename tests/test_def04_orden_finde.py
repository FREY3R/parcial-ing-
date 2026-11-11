"""Reproducción DEF-04: con E impar el finde se suma después de descuentos (R5)."""

from envios import calc


def test_finde_despues_de_descuentos():
    assert calc(5, "urbana", "ninguno", 7, "ENVIO10") == 10100
