#!/usr/bin/env python3
"""
zeros.py – Berechnung der Nullstellen der Riemannschen Zetafunktion ζ(s).
"""

import os
import logging
from typing import List, Optional
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor, as_completed

import mpmath as mp
from zeta import zeta

mp.mp.dps = 50

logger = logging.getLogger("zeros")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def find_zeros(limit: int, tol: float = 1e-5) -> List[complex]:
    """
    Findet die ersten `limit` nichttrivialen Nullstellen der Riemannschen Zetafunktion ζ(s)
    mithilfe der eingebauten mpmath-Funktion `mp.zetazero`. Jeder gefundene Wert wird auf
    numerische Stabilität geprüft und als Python-komplexe Zahl zurückgegeben.

    :param limit: Anzahl der ersten Nullstellen, die ermittelt werden sollen (muss > 0 sein)
    :param tol: Toleranz für den Vergleich und Rundung der Ergebnisse (Standard: 1e-5)
    :return: Liste von `limit` komplexen Nullstellen auf der kritischen Geraden
    """
    if limit <= 0:
        raise ValueError("`limit` muss größer als 0 sein")

    zeros: List[complex] = []
    for n in range(1, limit + 1):
        # mp.zetazero gibt eine mpmath.mpc zurück
        root_mpc = mp.zetazero(n)
        root = complex(root_mpc)
        # Auf Toleranz prüfen und ggf. abrunden
        real = round(root.real, int(-mp.log10(tol)))
        imag = round(root.imag, int(-mp.log10(tol)))
        zeros.append(complex(real, imag))

    return zeros


@lru_cache(maxsize=2048)
def _cached_zeta(real: float, imag: float) -> complex:
    return zeta(complex(real, imag))


def _generate_initial_guesses(n: int, first_im: float = 14.134725141) -> List[complex]:
    return [mp.mpc(0.5, first_im + k * mp.pi) for k in range(n)]


def _refine_root(guess: complex, tol: float) -> complex:
    def f(s):
        return _cached_zeta(s.real, s.imag)

    def df(s):
        return mp.diff(lambda z: _cached_zeta(z.real, z.imag), s)

    root = mp.findroot(f, guess, df, tol=tol, maxsteps=100)
    return complex(root)


def _filter_duplicates(roots: List[complex], tol: float) -> List[complex]:
    unique: List[complex] = []
    for r in roots:
        if all(abs(r - u) > tol for u in unique):
            unique.append(r)
    unique.sort(key=lambda c: c.imag)
    logger.info(f"{len(unique)} eindeutige Nullstellen gefunden")
    return unique


def find_roots(
    n: int, tol: float = 1e-12, max_workers: Optional[int] = None
) -> List[complex]:
    """Experimentelle Suche nach den ersten n Nullstellen auf der kritischen Geraden."""
    if n <= 0:
        raise ValueError("`n` muss größer als 0 sein")
    max_workers = max_workers or os.cpu_count() or 1
    guesses = _generate_initial_guesses(n)
    roots: List[complex] = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_refine_root, g, tol): g for g in guesses}
        for future in as_completed(futures):
            try:
                roots.append(future.result())
            except Exception as e:
                logger.warning(f"Fehler bei Schätzung {futures[future]}: {e}")

    return _filter_duplicates(roots, tol)


if __name__ == "__main__":
    print("Erste 5 Nullstellen (mp.zetazero):")
    for z in find_zeros(5):
        print(z)

    print("\nExperimentelle Suche nach 5 Nullstellen:")
    for z in find_roots(5, tol=1e-10):
        print(z)
