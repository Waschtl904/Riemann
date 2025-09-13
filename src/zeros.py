import mpmath as mp
from zeta import zeta  # Import der bereits existierenden zeta-Funktion

mp.mp.dps = 50


def find_zeros(count: int = 10):
    """
    Liefert die ersten `count` nicht-trivialen Nullstellen ζ(s)=0 auf der kritischen Linie.
    :param count: Anzahl der gewünschten Nullstellen.
    :return: Liste komplexer Nullstellen.
    """
    zeros = []
    for i in range(1, count + 1):
        rz = mp.zetazero(i)  # mpmath liefert direkt die i-te Nullstelle
        zeros.append(rz)
    return zeros
