"""
riemann.zeta
Berechnung der Riemannschen Zetafunktion mit mpmath.
"""

import mpmath as mp

# Präzision auf 50 Dezimalstellen setzen
mp.mp.dps = 50


def zeta(s: complex) -> complex:
    """
    Berechnet die Riemannsche Zetafunktion ζ(s).
    :param s: Komplexe Zahl, z.B. 0.5 + 14.1347j
    :return: Wert von ζ(s) als komplexe Zahl
    """
    return mp.zeta(s)


if __name__ == "__main__":
    # Beispielaufruf: erste nicht-triviale Nullstelle
    s = 0.5 + 14.134725141734693j
    result = zeta(s)
    print(f"ζ({s}) = {result}")
