import sys, os

# src-Ordner zum Modulpfad hinzufügen
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import pytest
import numpy as np
from zeros_odlyzko import OdlyzkoConfig, OdlyzkoSchönhage, find_zeros_odlyzko
from fft_helpers import optimal_fft_length, FFTInterpolator
import mpmath as mp


class TestOdlyzkoBasics:
    """Grundlegende Tests für Odlyzko-Schönhage Implementierung"""

    def test_config_initialization(self):
        config = OdlyzkoConfig(T_start=10.0, T_end=20.0, precision=30)
        assert config.T_start == 10.0
        assert config.T_end == 20.0
        assert config.precision == 30
        assert config.T_mid == 15.0
        assert config.delta_T == 10.0

    def test_fft_length_calculation(self):
        length = optimal_fft_length(1000)
        assert isinstance(length, int)
        assert length >= 1000

    def test_siegel_theta_function(self):
        config = OdlyzkoConfig(T_start=14.0, T_end=15.0, precision=30)
        algo = OdlyzkoSchönhage(config)
        theta = algo.siegeltheta(14.134725)
        assert isinstance(theta, float)
        assert not np.isnan(theta) and not np.isinf(theta)


class TestOdlyzkoVsReference:
    """Vergleichstests gegen bekannte Referenzwerte"""

    def test_first_zeros_approximation(self):
        expected_zero = 14.134725  # erste Nullstelle
        zeros = find_zeros_odlyzko(10.0, 20.0, step=0.01, precision=30)
        assert any(
            abs(z - expected_zero) < 0.1 for z in zeros
        ), f"Keine Nullstelle nahe {expected_zero} gefunden (gefunden: {zeros})"

    def test_versus_mpmath_zetazero(self):
        mp.mp.dps = 15  # richtiger Zugriff auf mpmath-Präzision
        reference_zero_1 = float(mp.zetazero(1).imag)
        zeros = find_zeros_odlyzko(13.0, 16.0, step=0.01, precision=30)
        assert any(
            abs(z - reference_zero_1) < 0.01 for z in zeros
        ), f"Keine Nullstelle nahe mpmath-Referenz {reference_zero_1} gefunden (gefunden: {zeros})"


class TestFFTHelpers:
    def test_fft_interpolator(self):
        t_vals = np.linspace(0, 2 * np.pi, 32)
        grid_data = np.sin(t_vals)
        interpolator = FFTInterpolator(grid_data, delta=2 * np.pi / 32, t_start=0)
        interpolated = interpolator.interpolate(np.pi / 2)
        expected = np.sin(np.pi / 2)
        assert abs(interpolated - expected) < 0.1


class TestPerformance:
    @pytest.mark.slow
    def test_precomputation_speed(self):
        import time

        config = OdlyzkoConfig(T_start=100.0, T_end=105.0, precision=25)
        algo = OdlyzkoSchönhage(config)
        start_time = time.time()
        algo.precompute_grid()
        duration = time.time() - start_time
        assert duration < 60, "Grid-Vorbereitung zu langsam (>60s)"
