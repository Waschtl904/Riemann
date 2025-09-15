import argparse
from typing import Any

from zeta import zeta
from utils import write_csv
from riemann_siegel import find_zeros_riemann_siegel


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

    # Standard-Befehl: ζ(s)-Berechnung
    results = []
    s = args.start
    while s.real <= args.end.real and s.imag <= args.end.imag:
        val = zeta(s)  # type: Any
        results.append((s, val))
        s = complex(s.real + args.step, s.imag + args.step)

    write_csv(results, args.output)
    print(f"Ergebnisse gespeichert in {args.output}")


if __name__ == "__main__":
    main()
