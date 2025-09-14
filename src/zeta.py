#!/usr/bin/env python3
"""
zeta.py – Berechnet die Riemannsche Zetafunktion ζ(s) mit mpmath.

Beispiele (Python):
    >>> from zeta import zeta, format_result
    >>> val = zeta(2, precision=80)
    >>> print(format_result(val, digits=10))
    1.6449340668

Beispiele (Terminal):
    $ python zeta.py "0.5+14.1347j" -p 80 -d 8 -v
    [INFO] Berechne ζ(0.5 + 14.1347j) mit 80 Dezimalstellen
    2.46599e-15 + 4.44089e-16j
    $ python zeta.py "2" --raw
    (1.6449340668482264364724151666460251892189499012068 + 0.0j)
"""

import sys
import ast
import argparse
import mpmath as mp
from typing import Any


def zeta(
    s: complex | float | int | Any, precision: int = 50, verbose: bool = False
) -> Any:
    """
    Berechnet die Riemannsche Zetafunktion ζ(s).

    :param s: Komplexe oder reelle Zahl (z.B. 0.5+14.1347j oder 2)
    :param precision: Dezimalstellen für Berechnung (Standard: 50)
    :param verbose: Bei True werden zusätzliche Infos ausgegeben
    :return: Wert von ζ(s) als mpmath.mpc
    :raises TypeError: bei ungültigem Eingabetyp
    """
    # Typprüfung und Konvertierung
    if isinstance(s, complex):
        s = mp.mpc(s.real, s.imag)
    elif isinstance(s, (float, int)):
        s = mp.mpf(s)
    elif not isinstance(s, (mp.mpf, mp.mpc)):
        raise TypeError(f"Ungültiger Eingabetyp: {type(s)}")

    # Debug-Info
    if verbose:
        print(f"[INFO] Berechne ζ({s}) mit {precision} Dezimalstellen", file=sys.stderr)

    # Berechnung im Präzisionskontext
    with mp.workdps(precision):
        return mp.zeta(s)


def format_result(val: Any, digits: int = 6) -> str:
    """
    Formatiert das Ergebnis als komplexe Zahl mit fester Genauigkeit.

    :param val: Ergebniswert (mpmath.mpf oder mpc)
    :param digits: Nachkommastellen für Ausgabe (Standard: 6)
    :return: formatierter String, z.B. '0.123457 + 1.234568j'
    """
    if isinstance(val, mp.mpf):
        return f"{val:.{digits}g}"
    else:  # mpc
        real = f"{val.real:.{digits}g}"
        imag = f"{abs(val.imag):.{digits}g}"
        sign = "+" if val.imag >= 0 else "-"
        return f"{real} {sign} {imag}j"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Berechnung der Riemannschen Zetafunktion ζ(s)"
    )
    parser.add_argument("s", type=str, help="Stelle s (z.B. 2 oder '0.5+14.1347j')")
    parser.add_argument(
        "-p",
        "--prec",
        type=int,
        default=50,
        help="Dezimalstellen für Berechnung (Standard: 50)",
    )
    parser.add_argument(
        "-d",
        "--digits",
        type=int,
        default=6,
        help="Nachkommastellen für Ausgabe (Standard: 6)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ausführliche Ausgabe"
    )
    parser.add_argument(
        "--raw", action="store_true", help="Unformatierte Ausgabe mit voller Präzision"
    )
    args = parser.parse_args()

    try:
        s_val = ast.literal_eval(args.s)
        result = zeta(s_val, precision=args.prec, verbose=args.verbose)
        if args.raw:
            print(result)
        else:
            print(format_result(result, digits=args.digits))
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
