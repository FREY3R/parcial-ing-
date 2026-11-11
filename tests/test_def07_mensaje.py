"""Reproducción DEF-07: el mensaje de peso inválido debe llevar tilde (R1)."""

import pytest

from envios import calc


def test_mensaje_peso_con_tilde():
    with pytest.raises(ValueError, match="peso inválido"):
        calc(0, "urbana", "ninguno", 3)
