import pytest
from zeta import zeta
import mpmath as mp

mp.mp.dps = 20


def test_zeta_at_two():
    # ζ(2) = π² / 6 ≈ 1.644934
    expected = mp.pi**2 / 6
    result = zeta(2)
    # Toleranz als positional argument statt rel=
    assert mp.almosteq(result, expected, 1e-12)


def test_zeta_zero():
    # ζ(-1) = -1/12
    assert mp.almosteq(zeta(-1), -1 / 12, 1e-12)
