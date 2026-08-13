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
  --layout-template config/layout_template_v003.json \
  --transfer-xls ../../09_Import_und_Pruefung/Eingang/Wochenplaene_2025_2026_transfer.xls \
  --target-school-year 2026/2027
```

Alternativ als Ein-Klick-Routine:

```bash
cd EduCore/modules/curriculum-planner/00_System/Generator
./generate_wochenplaene_v003.sh
```

Parameter fuer die Routine:

1. Transferdatei (optional)
2. Zielschuljahr (optional, Format `YYYY/YYYY`)
3. Druckmodus (optional: `auto` oder `off`)

Optionaler Druckmodus:

- `--print-mode auto` (Standard): versucht fuer jede Klassen-PDF maximal 2 Seiten zu erreichen
- `--print-mode off`: ohne automatische Verdichtung

Layout-Template:

- `--layout-template config/layout_template_v003.json` (Standard)
- Die Datei enthaelt Layout, Spaltenbreiten, Farben und Regeln fuer Sonderzeilen.
- Ferien-/freie Wochen werden in XLS und PDF automatisch mit hellem Pastell-Orange hinterlegt.
- Feiertagswochen werden in XLS und PDF automatisch mit hellem Pastell-Gruen hinterlegt.

## Wiederverwendbare Jahresroutine

Die Routine liest die Kalenderquelle aus `config/probe_2026_2027.json` und uebernimmt
die Themenreihenfolge aus der Transfer-XLS. Fuer ein neues Schuljahr werden nur die
Kalenderquelle, die Zieljahresangabe und die Transferdatei ausgetauscht:

```bash
./generate_wochenplaene_v003.sh \
  ../../09_Import_und_Pruefung/Eingang/Wochenplaene_<VORJAHR>_transfer.xls \
  <STARTJAHR>/<ENDJAHR> \
  auto
```

Die Kalenderquelle muss `vacation_ranges`, optional `movable_vacation_days` und
`holidays` enthalten. Feiertage koennen als `{ "date": "YYYY-MM-DD", "name": "..." }`
angegeben werden. Die Routine erzeugt die Ferienzeilen neu, verteilt die vorhandenen
Themen in ihrer Reihenfolge auf die verbleibenden Unterrichtswochen und markiert
Feiertagswochen gruen. Anmerkungen werden bei einer Kalenderregeneration komplett
neu aufgebaut; alte Tageshinweise wie `nur Mo - Do` werden nicht uebernommen.

Automatik in der Spalte Anmerkung:

- Ein Tageshinweis wird nur erzeugt, wenn ein Ferienblock unter der Woche startet (Dienstag bis Freitag).
- In diesem Fall wird fuer die betroffene Woche ein Hinweis wie `nur Mo - Di` oder `nur Mo` gesetzt.
- Die Berechnung basiert auf den Ferien-/Feiertagsdaten der Generator-Konfiguration.
- Bei Ferienbeginn am Montag wird kein Tageshinweis erzeugt.

Automatische Anmerkungen (Spalte `Anmerkung`):

- Der Generator analysiert pro Kalenderwoche die Schultage (Mo-Fr) gegen Ferien, Feiertage und Schuljahresgrenzen.
- Bei Teilwochen wird automatisch ein Hinweis gesetzt, z. B. `nur Mo - Mi.` oder `nur Di, Do.`
- Vorhandene manuelle Hinweise bleiben erhalten und werden um den Tageshinweis ergaenzt.

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
