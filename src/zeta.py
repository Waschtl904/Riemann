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
from functools import lru_cache
import mpmath as mp
from typing import Any, Union

Number = Union[float, complex]


@lru_cache(maxsize=128)
def zeta(s: Any, precision: int = 50) -> Any:
    """
    Berechnet die Riemannsche Zetafunktion ζ(s) mit mpmath und Cache.

    :param s: Komplexe oder reelle Zahl
    :param precision: Dezimalstellen
    :return: mpmath.mpc Wert von ζ(s)
    :raises ValueError: Wenn s == 1 (Polstelle)
    """
    if isinstance(s, (int, float, complex)) and mp.almosteq(s, 1.0):
        raise ValueError(
            "ζ(s) hat eine Polstelle bei s = 1 und kann hier nicht ausgewertet werden."
        )

    # Typkonvertierung zu mpmath
    if isinstance(s, complex):
        s = mp.mpc(s.real, s.imag)
    else:
        s = mp.mpf(s)

    with mp.workdps(precision):
        return mp.zeta(s)


def format_result(val: Any, digits: int = 6) -> str:
    """
    Formatiert das Ergebnis als komplexe Zahl mit fester Genauigkeit.
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
        "-p", "--prec", type=int, default=50, help="Dezimalstellen für Berechnung"
    )
    parser.add_argument(
        "-d", "--digits", type=int, default=6, help="Nachkommastellen für Ausgabe"
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
        result = zeta(s_val, precision=args.prec)
        if args.verbose:
            print(
                f"[INFO] Berechne ζ({s_val}) mit {args.prec} Dezimalstellen",
                file=sys.stderr,
            )
        if args.raw:
            print(result)
        else:
            print(format_result(result, digits=args.digits))
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
