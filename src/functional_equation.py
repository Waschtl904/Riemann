"""
functional_equation.py

Implementierung der Zeta-Symmetrietransformation über die funktionale Gleichung:
ζ(s) = 2^s π^(s−1) sin(π s/2) Γ(1−s) ζ(1−s)

Bietet sowohl direkte Anwendung der funktionalen Gleichung als auch automatische
Methodenwahl basierend auf dem Imaginärteil von s.
"""

import mpmath as mp
from typing import Union
from zeta import zeta

__all__ = ["zeta_via_functional", "zeta_complete", "benchmark_methods"]


def zeta_via_functional(s: Union[complex, float]) -> complex:
    """
    Berechnet ζ(s) mithilfe der funktionalen Gleichung:
    ζ(s) = 2^s π^(s−1) sin(π s/2) Γ(1−s) ζ(1−s)

    Args:
        s: Komplexe Zahl oder float

    Returns:
        Wert der Zetafunktion als complex

    Note:
        Besonders effizient für |Im(s)| > 50
    """
    s = complex(s)  # Sicherstellen, dass s komplex ist

    # Berechnung der Faktoren
    factor_2s = 2**s
    factor_pi = mp.pi ** (s - 1)
    factor_sin = mp.sin(mp.pi * s / 2)
    factor_gamma = mp.gamma(1 - s)

    # Funktionale Gleichung anwenden
    prefactor = factor_2s * factor_pi * factor_sin * factor_gamma
    zeta_1_minus_s = zeta(1 - s)

    return complex(prefactor * zeta_1_minus_s)


def zeta_complete(s: Union[complex, float], threshold: float = 50.0) -> complex:
    """
    Wählt automatisch die effizienteste Auswertungsmethode:
    - Für |Im(s)| ≥ threshold: funktionale Gleichung
    - Für |Im(s)| < threshold: direkte zeta(s)-Berechnung

    Args:
        s: Komplexe Zahl oder float
        threshold: Schwellwert für Methodenwahl (default: 50.0)

    Returns:
        Wert der Zetafunktion als complex
    """
    s = complex(s)

    if abs(s.imag) >= threshold:
        return zeta_via_functional(s)
    else:
        return zeta(s)


def benchmark_methods(s_values: list, runs: int = 3) -> dict:
    """
    Vergleicht Laufzeiten zwischen direkter Berechnung und funktionaler Gleichung.

    Args:
        s_values: Liste von komplexen Zahlen zum Testen
        runs: Anzahl der Durchläufe für Mittelwertbildung

    Returns:
        Dictionary mit Benchmark-Ergebnissen
    """
    import time

    results = {
        "direct_times": [],
        "functional_times": [],
        "s_values": s_values,
        "speedup_factors": [],
    }

    for s in s_values:
        # Direkte Methode
        direct_times = []
        for _ in range(runs):
            start = time.time()
            zeta(s)
            direct_times.append(time.time() - start)
        avg_direct = sum(direct_times) / len(direct_times)

        # Funktionale Gleichung
        func_times = []
        for _ in range(runs):
            start = time.time()
            zeta_via_functional(s)
            func_times.append(time.time() - start)
        avg_func = sum(func_times) / len(func_times)

        results["direct_times"].append(avg_direct)
        results["functional_times"].append(avg_func)
        results["speedup_factors"].append(
            avg_direct / avg_func if avg_func > 0 else float("inf")
        )

    return results


def validate_functional_equation(
    s: Union[complex, float], tolerance: float = 1e-10
) -> tuple:
    """
    Validiert die funktionale Gleichung durch Vergleich beider Methoden.

    Args:
        s: Zu testende komplexe Zahl
        tolerance: Toleranz für Gleichheitsprüfung

    Returns:
        Tuple (is_valid, direct_result, functional_result, error)
    """
    s = complex(s)

    # Beide Methoden ausführen und in built-in complex umwandeln
    direct_raw = zeta(s)
    functional_raw = zeta_via_functional(s)
    direct = complex(direct_raw)
    functional = complex(functional_raw)

    # Fehler berechnen
    error = abs(direct - functional)
    is_valid = error < tolerance

    return is_valid, direct, functional, error
