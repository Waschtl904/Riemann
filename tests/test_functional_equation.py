import pytest
import mpmath as mp
from functional_equation import (
    zeta_via_functional,
    zeta_complete,
    benchmark_methods,
    validate_functional_equation,
)
from zeta import zeta


class TestFunctionalEquationBasics:
    def test_zeta_via_functional_matches_direct(self):
        # Test für einige Stellen auf der kritischen Linie
        mp.mp.dps = 15
        test_points = [0.5 + 10j, 0.5 + 20j, 0.5 + 50j]
        for s in test_points:
            direct = zeta(s)
            functional = zeta_via_functional(s)
            # Relative Abweichung klein
            assert abs(direct - functional) / abs(direct) < 1e-8

    def test_zeta_complete_auto(self):
        mp.mp.dps = 15
        # Kleiner Imaginärteil → direkte Methode
        s1 = 2 + 10j
        assert zeta_complete(s1) == zeta(s1)
        # Großer Imaginärteil → funktionale Gleichung
        s2 = 2 + 100j
        assert zeta_complete(s2) == zeta_via_functional(s2)


class TestValidateAndBenchmark:
    def test_validate_functional_equation(self):
        mp.mp.dps = 20
        s = 0.5 + 30j
        valid, direct, functional, error = validate_functional_equation(
            s, tolerance=1e-12
        )
        assert valid is True
        assert isinstance(direct, complex)
        assert isinstance(functional, complex)
        assert error < 1e-12

    def test_benchmark_methods_structure(self):
        mp.mp.dps = 10
        points = [0.5 + 10j, 0.5 + 20j]
        results = benchmark_methods(points, runs=2)
        # Schlüssel sind vorhanden
        assert "direct_times" in results
        assert "functional_times" in results
        assert "speedup_factors" in results
        assert "s_values" in results
        # Längen stimmen
        assert len(results["s_values"]) == len(points)
        assert len(results["direct_times"]) == len(points)
        assert len(results["functional_times"]) == len(points)
        assert len(results["speedup_factors"]) == len(points)
        # Speedup-Faktoren positiv
        assert all(f > 0 for f in results["speedup_factors"])


# Marker für langsame Benchmarks registrieren
pytestmark = pytest.mark.slow
