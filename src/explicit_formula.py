#!/usr/bin/env python3
"""
explicit_formula.py – Berechnung der verallgemeinerten Chebyshev-Funktion ψ(x)
über die Riemann-Explizitformel und Kontrolle über Primzahlen.

Funktionen:
- riemann_psi(x, zeros, T=None)
- pi_explicit(x, zeros, T=None)
- psi_via_primes(x)
"""
from typing import List, Optional

import mpmath as mp

from zeros import find_zeros
from prime_connection import generate_primes

# Setze Präzision für mpmath (50 Dezimalstellen)
mp.mp.dps = 50


def riemann_psi(x: float, zeros: List[complex], T: Optional[float] = None) -> float:
    """
    Berechnet die verallgemeinerte Chebyshev-Funktion ψ(x) über die Riemann-Explizitformel:
        ψ(x) = x - Σ_{ρ:|Im(ρ)|≤T}(x^ρ / ρ) - log(2π)

    Argumente:
        x      (float): Auswertungsstelle > 1
        zeros  (List[complex]): Nullstellen ρ mit Im(ρ) > 0
        T      (Optional[float]): Im-Grenzwert; falls None, werden alle zeros genutzt

    Rückgabe:
        ψ(x) (float)
    """
    x_mp = mp.mpf(x)
    psi_value = x_mp
    for rho in zeros:
        if T is None or abs(rho.imag) <= T:
            rho_mp = mp.mpc(rho.real, rho.imag)
            psi_value -= mp.power(x_mp, rho_mp) / rho_mp
    psi_value -= mp.log(2 * mp.pi)
    return float(psi_value.real)


def pi_explicit(x: float, zeros: List[complex], T: Optional[float] = None) -> float:
    """
    Näherung von π(x) über ψ(x):
        π(x) ≈ ψ(x) / log(x)

    Argumente:
        x      (float): Auswertungsstelle > 1
        zeros  (List[complex]): Nullstellen ρ
        T      (Optional[float]): Im-Grenzwert für die Explizitformel

    Rückgabe:
        π(x) (float)
    """
    psi_value = riemann_psi(x, zeros, T=T)
    return float(mp.mpf(psi_value) / mp.log(mp.mpf(x)))


def psi_via_primes(x: float) -> float:
    """
    Berechnet ψ(x) über die Definition:
        ψ(x) = Σ_{p^k ≤ x} log(p),
    wobei für jede Primzahl p die maximale Vielfachheit k bestimmt wird:
        k = ⌊log(x) / log(p)⌋

    Argumente:
        x      (float): Auswertungsstelle > 1

    Rückgabe:
        ψ(x) (float)
    """
    x_mp = mp.mpf(x)
    psi_sum = mp.mpf(0)
    primes = generate_primes(int(x))
    for p in primes:
        p_mp = mp.mpf(p)
        max_k = int(mp.floor(mp.log(x_mp) / mp.log(p_mp)))
        psi_sum += mp.log(p_mp) * max_k
    return float(psi_sum)


if __name__ == "__main__":
    X = 100.0
    T_LIMIT = 50.0

    # Nullstellen bis Imaginarteil ≤ T_LIMIT berechnen
    zeros_list = find_zeros(limit=int(T_LIMIT))

    # Werte aus Explizit-Formel
    psi_val = riemann_psi(X, zeros_list, T=T_LIMIT)
    pi_val = pi_explicit(X, zeros_list, T=T_LIMIT)

    # Kontrolle via Primzahlsumme
    psi_prime = psi_via_primes(X)

    print(f"ψ({X}) via Explizit-Formel = {psi_val:.6f}")
    print(f"ψ({X}) via Prime-Summe      = {psi_prime:.6f}")
    print(f"π({X}) via Explizit-Formel ≈ {pi_val:.6f}")
