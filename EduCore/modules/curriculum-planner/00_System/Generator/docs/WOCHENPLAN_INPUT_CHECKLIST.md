# Wochenplan Input-Checklist

## Pflichtdokumente fuer einen Echtlauf

1. Transfer-Datei Vorjahr
- Dateiname: `Wochenplaene_2025_2026_transfer.xls`
- Inhalt: alle bisherigen Wochenplan-Sheets (je Klasse ein Sheet)
- Upload-Ziel: `EduCore/modules/curriculum-planner/09_Import_und_Pruefung/Eingang/`

2. Schulkalender kommendes Schuljahr
- Empfohlenes Format: `.json` oder `.csv`
- Muss enthalten: Schuljahresstart, Schuljahresende, ggf. unterrichtsfreie Schultage
- Upload-Ziel: `EduCore/modules/curriculum-planner/03_Schulkalender/Schuljahre/`

3. Ferien- und Feiertagskalender
- Empfohlenes Format: `.json` oder `.csv`
- Muss enthalten: Zeitraum pro Ferienblock sowie Feiertage als Einzeltermine
- Upload-Ziel:
  - Ferien: `EduCore/modules/curriculum-planner/03_Schulkalender/Ferien_und_Feiertage/`
  - Sondertermine: `EduCore/modules/curriculum-planner/03_Schulkalender/Besondere_Termine/`

4. Aktueller Lehrplan je Schulart/Klasse
- Empfohlenes Format: `.pdf` plus optional strukturierte Extraktion als `.md` oder `.json`
- Muss enthalten: Themenfelder, Kompetenzen, Priorisierung
- Upload-Ziel:
  - Original: `EduCore/modules/curriculum-planner/02_Lehrplaene/Originale/`
  - Aufbereitet: `EduCore/modules/curriculum-planner/02_Lehrplaene/Aufbereitet/`

5. Wochenstunden und Klassen-Setup
- Muss enthalten: Klassenliste (z. B. BKWI1, BKWI2, BG12, BG13), Wochenstunden, Schulart
- Upload-Ziel: `EduCore/modules/curriculum-planner/01_Stammdaten/Klassen/`

## Optional jetzt, Pflicht sobald verfuegbar

1. Abiturtermine und Pruefungsphasen
- Upload-Ziel: `EduCore/modules/curriculum-planner/03_Schulkalender/Besondere_Termine/`
- Wirkung: automatische Beruecksichtigung bei Themengewichtung und Wiederholungsfenstern

2. Gewichtung muendlich/schriftlich (Info fuer Schueler)
- Upload-Ziel: `EduCore/modules/curriculum-planner/01_Stammdaten/Faecher/`
- Wirkung: Ausgabehinweis im Wochenplan

## Ausgabeziele

- Excel: `EduCore/modules/curriculum-planner/08_Ausgaben/Jahresuebersichten/`
- PDF Lehrkraft: `EduCore/modules/curriculum-planner/08_Ausgaben/PDF_Lehrkraft/`
- PDF Schueler: `EduCore/modules/curriculum-planner/08_Ausgaben/PDF_Schueler/`

## Namensroutine (v1)

- `Wochenplaene_<SCHULJAHR>_<TIMESTAMP>.xls`
- `Wochenplaene_<SCHULJAHR>_<TIMESTAMP>.pdf`
