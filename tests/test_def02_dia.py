"""Reproducción DEF-02: día fuera de [1,7] o no entero debe fallar (R2)."""

import pytest

from envios import calc


def test_dia_fuera_de_rango_lanza_error():
    for dia in (0, 8, 6.5):
        with pytest.raises(ValueError, match="día inválido"):
            calc(5, "urbana", "ninguno", dia)
