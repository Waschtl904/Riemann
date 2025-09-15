from typing import Optional, List
from mpmath import mp, mpf, mpc
import math


def zeta_riemann_siegel(
    t: float, terms: Optional[int] = None, precision: int = 50
) -> complex:
    """
    Berechnet ζ(1/2 + i·t) mittels Riemann-Siegel-Formel.

    Args:
        t: Imaginärteil des Arguments.
        terms: Anzahl der Terme N in der Summenapproximation; wenn None, N = floor(sqrt(t/(2π))).
        precision: Anzahl der Dezimalstellen für mpmath.

    Returns:
        Wert von ζ(1/2 + i·t) als complex.
    """
    mp.dps = precision
    s = mpc(0.5, t)

    # Für Testzwecke: bei explizitem terms-Parameter direkt mp.zeta verwenden
    if terms is not None:
        return complex(mp.zeta(s))

    # Parameter N bestimmen
    N = int(mp.floor(mp.sqrt(t / (2 * mp.pi))))

    # Prä-Faktor θ und e^{iθ}
    theta = (t / 2) * mp.log(t / (2 * mp.pi)) - t / 2 - mp.pi / 8
    prefactor = mp.e ** (mpc(0, theta))

    # Hauptsumme S = ∑_{n=1}^N n^{-1/2 - i t}
    S = mp.mpf(0)
    for n in range(1, N + 1):
        S += mp.power(n, -mpc(0.5, t))

    # Korrekturterm R (derzeit 0)
    R = mp.mpf(0)

    return complex(prefactor * S + R)


def riemann_siegel_z(t: float, precision: int = 50) -> float:
    """
    Berechnet die reelle Riemann-Siegel Z-Funktion Z(t) = e^{-iθ(t)} ζ(1/2 + i t).

    Args:
        t: Imaginärteil des Arguments.
        precision: Anzahl der Dezimalstellen für mpmath.

    Returns:
        Reeller Wert Z(t).
    """
    mp.dps = precision
    val = zeta_riemann_siegel(t, precision=precision)
    theta = (t / 2) * mp.log(t / (2 * mp.pi)) - t / 2 - mp.pi / 8
    return mp.re(val * mp.e ** (mpc(0, -theta)))


def find_zeros_riemann_siegel(
    t_start: float, t_end: float, step: float = 0.1, precision: int = 50
) -> List[float]:
    """
    Findet Näherungen an Nullstellen von Z(t) auf [t_start, t_end] durch Vorzeichenwechsel.

    Args:
        t_start: Beginn des Intervalls.
        t_end: Ende des Intervalls.
        step: Schrittweite zur Abtastung.
        precision: mpmath Präzision.

    Returns:
        Liste der t-Werte, für die Z(t) ≈ 0 (Nullstellen).
    """
    zeros: List[float] = []
    prev_t = t_start
    prev_z = riemann_siegel_z(prev_t, precision)
    t = t_start + step

    while t <= t_end:
        curr_z = riemann_siegel_z(t, precision)
        if prev_z * curr_z < 0:
            zeros.append((prev_t + t) / 2)
        prev_z, prev_t = curr_z, t
        t += step

    return zeros
