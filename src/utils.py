# src/utils.py

"""
riemann.utils
Hilfsfunktionen für Visualisierung und Datenaufbereitung.
"""

# 1) matplotlib installieren: pip install matplotlib
import matplotlib.pyplot as plt
from typing import List
import matplotlib.markers as mmarkers


def plot_zeros(zeros: List[complex], title: str = "Nullstellen der ζ-Funktion"):
    """
    Zeichnet die gegebenen Nullstellen im komplexen Raum.
    :param zeros: Liste von komplexen Nullstellen
    :param title: Titel des Plots
    """
    re = [z.real for z in zeros]
    im = [z.imag for z in zeros]
    plt.figure(figsize=(6, 6))
    # 2) MarkerStyle statt Literal-String für Pylance
    plt.scatter(re, im, color="blue", marker=mmarkers.MarkerStyle("x"))
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.title(title)
    plt.xlabel("Realteil")
    plt.ylabel("Imaginärteil")
    plt.grid(True)
    plt.show()
