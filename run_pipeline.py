from data_pipeline import build_dataset
from utils import save_pi_error_plot
import pandas as pd
from pathlib import Path

if __name__ == "__main__":
    # Pipeline starten
    build_dataset(max_zero_imag=10, x_values=[10, 50, 100, 500, 1000])

    # Ergebnis einlesen und Plot speichern
    pi_df = pd.read_csv(Path("data") / "pi_comparison.csv")
    save_pi_error_plot(pi_df, Path("data") / "pi_error_plot.png")

    print("✓ Alle Daten und Plots sind in data/ verfügbar")
