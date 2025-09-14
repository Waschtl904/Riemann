import mpmath as mp
from zeta import zeta  # Import der bereits existierenden zeta-Funktion

mp.mp.dps = 50


def find_zeros(limit: int, tol: float = 1e-6):
    """
    Liefert die ersten Nullstellen ζ(s)=0 mit Im(ρ) ≤ limit.
    :param limit: Anzahl oder Höhe der Imaginärteile (je nach Bedarf)
    :param tol: Genauigkeit für mpmath
    """
    zeros = []
    # Beispiel: mpmath liefert gezielt die i-te Nullstelle,
    # hier müssten Sie wählen, wie Sie limit interpretieren.
    for i in range(1, limit + 1):
        rz = mp.zetazero(i)
        zeros.append(rz)
    return zeros
