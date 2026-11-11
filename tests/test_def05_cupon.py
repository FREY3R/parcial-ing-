"""Reproducción DEF-05: cupón inexistente debe lanzar ValueError (R7, F impar)."""

import pytest

from envios import calc


def test_cupon_inexistente_lanza_error():
    with pytest.raises(ValueError, match="cupón inválido"):
        calc(5, "urbana", "ninguno", 3, "OTRO")
