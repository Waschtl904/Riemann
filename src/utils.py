import math
import csv
import matplotlib.pyplot as plt
from typing import List, Tuple, Any
from .prime_connection import zeta_series, zeta_euler, generate_primes, prime_error


def plot_euler_vs_series(
    s_real: float, imag_list: List[float], p_max: int, n_max: int
) -> None:
    """Vergleich Serie vs. Euler-Produkt für s = s_real + i·b."""
    primes: List[int] = generate_primes(p_max)
    results: List[Tuple[float, float]] = []
    for b in imag_list:
        s = complex(s_real, b)
        series = zeta_series(s, n_max)
        euler = zeta_euler(s, primes)
        results.append((b, abs(series - euler)))
    bs, diffs = zip(*results)
    plt.figure()
    plt.plot(bs, diffs, marker="o")
    plt.xlabel("Imaginärteil b")
    plt.ylabel("|ζ_series–ζ_euler|")
    plt.title(f"Abweichung bei Re(s)={s_real}")
    plt.show()


def plot_prime_distribution(x_max: int) -> None:
    """Primzahldichte vs. x/log(x) und deren Differenz."""
    primes: List[int] = generate_primes(x_max)
    xs = list(range(2, x_max + 1, max(1, x_max // 100)))
    pi_vals = [len([p for p in primes if p <= x]) for x in xs]
    approx = [x / math.log(x) for x in xs]
    plt.figure(figsize=(10, 4))
    plt.plot(xs, pi_vals, label="π(x)")
    plt.plot(xs, approx, label="x/log(x)", linestyle="--")
    plt.legend()
    plt.title("Primzahldichte vs. Näherung")
    plt.show()


def save_pi_error_plot(pi_df: Any, output_path: str) -> None:
    """
    Speichert den Fehlervergleich der π(x)-Methoden als Bild.
    pi_df: DataFrame mit Spalten 'x', 'error_approx', 'error_explicit'
    output_path: Pfad zur Ausgabedatei (z.B. 'data/pi_error_plot.png')
    """
    plt.figure(figsize=(8, 5))
    plt.loglog(pi_df["x"], pi_df["error_approx"], label="x/log(x)")
    plt.loglog(pi_df["x"], pi_df["error_explicit"], label="Explizitformel")
    plt.xlabel("x")
    plt.ylabel("Fehler")
    plt.title("Fehlervergleich der π(x)-Methoden")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig(output_path)
    plt.close()


def write_csv(data: List[Tuple[complex, Any]], filename: str) -> None:
    """Speichert eine Liste von (s, ζ(s))-Paaren als CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["s", "zeta(s)"])
        for s, val in data:
            writer.writerow([f"{s.real}+{s.imag}j", str(val)])
