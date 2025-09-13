import math
import matplotlib.pyplot as plt
from prime_connection import zeta_series, zeta_euler, generate_primes, prime_error


def plot_euler_vs_series(s_real, imag_list, p_max, n_max):
    """Vergleich Serie vs. Euler-Produkt für s = s_real + i·b."""
    primes = generate_primes(p_max)
    results = []
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


def plot_prime_distribution(x_max):
    """Primzahldichte vs. x/log(x) und deren Differenz."""
    primes = generate_primes(x_max)
    xs = list(range(2, x_max + 1, max(1, x_max // 100)))
    pi_vals = [len([p for p in primes if p <= x]) for x in xs]
    approx = [x / math.log(x) for x in xs]
    plt.figure(figsize=(10, 4))
    plt.plot(xs, pi_vals, label="π(x)")
    plt.plot(xs, approx, label="x/log(x)", linestyle="--")
    plt.legend()
    plt.title("Primzahldichte vs. Näherung")
    plt.show()
