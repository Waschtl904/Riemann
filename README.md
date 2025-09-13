Riemann-Projekt
Dieses Projekt untersucht die Riemannsche Zetafunktion ζ(s) und deren Nullstellen.

Projektstruktur
Riemann/
├── .venv/ Virtuelle Umgebung (nicht im VCS)
├── data/ Datendateien und Ergebnisse
├── notebooks/ Jupyter-Notebooks für Exploration
│ └── 01_zeta_evaluation.ipynb
├── src/ Quellcode-Paket
│ ├── init.py
│ ├── zeta.py Berechnung der Zetafunktion
│ └── utils.py Hilfsfunktionen (z.B. Visualisierung)
├── tests/ Unit-Tests
│ └── test_zeta.py
├── requirements.txt Pip-Abhängigkeiten
├── .gitignore Ignorierte Dateien und Ordner
└── README.md Projektübersicht und Installationsanleitung

Setup
Virtuelle Umgebung erstellen und aktivieren

powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Abhängigkeiten installieren

powershell
pip install -r requirements.txt
Paket im Entwicklungsmodus installieren

powershell
pip install -e .
Nutzung
Berechnung in Python-Skripten:

python
from riemann.zeta import zeta
print(zeta(2))
Interaktive Analyse im Jupyter-Notebook:

powershell
jupyter lab
Unit-Tests ausführen:

powershell
pytest
Lizenz
MIT License