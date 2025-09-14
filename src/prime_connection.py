"""
prime_connection.py

Optimierte Funktionen zur Untersuchung der Zetafunktion ζ(s) und Primzahlnäherungen.

Features:
- Optionale Hochpräzision mit mpmath
- Reihen-, Euler‐Produkt‐ und Euler–Maclaurin‐Methoden
- Segmentierter Sieb mit LRU‐Cache
- Caching der Bernoulli‐Zahlen
- Logging statt Druckausgaben
- CLI‐Interface via argparse
"""

import argparse
import logging
import math
from functools import lru_cache
from typing import List, Optional, Tuple
from typing import Any

import numpy as np
from mpmath import mp, mpf, mpc

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _simple_sieve(limit: int) -> Tuple[int, ...]:
    """Einfacher Eratosthenes‐Sieb bis limit."""
    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    r = int(math.isqrt(limit))
    for i in range(2, r + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start : limit + 1 : step] = b"\x00" * (((limit - start) // step) + 1)
    return tuple(i for i, v in enumerate(sieve) if v)


@lru_cache(maxsize=None)
def generate_primes(n_max: int) -> List[int]:
    """
    Segmentierter Sieb zur Erzeugung aller Primzahlen ≤ n_max.

    Rückgabe:
        Liste[int]: Primzahlen bis n_max
    """
    if n_max < 2:
        return []
    limit = int(math.isqrt(n_max)) + 1
    base_primes = _simple_sieve(limit)
    primes = list(base_primes)
    segment_size = max(limit, 32768)
    low = limit
    while low <= n_max:
        high = min(low + segment_size - 1, n_max)
        segment = bytearray(b"\x01") * (high - low + 1)
        for p in base_primes:
            start = ((low + p - 1) // p) * p
            for j in range(start, high + 1, p):
                segment[j - low] = 0
        primes.extend(low + i for i, v in enumerate(segment) if v)
        low += segment_size
    logger.debug(f"generate_primes({n_max}) -> {len(primes)} primes")
    return primes


@lru_cache(maxsize=None)
def _bernoulli_number(n: int) -> Any:
    """Cached Bernoulli-Zahl B_n via mpmath."""
    return mp.bernoulli(n)


def zeta_series(s: complex, n_max: int, use_mpmath: bool = False) -> complex:
    """
    Partielle Reihen‐Summe ζ(s) ≈ ∑_{n=1}^{n_max} n^{-s}.
    Re(s)>1 für absolute Konvergenz.
    """
    if n_max < 1:
        raise ValueError("n_max muss ≥1 sein.")
    if use_mpmath:
        mp.mp.dps = max(mp.mp.dps, 50)
        s_mp = mpc(s)
        total = mpc(0)
        for n in range(1, n_max + 1):
            total += mp.power(mpf(n), -s_mp)
        return total
    arr = np.arange(1, n_max + 1, dtype=np.complex128)
    return np.sum(arr ** (-s))


def zeta_em(
    s: complex, n_max: int, bernoulli_terms: int = 4, use_mpmath: bool = False
) -> complex:
    """
    Euler–Maclaurin‐Korrektur für ζ(s):
      Partialsumme + Integral‐Term + Bernoulli‐Korrekturen.
    Für Re(s)≤1 use_mpmath=True empfohlen.
    """
    if n_max < 1:
        raise ValueError("n_max muss ≥1 sein.")
    if use_mpmath:
        mp.mp.dps = max(mp.mp.dps, 80)
        s_mp = mpc(s)
        partial = mpc(0)
        # partielle Summe
        for k in range(1, n_max + 1):
            partial += mp.power(mpf(k), -s_mp)
        term0 = mp.power(mpf(n_max), mpf(1) - s_mp) / (s_mp - mpf(1))
        term1 = mpf("0.5") * mp.power(mpf(n_max), -s_mp)
        correction = mpc(0)
        for k in range(1, bernoulli_terms + 1):
            B = _bernoulli_number(2 * k)
            denom = mp.factorial(2 * k)
            r = 2 * k - 1
            rf = mp.nprod(lambda i: s_mp + i, [0, r - 1])
            correction += (B / denom) * rf * mp.power(mpf(n_max), -s_mp - r + 1)
        return partial + term0 + term1 + correction
    # numpy-basiert
    partial = zeta_series(s, n_max, use_mpmath=False)
    s_c = complex(s)
    term0 = (n_max ** (1 - s_c)) / (s_c - 1)
    term1 = 0.5 * (n_max ** (-s_c))
    correction = 0 + 0j
    for k in range(1, bernoulli_terms + 1):
        B = complex(_bernoulli_number(2 * k))
        denom = math.factorial(2 * k)
        r = 2 * k - 1
        rf = complex(np.prod([s_c + i for i in range(r)]))
        correction += (B / denom) * rf * (n_max ** (-s_c - r + 1))
    return partial + term0 + term1 + correction


def zeta_euler(
    s: complex,
    primes: List[int],
    use_mpmath: bool = False,
    threshold: Optional[float] = None,
) -> complex:
    """
    Euler‐Produkt ζ(s) ≈ ∏_{p in primes} (1 - p^{-s})^{-1}.
    Re(s)>1.
    :param s: Komplexe Zahl, an der die Zetafunktion ausgewertet wird.
    :param primes: Liste der Primzahlen bis zum gewünschten Maximum.
    :param use_mpmath: Ob mpmath für hohe Präzision genutzt werden soll.
    :param threshold: Brich ab, wenn |factor - 1| < threshold.
    :return: Wert der Zetafunktion als complex.
    """
    prod = mpc(1) if use_mpmath else 1 + 0j

    if use_mpmath:
        mp.mp.dps = max(mp.mp.dps, 80)
        s_mp = mpc(s)
        for p in primes:
            p_pow = mp.power(mpf(p), s_mp)
            factor = 1 / (1 - (1 / p_pow))
            if threshold is not None and abs(factor - 1) < threshold:
                break
            prod *= factor
    else:
        for p in primes:
            p_pow = p ** complex(s)
            factor = 1 / (1 - 1 / p_pow)
            if threshold is not None and abs(factor - 1) < threshold:
                break
            prod *= factor

    return prod


def prime_error(x: float, primes: List[int], use_mpmath: bool = True) -> float:
    """
    Abweichung π(x) − li(x).
    Für höhere Präzision use_mpmath=True.
    """
    if x < 2:
        return 0.0
    pi_x = len(primes)
    if use_mpmath:
        mp.mp.dps = max(mp.mp.dps, 50)
        return float(pi_x - mp.li(mpf(x)))
    return float(pi_x - (x / math.log(x)))


def main():
    parser = argparse.ArgumentParser(description="prime_connection Demo und Tests")
    parser.add_argument("--max", type=int, default=100_000, help="Obergrenze n_max")
    parser.add_argument("--method", choices=["series", "em", "euler"], default="series")
    parser.add_argument("--s", type=complex, default=2 + 0j, help="Wert s für ζ(s)")
    parser.add_argument("--precision", type=int, default=50, help="mpmath mp.dps")
    args = parser.parse_args()

    mp.mp.dps = args.precision
    n = args.max
    s = args.s

    logger.info(f"Berechne ζ({s}) mit Methode {args.method} bis n_max={n}")
    if args.method == "series":
        result = zeta_series(s, n, use_mpmath=True)
    elif args.method == "em":
        result = zeta_em(s, n, use_mpmath=True)
    else:
        result = zeta_euler(s, n, use_mpmath=True)
    logger.info(f"Ergebnis: ζ({s}) ≈ {result}")

    primes = generate_primes(n)
    err = prime_error(float(n), primes, use_mpmath=True)
    logger.info(f"π({n}) − li({n}) = {err:.6f}")


if __name__ == "__main__":
    main()
