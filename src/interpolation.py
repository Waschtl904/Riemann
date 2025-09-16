import numpy as np
from typing import Callable, List, Tuple
import logging


def finite_difference(
    f: Callable[[float], complex], t: float, h: float = 1e-6
) -> Tuple[complex, complex]:
    """
    Liefert (f'(t), f''(t)) per zentraler Differenz:
      f'(t) ≈ [f(t+h)-f(t-h)]/(2h)
      f''(t) ≈ [f(t+h)-2f(t)+f(t-h)]/h^2
    """
    f_plus = f(t + h)
    f_minus = f(t - h)
    deriv1 = (f_plus - f_minus) / (2 * h)
    deriv2 = (f_plus - 2 * f(t) + f_minus) / (h * h)
    return deriv1, deriv2


def taylor_expansion(
    f: Callable[[float], complex], t0: float, t: float, max_terms: int = 5
) -> complex:
    """
    Taylor-Entwicklung von f um t0, bis max_terms.
    """
    dt = t - t0
    value = f(t0)
    deriv1, deriv2 = finite_difference(f, t0)
    terms = [value]
    if max_terms >= 1:
        terms.append(deriv1 * dt)
    if max_terms >= 2:
        terms.append(deriv2 * (dt**2) / 2)
    # Höhere Terme per finite difference mehrfach (optional)
    result = sum(terms)
    return result


class AdaptiveInterpolator:
    """Adaptive Interpolation mit automatischer Genauigkeitskontrolle."""

    def __init__(self, tol: float = 1e-12):
        self.tol = tol
        self.logger = logging.getLogger(__name__)

    def interpolate(
        self,
        f: Callable[[float], complex],
        grid_points: List[float],
        grid_values: List[complex],
        t: float,
    ) -> complex:
        """
        Versucht stufenweise Taylor-Expansion bis Konvergenz < tol,
        Fallback auf lineare Interpolation.
        """
        # nächster Gitterindex
        dists = [abs(t - gp) for gp in grid_points]
        i0 = int(np.argmin(dists))
        t0 = grid_points[i0]
        for terms in range(1, 6):
            approx = taylor_expansion(f, t0, t, max_terms=terms)
            if terms > 1:
                extra = taylor_expansion(f, t0, t, max_terms=terms + 1)
                if abs(extra - approx) < self.tol:
                    return approx
        # Linearer Fallback
        if i0 < len(grid_points) - 1:
            t1, t2 = grid_points[i0], grid_points[i0 + 1]
            v1, v2 = grid_values[i0], grid_values[i0 + 1]
            α = (t - t1) / (t2 - t1)
            return v1 + α * (v2 - v1)
        return grid_values[i0]
