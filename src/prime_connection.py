# src/prime_connection.py

import math


def zeta_series(s, n_max):
    """Berechnet ζ(s) als Summe bis n_max."""
    return sum(1 / complex(n) ** s for n in range(1, n_max + 1))


def zeta_euler(s, p_list):
    """Berechnet ζ(s) als Produkt über Primliste p_list."""
    prod = 1
    for p in p_list:
        prod *= 1 / (1 - p ** (-s))
    return prod


def prime_error(x, primes):
    """
    Bestimmt die Abweichung der Primzahldichte π(x)
    gegenüber der Näherung x/log(x).
    primes: Liste aller p ≤ x
    """
    pi_x = len(primes)
    approx = x / math.log(x)
    return pi_x - approx


def generate_primes(n_max):
    """Einfache Sieb-Methode, liefert Liste aller Primzahlen ≤ n_max."""
    sieve = [True] * (n_max + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(n_max**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n_max + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]
