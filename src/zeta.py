#!/usr/bin/env python3
"""
zeta.py – Berechnet die Riemannsche Zetafunktion ζ(s) mit mpmath.
"""

import sys
import ast
import argparse
from typing import Any

import mpmath as mp


def zeta(s: Any, precision: int = 50, verbose: bool = False) -> Any:
    """
    Berechnet die Riemannsche Zetafunktion ζ(s).

    :param s: Komplexe oder reelle Zahl (z.B. 0.5+14.1347j oder 2)
    :param precision: Dezimalstellen für Berechnung (Standard: 50)
    :param verbose: Bei True werden zusätzliche Infos ausgegeben
    :return: Wert von ζ(s) als mpmath-Zahl (mpf oder mpc)
    """
    if isinstance(s, complex):
        s = mp.mpc(s.real, s.imag)
    elif isinstance(s, (float, int)):
        s = mp.mpf(s)
    elif not isinstance(s, (mp.mpf, mp.mpc)):
        raise TypeError(f"Ungültiger Eingabetyp: {type(s)}")

    if verbose:
        print(f"[INFO] Berechne ζ({s}) mit {precision} Dezimalstellen", file=sys.stderr)

    with mp.workdps(precision):
        return mp.zeta(s)


def format_result(val: Any, digits: int = 6) -> str:
    """
    Formatiert das Ergebnis als komplexe Zahl mit fester Genauigkeit.

    :param val: Ergebniswert (mpmath.mpf oder mpc)
    :param digits: Nachkommastellen für Ausgabe (Standard: 6)
    :return: formatierter String
    """
    if isinstance(val, mp.mpf):
        return f"{val:.{digits}g}"
    else:
        real_str = f"{val.real:.{digits}g}"
        imag_str = f"{abs(val.imag):.{digits}g}"
        sign = "+" if val.imag >= 0 else "-"
        return f"{real_str} {sign} {imag_str}j"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Berechnung der Riemannschen Zetafunktion ζ(s)"
    )
    parser.add_argument("s", type=str, help="Stelle s (z.B. 2 oder '0.5+14.1347j')")
    parser.add_argument(
        "-p", "--prec", type=int, default=50, help="Dezimalstellen (Standard: 50)"
    )
    parser.add_argument(
        "-d", "--digits", type=int, default=6, help="Nachkommastellen (Standard: 6)"
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
