"""
spectral_analysis.py

Spektralanalyse der Abstände der Riemann-Nullstellen.
"""

import numpy as np
import pandas as pd
from scipy import signal

__all__ = ["load_spacings", "spectrum_of_spacings"]


def load_spacings(csv_file: str) -> np.ndarray:
    """
    Lädt Imaginärteile der Nullstellen aus CSV und berechnet die Abstände Δt.

    Args:
        csv_file: Pfad zur CSV-Datei mit Spalte 't' für Imaginärteile.

    Returns:
        Array der Abstände Δtᵢ = tᵢ₊₁ - tᵢ.
    """
    df = pd.read_csv(csv_file)
    if "t" not in df.columns:
        raise ValueError("CSV muss Spalte 't' mit Imaginärteilen enthalten")
    t = df["t"].to_numpy(dtype=float)
    if len(t) < 2:
        return np.array([])
    spacings = np.diff(t)
    return spacings


def spectrum_of_spacings(
    spacings: np.ndarray, fs: float = 1.0, nperseg: int = 256
) -> tuple:
    """
    Berechnet die Power Spectral Density (PSD) der Abstände mittels Welch's Methode.

    Args:
        spacings: Array der Abstände Δtᵢ.
        fs: Sampling-Frequenz (default 1.0).
        nperseg: Länge der Segmente für Welch (default 256).

    Returns:
        Frequenzen f und PSD-Werte Pxx.
    """
    if spacings.size == 0:
        return np.array([]), np.array([])
    f, Pxx = signal.welch(spacings, fs=fs, nperseg=min(nperseg, len(spacings)))
    return f, Pxx
