# src/explicit_formula.py

import math
from zeros import find_zeros
from prime_connection import generate_primes


def riemann_psi(x, zeros, T=None):
    """
    Berechnet die verallgemeinerte Chebyshev-Funktion ψ(x) über die Riemann-Explizitformel:
        ψ(x) = x - Σ_{ρ:|Im(ρ)|≤T}(x^ρ/ρ) - log(2π)
    Argumente:
        x     (float): Auswertungsstelle >1
        zeros (list of complex): Nullstellen ρ mit Im(ρ)>0
        T     (float): optionaler Im-Grenzwert; falls None, werden alle übergebenen zeros genutzt
    Rückgabe:
        ψ (float)
    """
    # Hauptterm
    psi = x
    # Summe über Nullstellen
    for rho in zeros:
        if T is None or abs(rho.imag) <= T:
            psi -= x**rho / rho
    # Konstante
    psi -= math.log(2 * math.pi)
    return psi.real


def pi_explicit(x, zeros, T=None):
    """
    Näherung von π(x) über ψ(x):
        π(x) ≈ ψ(x) / log(x)
    Argumente:
        x     (float): Auswertungsstelle >1
        zeros (list of complex): Nullstellen ρ
        T     (float): optionaler Im-Grenzwert für die Explizitformel
    Rückgabe:
        pi (float)
    """
    psi = riemann_psi(x, zeros, T)
    return psi / math.log(x)


# Hilfsfunktion: Nullstellen bis Höhe T berechnen (vereinfachtes Beispiel)
def find_zeros(limit, tol=1e-6):
    """
    Platzhalterfunktion: Liefert eine Liste erster nicht-trivialer Nullstellen ρ
    mit Im(ρ) > 0 bis Im(ρ) ≤ limit.
    In einer realen Implementierung würde man hier Kontur­integration oder
    Newton-Verfahren auf ζ(s) einsetzen.
    """
    # Beispielwerte (paar erste Nullstellen)
    example = [
        0.5 + 14.134725j,
        0.5 + 21.022040j,
        0.5 + 25.010858j,
        0.5 + 30.424876j,
    ]
    return [rho for rho in example if rho.imag <= limit]
