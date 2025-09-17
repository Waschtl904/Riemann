import argparse
from typing import Any, List, Tuple

from zeta import zeta
from utils import write_csv
from riemann_siegel import find_zeros_riemann_siegel
from zeros_odlyzko import find_zeros_odlyzko
from functional_equation import zeta_via_functional, zeta_complete
from spectral_analysis import load_spacings, spectrum_of_spacings
import numpy as np
import matplotlib.pyplot as plt


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="riemann",
        description="Berechnung der Riemannschen Zetafunktion und Nullstellensuche",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Subparser für Zetafunktion-Berechnung
    compute = subparsers.add_parser(
        "compute", help="Berechnung von ζ(s) über einen Bereich"
    )
    compute.add_argument(
        "--start", type=complex, required=True, help="Startwert s im Format a+bj"
    )
    compute.add_argument(
        "--end", type=complex, required=True, help="Endwert s im Format a+bj"
    )
    compute.add_argument(
        "--step",
        type=float,
        default=1.0,
        help="Schrittweite für die Real- und Imaginärteile",
    )
    compute.add_argument(
        "--output", type=str, default="results.csv", help="CSV-Datei für die Ausgabe"
    )

    # Subparser für Riemann-Siegel-Nullstellensuche
    siegel = subparsers.add_parser(
        "siegel", help="Nullstellensuche via Riemann-Siegel-Formel"
    )
    siegel.add_argument("--t-start", type=float, required=True, help="Start t-Wert")
    siegel.add_argument("--t-end", type=float, required=True, help="Ende t-Wert")
    siegel.add_argument("--step", type=float, default=0.1, help="Abtast-Schrittweite")
    siegel.add_argument("--precision", type=int, default=50, help="mpmath-Präzision")
    siegel.add_argument(
        "--output", type=str, default="zeros.csv", help="CSV-Datei für Nullstellen"
    )

    # Subparser für Odlyzko–Schönhage-Algorithmus
    odlyzko = subparsers.add_parser(
        "odlyzko", help="Nullstellensuche via Odlyzko–Schönhage-Algorithmus"
    )
    odlyzko.add_argument("--t-start", type=float, required=True, help="Start t-Wert")
    odlyzko.add_argument("--t-end", type=float, required=True, help="Ende t-Wert")
    odlyzko.add_argument(
        "--precision", type=int, default=50, help="mpmath-Präzision für FFT"
    )
    odlyzko.add_argument(
        "--output",
        type=str,
        default="zeros_odlyzko.csv",
        help="CSV-Datei für Nullstellen",
    )

    # Subparser für Functional Equation
    func = subparsers.add_parser(
        "compute-func", help="Berechnung von ζ(s) über funktionale Gleichung"
    )
    func.add_argument(
        "--s", type=complex, required=True, help="Stelle s im Format a+bj"
    )
    func.add_argument(
        "--method",
        type=str,
        choices=["direct", "functional", "auto"],
        default="auto",
        help="Auswertungsmethode",
    )

    # Subparser für Spektralanalyse
    spectrum = subparsers.add_parser(
        "analyze-spectrum", help="Spektralanalyse der Nullstellenabstände"
    )
    spectrum.add_argument(
        "--input",
        type=str,
        required=True,
        help="CSV-Datei mit Spalte 't' für Imaginärteile",
    )
    spectrum.add_argument(
        "--fs", type=float, default=1.0, help="Sampling-Frequenz für PSD"
    )
    spectrum.add_argument(
        "--nperseg", type=int, default=256, help="Segmentlänge für Welch-Methode"
    )
    spectrum.add_argument("--plot", action="store_true", help="PSD-Plot anzeigen")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "siegel":
        zeros = find_zeros_riemann_siegel(
            args.t_start, args.t_end, step=args.step, precision=args.precision
        )
        write_csv([(z, 0) for z in zeros], args.output)
        print(f"Nullstellen gespeichert in {args.output}")
        return

    if args.command == "odlyzko":
        zeros = find_zeros_odlyzko(
            args.t_start, args.t_end, precision=args.precision, output=args.output
        )
        write_csv([(z, 0) for z in zeros], args.output)
        print(f"Nullstellen (Odlyzko) gespeichert in {args.output}")
        return

    if args.command == "compute-func":
        s = args.s
        if args.method == "direct":
            result = zeta(s)
        elif args.method == "functional":
            result = zeta_via_functional(s)
        else:
            result = zeta_complete(s)
        print(f"ζ({s}) = {result}")
        return

    if args.command == "analyze-spectrum":
        spacings = load_spacings(args.input)
        f, Pxx = spectrum_of_spacings(spacings, fs=args.fs, nperseg=args.nperseg)
        if args.plot:
            plt.semilogy(f, Pxx)
            plt.xlabel("Frequenz")
            plt.ylabel("PSD")
            plt.title("Power Spectral Density der Nullstellenabstände")
            plt.show()
        else:
            write_csv(list(zip(f, Pxx)), "spectrum.csv")
            print("Spektraldaten gespeichert in spectrum.csv")
        return

    # Standard-Befehl: ζ(s)-Berechnung über Bereich
    results: List[Tuple[complex, complex]] = []
    s = args.start
    while s.real <= args.end.real and s.imag <= args.end.imag:
        val = zeta(s)
        results.append((s, val))
        s = complex(s.real + args.step, s.imag + args.step)

    write_csv(results, args.output)
    print(f"Ergebnisse gespeichert in {args.output}")


if __name__ == "__main__":
    main()
