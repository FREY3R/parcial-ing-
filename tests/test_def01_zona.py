"""Reproducción DEF-01: zona desconocida debe lanzar ValueError (R2)."""

import pytest

from envios import calc


def test_zona_invalida_lanza_error():
    with pytest.raises(ValueError, match="zona inválida"):
        calc(5, "express", "ninguno", 3)
