import numpy as np
from scipy.fft import fft, ifft, next_fast_len
import logging


def optimal_fft_length(n: int) -> int:
    """
    Gibt die nächste performant effiziente FFT-Länge zurück.
    next_fast_len liefert garantiert einen int zurück.
    """
    return int(next_fast_len(n))


def compute_rational_evaluation_grid(
    coeffs: np.ndarray, roots_of_unity: np.ndarray
) -> np.ndarray:
    """
    Evaluiert Σ a_k/(ω_j - β_k) an Einheitswurzeln ω_j.
    coeffs: ndarray der Form [[a0, β0], [a1, β1], ...]
    roots_of_unity: ndarray komplexer Einheitswurzeln
    """
    coeffs_arr = np.asarray(coeffs, dtype=complex)
    roots_arr = np.asarray(roots_of_unity, dtype=complex)
    length = roots_arr.shape[0]
    results = np.zeros(length, dtype=complex)
    for idx in range(length):
        omega = roots_arr[idx]
        total = 0 + 0j
        for pair in coeffs_arr:
            a_k, beta_k = pair
            total += a_k / (omega - beta_k)
        results[idx] = total
    return results


def multi_fft_evaluation(data_matrix: np.ndarray, axis: int = -1) -> np.ndarray:
    """
    Führt mehrere FFTs in einem Array gleichzeitig aus.
    """
    array = np.asarray(data_matrix, dtype=complex)
    return fft(array, axis=axis)


class FFTInterpolator:
    """
    Band-limited Interpolation via Whittaker-Shannon.
    """

    def __init__(self, grid_data: np.ndarray, delta: float, t_start: float):
        self.grid_data = np.asarray(grid_data, dtype=complex)
        self.delta = float(delta)
        self.t_start = float(t_start)
        self.logger = logging.getLogger(__name__)
        if self.grid_data.size > 0:
            self._fft_data = fft(self.grid_data)
        else:
            self._fft_data = np.zeros((1,), dtype=complex)

    def interpolate(self, t: float) -> complex:
        """
        Interpoliert F(t) an beliebiger Stelle auf dem Grid.
        """
        t_val = float(t)
        x = (t_val - self.t_start) / self.delta if self.delta != 0 else 0.0
        # Vorher: n = self.grid_data.shape[0]
        n = len(self.grid_data)  # Vermeidet shape-Zugriff auf tuple
        if n == 0:
            return 0 + 0j
        if x < 0 or x >= n:
            self.logger.warning(f"t={t_val} außerhalb des Grid-Bereichs")
            if x < 0 and n > 1:
                slope = (self.grid_data[1] - self.grid_data[0]) / self.delta
                return self.grid_data[0] + slope * (t_val - self.t_start)
            if n > 1:
                end_t = self.t_start + (n - 1) * self.delta
                slope = (self.grid_data[-1] - self.grid_data[-2]) / self.delta
                return self.grid_data[-1] + slope * (t_val - end_t)
            return self.grid_data[0]

        pad = 2 * n
        freq = np.zeros(pad, dtype=complex)
        half = n // 2
        fft_data = (
            self._fft_data
            if hasattr(self._fft_data, "__len__")
            else np.zeros(n, dtype=complex)
        )
        freq[:half] = fft_data[:half]
        freq[-half:] = fft_data[half:]
        vals = ifft(freq) * 2
        idx = int(round(x * 2))
        if 0 <= idx < len(vals):
            return vals[idx]
        return self.grid_data[-1]
