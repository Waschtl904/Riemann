# Riemann-Projekt

Ein Python-Paket zur Untersuchung und Bewertung der Riemannschen Zetafunktion ζ(s), inklusive Skripten, Jupyter-Notebooks und Unit-Tests.

---

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)  
- [Features](#features)  
- [Projektstruktur](#projektstruktur)  
- [Installation](#installation)  
- [Schnelleinstieg](#schnelleinstieg)  
- [API-Referenz](#api-referenz)  
- [Beispiele](#beispiele)  
- [Tests](#tests)  
- [Contributing](#contributing)  
- [Lizenz](#lizenz)  

---

## Über das Projekt

Dieses Repository bietet:

- **Berechnung** der Riemannschen Zetafunktion für reelle und komplexe Argumente  
- **Visualisierung** von Funktionswerten und Konvergenzverhalten  
- **Jupyter-Notebooks** zur interaktiven Erforschung  
- **Unit-Tests** zur Sicherstellung der Korrektheit  

Ziel ist es, Forschenden und Studierenden eine modulare, erweiterbare Basis für Experimente mit ζ(s) zu bieten.

---

## Features

- **Effiziente Summationsverfahren** für schnelle und genaue Auswertung  
- **Parameter-Validierung** und Fehlerbehandlung  
- **Plot-Utilities** für 2D- und 3D-Darstellungen  
- **CLI-Interface** (geplant)  
- **Umfangreiche Tests** mit pytest und Coverage  

---

## Projektstruktur

```text
Riemann/
├── data/                      ← Datenausgaben und Ergebnisse
│   └── ...
├── notebooks/                 ← Jupyter-Notebooks zur Analyse
│   └── 01_zeta_evaluation.ipynb
├── src/                       ← Quellcode-Paket
│   ├── __init__.py
│   ├── zeta.py                ← Kernfunktionen zur Berechnung
│   └── utils.py               ← Hilfsfunktionen (Plots, Validierung)
├── tests/                     ← Unit-Tests
│   └── test_zeta.py
├── .gitignore                 ← Git-Ignorierregeln
├── requirements.txt           ← Abhängigkeiten
└── README.md                  ← Projektübersicht
```

---

## Installation

1. Repository klonen  
   ```bash
   git clone https://github.com/Waschtl904/Riemann.git
   cd Riemann
   ```

2. Virtuelle Umgebung erstellen und aktivieren  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/macOS
   .venv\Scripts\Activate.ps1   # Windows PowerShell
   ```

3. Abhängigkeiten installieren  
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

---

## Schnelleinstieg

```python
from zeta import zeta

# Zetafunktion an der Stelle s = 2
wert = zeta(2)
print(f"ζ(2) = {wert:.6f}")  
```

---

## API-Referenz

### `zeta(s: complex | float) → complex`

Berechnet ζ(s) für reelle oder komplexe Argumente.  
- **Parameter**  
  - `s` – Punkt in der komplexen Ebene  
- **Rückgabe**  
  - Wert der Zetafunktion als `complex`

### `utils.plot_zeta(real_range: tuple, imag_range: tuple) → None`

Erstellt einen Plot der Funktionswerte.  
- **Parameter**  
  - `real_range` – (min, max) für den Realteil  
  - `imag_range` – (min, max) für den Imaginärteil  

*Weitere Funktionen sind in `src/utils.py` dokumentiert.*

---

## Beispiele

- **Evaluation in Jupyter**  
  ```bash
  jupyter lab notebooks/01_zeta_evaluation.ipynb
  ```
- **Plot einer Real-Schnitt-Analyse**  
  ```python
  from utils import plot_real_slice
  plot_real_slice(-10, 10, imag=0.5)
  ```

---

## Tests

Unit-Tests mit pytest ausführen:  
```bash
pytest --maxfail=1 --disable-warnings -q
```

Coverage-Report erzeugen:  
```bash
coverage run -m pytest
coverage html
```

---

## Contributing

Beiträge sind willkommen!  
1. Forke das Repository  
2. Erstelle einen Feature-Branch (`git checkout -b feature/xyz`)  
3. Schreibe Tests und implementiere Features  
4. Öffne einen Pull Request  

Bitte halte dich an PEP 8 und nutze Typannotations sowie Docstrings.

---

## Lizenz

MIT License © 2025 Waschtl904  
> siehe [LICENSE.md](LICENSE.md)
