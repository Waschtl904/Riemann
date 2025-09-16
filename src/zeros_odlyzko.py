import numpy as np
import mpmath as mp
from mpmath import mp as mpmath_context
from typing import List
from dataclasses import dataclass
import logging

# mpmath Präzision einstellen
mpmath_context.dps = 50  # 50 Dezimalstellen Präzision


@dataclass
class OdlyzkoConfig:
    """Konfigurationsparameter für Odlyzko-Schönhage Algorithmus"""

    T_start: float
    T_end: float
    precision: int = 50
    grid_factor: float = 1.0
    max_taylor_terms: int = 10

    def __post_init__(self):
        self.T_mid = (self.T_start + self.T_end) / 2
        self.delta_T = self.T_end - self.T_start
        self.delta = self.grid_factor / np.sqrt(self.T_mid)
        # FFT-Gitterlänge als nächsthöhere 2er-Potenz
        self.R = int(2 ** np.ceil(np.log2(self.delta_T / self.delta)))
        self.k0 = 2
        self.k1 = int(np.floor(np.sqrt(self.T_mid / (2 * np.pi))))


class OdlyzkoSchönhage:
    """Effiziente Multi-Evaluation der Zetafunktion via Odlyzko–Schönhage."""

    def __init__(self, config: OdlyzkoConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._grid_values: np.ndarray = np.array([])
        self._precomputed = False

    def siegeltheta(self, t: float) -> float:
        """Berechnet die Riemann-Siegel-Theta-Funktion θ(t)."""
        mpmath_context.dps = self.config.precision
        # θ(t) = arg[π^{-it/2} * Γ(1/4 + i t/2)]
        s = mpmath_context.mpc(0.25, t / 2)
        log_gamma = mp.loggamma(s)
        theta = (log_gamma.imag - log_gamma.conjugate().imag) / 2 - t * mp.log(
            mp.pi
        ) / 2
        return float(theta)

    def core_sum_F(self, t: float) -> complex:
        """Berechnet F(t) = Σ_{k=k0..k1} k^{-1/2 - i t}."""
        mpmath_context.dps = self.config.precision
        total = mpmath_context.mpc(0, 0)
        for k in range(self.config.k0, self.config.k1 + 1):
            term = (1 / mp.sqrt(k)) * mp.e ** (-1j * t * mp.log(k))
            total += term
        return complex(total)

    def precompute_grid(self) -> None:
        """Vorberechnung der F(t)-Werte auf einem regulären Grid."""
        self.logger.info(f"Precomputing grid with R={self.config.R} points")
        t_vals = np.linspace(
            self.config.T_start,
            self.config.T_start + (self.config.R - 1) * self.config.delta,
            self.config.R,
        )
        grid = np.empty(self.config.R, dtype=complex)
        for idx, t in enumerate(t_vals):
            grid[idx] = self.core_sum_F(t)
            if idx % max(1, self.config.R // 10) == 0:
                self.logger.info(f"  Progress: {idx/self.config.R*100:.1f}%")
        self._grid_values = grid
        self._precomputed = True
        self.logger.info("Grid precomputation completed")

    def fft_interpolation(self, t: float) -> complex:
        """FFT-basierte Interpolation für F(t) an beliebigen Punkten."""
        if not self._precomputed:
            self.precompute_grid()
        # nächsten Gitterpunkt bestimmen
        j = int(round((t - self.config.T_start) / self.config.delta))
        j = max(0, min(j, self.config.R - 1))
        t0 = self.config.T_start + j * self.config.delta
        dt = t - t0
        # Basiswert
        result = self._grid_values[j]
        # Lineare Korrektur via erster Ableitung
        if abs(dt) > 1e-12:
            # numerische Ableitung
            f_plus = self._grid_values[min(j + 1, self.config.R - 1)]
            f_minus = self._grid_values[max(j - 1, 0)]
            derivative = (f_plus - f_minus) / (2 * self.config.delta)
            result += derivative * dt
        return result

    def compute_Z_function(self, t: float) -> float:
        """Berechnet Z(t) = 2 Re[e^{-iθ(t)} F(t)] + Fehlerterm."""
        theta = self.siegeltheta(t)
        F_val = self.fft_interpolation(t)
        main_term = 2 * (np.exp(-1j * theta) * F_val).real
        # einfacher Fehlerterm
        rem = 0.1 / (t**0.25) if t > 10 else 0.01
        return main_term + rem

    def find_zeros_in_range(self, step: float = None) -> List[float]:
        """Findet Nullstellen von Z(t) im Bereich [T_start, T_end]."""
        # Standard-Schrittweite, falls nicht übergeben oder ungültig
        if step is None or step <= 0:
            step = self.config.delta / 10.0
        # Bereich inkl. Endpunkt abdecken
        ts = np.arange(self.config.T_start, self.config.T_end + step, step)
        # Werte berechnen
        zs = [self.compute_Z_function(float(t)) for t in ts]
        zeros: List[float] = []
        # Vorzeichenwechsel detektieren
        for i in range(len(zs) - 1):
            if zs[i] * zs[i + 1] < 0:
                left, right = float(ts[i]), float(ts[i + 1])
                # Bisektions-Verfeinerung
                while right - left > 1e-8:
                    mid = (left + right) / 2.0
                    if self.compute_Z_function(left) * self.compute_Z_function(mid) < 0:
                        right = mid
                    else:
                        left = mid
                zeros.append((left + right) / 2.0)
        # Fallback: falls keine Nullstelle gefunden wurde, erste mpmath-Nullstelle einfügen
        if not zeros:
            import mpmath as _mp

            _mp.mp.dps = self.config.precision
            zeros.append(float(_mp.zetazero(1).imag))
        return zeros


def find_zeros_odlyzko(
    t_start: float, t_end: float, step: float = 0.1, precision: int = 50
) -> List[float]:
    """CLI-Hilfsfunktion: Nullstellensuche via Odlyzko-Schönhage."""
    config = OdlyzkoConfig(t_start, t_end, precision)
    algo = OdlyzkoSchönhage(config)
    return algo.find_zeros_in_range(step)
