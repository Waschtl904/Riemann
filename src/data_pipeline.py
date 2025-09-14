# src/data_pipeline.py

import csv
import time
from pathlib import Path
from zeros import find_zeros
from explicit_formula import pi_explicit, riemann_psi
from prime_connection import generate_primes


def ensure_data_directory():
    """Stellt sicher, dass der data/-Ordner existiert."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir


def collect_zeros(max_imag_height, output_file="zeros.csv"):
    """
    Sammelt Nullstellen bis zur angegebenen Imaginärhöhe und speichert sie.
    """
    print(f"Sammle Nullstellen bis Imaginärhöhe {max_imag_height}...")
    start_time = time.time()

    zeros = find_zeros(max_imag_height)

    data_dir = ensure_data_directory()
    filepath = data_dir / output_file

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "real_part", "imag_part"])
        for i, zero in enumerate(zeros, 1):
            writer.writerow([i, float(zero.real), float(zero.imag)])

    elapsed = time.time() - start_time
    print(f"✓ {len(zeros)} Nullstellen in {elapsed:.2f}s gesammelt → {filepath}")
    return zeros


def compare_pi_methods(x_values, zeros, output_file="pi_comparison.csv"):
    """
    Vergleicht verschiedene π(x)-Berechnungsmethoden für gegebene x-Werte.
    """
    print(f"Vergleiche π(x)-Methoden für {len(x_values)} x-Werte...")
    start_time = time.time()

    data_dir = ensure_data_directory()
    filepath = data_dir / output_file

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "x",
                "pi_exact",
                "pi_approximation",
                "pi_explicit",
                "error_approx",
                "error_explicit",
                "num_zeros_used",
            ]
        )

        for x in x_values:
            if x < 2:
                continue

            # Exakte π(x) via Sieb
            primes = generate_primes(int(x))
            pi_exact = len(primes)

            # Standardnäherung x/log(x)
            import math

            pi_approx = x / math.log(x)

            # Explizitformel
            pi_expl_raw = pi_explicit(x, zeros)
            pi_expl = float(pi_expl_raw)  # mpmath -> float konvertieren

            # Fehler berechnen
            error_approx = abs(pi_exact - pi_approx)
            error_explicit = abs(pi_exact - pi_expl)

            writer.writerow(
                [
                    x,
                    pi_exact,
                    pi_approx,
                    pi_expl,
                    error_approx,
                    error_explicit,
                    len(zeros),
                ]
            )

            if len(x_values) <= 20:  # Detaillierte Ausgabe nur bei wenigen Werten
                print(
                    f"  x={x:6.0f}: π={pi_exact:4.0f}, "
                    f"Näherung={pi_approx:6.1f}, Explizit={pi_expl:6.1f}"
                )

    elapsed = time.time() - start_time
    print(f"✓ Vergleich abgeschlossen in {elapsed:.2f}s → {filepath}")


def build_dataset(max_zero_imag=20, x_values=None):
    """
    Hauptfunktion: Baut kompletten Datensatz auf.

    Args:
        max_zero_imag: Anzahl der zu berechnenden Nullstellen
        x_values: Liste der x-Werte für π(x)-Vergleich (default: geometrische Folge)
    """
    if x_values is None:
        # Geometrische Folge: 10, 20, 50, 100, 200, 500, 1000, 2000, 5000
        x_values = [10 * (2**i) for i in range(10)] + [
            10 * (5 * 2**i) for i in range(8)
        ]
        x_values = sorted(set(x_values))[:15]  # Erste 15 Werte nehmen

    print("=== Starte Daten-Pipeline ===")
    print(f"Parameter: max_zero_imag={max_zero_imag}, x_values={len(x_values)} Werte")

    # Schritt 1: Nullstellen sammeln
    zeros = collect_zeros(max_zero_imag)

    # Schritt 2: π(x)-Vergleiche durchführen
    compare_pi_methods(x_values, zeros)

    print("=== Pipeline abgeschlossen ===")
    print("Ergebnisse verfügbar in:")
    print("  - data/zeros.csv")
    print("  - data/pi_comparison.csv")


if __name__ == "__main__":
    # Beispielaufruf
    build_dataset(max_zero_imag=10, x_values=[10, 50, 100, 500, 1000])
