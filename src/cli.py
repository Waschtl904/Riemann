import argparse
from .zeta import zeta
from .utils import write_csv  # optional: Hilfsfunktion, um CSV zu erzeugen
from typing import Any


def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        prog="riemann",
        description="Berechnung der Riemannschen Zetafunktion für Bereiche im komplexen Feld",
    )
    parser.add_argument(
        "--start", type=complex, required=True, help="Startwert s im Format a+bj"
    )
    parser.add_argument(
        "--end", type=complex, required=True, help="Endwert s im Format a+bj"
    )
    parser.add_argument(
        "--step",
        type=float,
        default=1.0,
        help="Schrittweite für die Real- und Imaginärteile",
    )
    parser.add_argument(
        "--output", type=str, default="results.csv", help="CSV-Datei für die Ausgabe"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = []
    s = args.start
    while s.real <= args.end.real and s.imag <= args.end.imag:
        # zeta kann mpf-Typen intern nutzen, Any erlaubt Kompatibilität
        val = zeta(s)  # type: Any
        results.append((s, val))
        s = complex(s.real + args.step, s.imag + args.step)
    write_csv(results, args.output)
    print(f"Ergebnisse gespeichert in {args.output}")


if __name__ == "__main__":
    main()
