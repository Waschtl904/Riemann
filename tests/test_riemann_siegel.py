import pytest
from riemann_siegel import (
    zeta_riemann_siegel,
    riemann_siegel_z,
    find_zeros_riemann_siegel,
)
from mpmath import mp


def test_zeta_at_two():
    # Bekannter Wert ζ(1/2 + 2i) ≈ ζ(0.5+2i) aus mpmath
    mp.dps = 30
    expected = mp.zeta(mp.mpc(0.5, 2))
    result = zeta_riemann_siegel(2, terms=5, precision=30)
    assert abs(result - expected) < 1e-6


def test_siegel_z_symmetry():
    # Z(t) reell
    val = riemann_siegel_z(14.1347, precision=30)
    assert abs(val.imag) < 1e-8


def test_find_zeros_small_interval():
    zeros = find_zeros_riemann_siegel(14, 15, step=0.1, precision=20)
    assert isinstance(zeros, list)
