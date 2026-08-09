# Wochenplan Generator (OOP/MVC v1)

Dieser Generator erzeugt aus einer JSON-Konfiguration wochenweise Klassenplaene als `.xls` und `.pdf`.

## Architektur

- `wochenplan_generator.py`
  - Model: `SchoolYear`, `ClassProfile`, `WeekSlot`, `WeekRow`, `CalendarModel`
  - Controller: `WeeklyPlanController`
  - View: `XlsView`, `PdfView`
  - App/Composition Root: `WeeklyPlanApp`

## Installation

```bash
cd EduCore/modules/curriculum-planner/00_System/Generator
python3 -m pip install -r requirements.txt
```

## Probe-Run 2026/2027

```bash
cd EduCore/modules/curriculum-planner/00_System/Generator
python3 wochenplan_generator.py --config config/probe_2026_2027.json
```

## Echtlauf aus Transferdatei

Dieser Modus liest die Ausgangsdatei (mehrere Sheets), uebernimmt Klassen/Stammdaten
direkt aus der Datei und setzt nur das Schuljahr auf das Zieljahr um.

```bash
cd EduCore/modules/curriculum-planner/00_System/Generator
python3 wochenplan_generator.py \
  --config config/probe_2026_2027.json \
  --transfer-xls ../../09_Import_und_Pruefung/Eingang/Wochenplaene_2025_2026_transfer.xls \
  --target-school-year 2026/2027
```

Optionaler Druckmodus:

- `--print-mode auto` (Standard): versucht fuer jede Klassen-PDF maximal 2 Seiten zu erreichen
- `--print-mode off`: ohne automatische Verdichtung

## Eingabedaten (Echtlauf)

Siehe Checkliste:
- `docs/WOCHENPLAN_INPUT_CHECKLIST.md`

## Ausgabeorte

- Excel: `EduCore/modules/curriculum-planner/08_Ausgaben/Jahresuebersichten/`
- PDF: `EduCore/modules/curriculum-planner/08_Ausgaben/Jahresuebersichten/`

## Namensroutine

- `Wochenplaene_<SCHULJAHR>_vNNN_<TIMESTAMP>.xls`
- `Wochenplan_<KLASSE>_<SCHULJAHR>_vNNN_<TIMESTAMP>.pdf`

Die Versionsnummer `vNNN` wird pro Lauf im Ausgabeordner automatisch hochgezaehlt.
