import pytest
import numpy as np
import pandas as pd
from spectral_analysis import load_spacings, spectrum_of_spacings


def test_load_spacings_valid(tmp_path):
    # Erstelle eine CSV mit t-Werten
    t_vals = [1.0, 2.5, 4.0, 7.5]
    df = pd.DataFrame({"t": t_vals})
    file = tmp_path / "zeros.csv"
    df.to_csv(file, index=False)

    spacings = load_spacings(str(file))
    expected = np.diff(np.array(t_vals))
    assert isinstance(spacings, np.ndarray)
    assert np.allclose(spacings, expected)


def test_load_spacings_missing_column(tmp_path):
    # CSV ohne t-Spalte sollte Fehler werfen
    df = pd.DataFrame({"x": [1, 2, 3]})
    file = tmp_path / "bad.csv"
    df.to_csv(file, index=False)

    with pytest.raises(ValueError):
        load_spacings(str(file))


def test_load_spacings_insufficient_data(tmp_path):
    # Nur ein Wert -> leeres Array
    df = pd.DataFrame({"t": [5.0]})
    file = tmp_path / "single.csv"
    df.to_csv(file, index=False)

    spacings = load_spacings(str(file))
    assert isinstance(spacings, np.ndarray)
    assert spacings.size == 0


def test_spectrum_of_spacings_empty():
    f, Pxx = spectrum_of_spacings(np.array([]))
    assert isinstance(f, np.ndarray) and isinstance(Pxx, np.ndarray)
    assert f.size == 0 and Pxx.size == 0


def test_spectrum_of_spacings_known():
    # Gleichmäßige Abstände, z.B. ones
    spacings = np.ones(512)
    fs = 1.0
    f, Pxx = spectrum_of_spacings(spacings, fs=fs, nperseg=256)
    # Frequenzen und PSD zurück
    assert f.ndim == 1 and Pxx.ndim == 1
    # Positive Werte
    assert np.all(Pxx >= 0)
    # f und Pxx gleiche Länge
    assert f.shape == Pxx.shape
