# Curriculum Planner

Diese Struktur bildet das neue Modul für den Curriculum-Planner ab.

## Gliederung
- 00_System
- 01_Stammdaten
- 02_Lehrplaene
- 03_Schulkalender
- 04_Stundenplaene
- 05_Unterrichtsplanung
- 06_Wochenplaene
- 07_Vorlagen
- 08_Ausgaben
- 09_Import_und_Pruefung

## Generator (Probe v1)

Der erste Generator fuer Wochenplaene liegt unter:

- `00_System/Generator/`

Schnellstart:

```bash
cd EduCore/modules/curriculum-planner/00_System/Generator
python3 -m pip install -r requirements.txt
python3 wochenplan_generator.py --config config/probe_2026_2027.json
```
