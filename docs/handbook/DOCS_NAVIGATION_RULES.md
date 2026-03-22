# Docs Navigation Rules (Grundlagen)

Dieses Dokument definiert den Standard für die Navigation in den modularen Programmier-Grundlagen.

## Einordnung im Handbuch

- Primaere Handbuch-Navigation und Dokument-Ownership: [README.md](README.md)
- Verbindliche Scope- und Redundanzregeln: [PFLICHTENHEFT.md](PFLICHTENHEFT.md)

Ziele:

- keine Redundanzen bei Pflege der Kapitelreihenfolge
- hohe Wartbarkeit durch zentrale Regeln
- einfache Erweiterbarkeit bei neuen Kapiteln oder Sprachen

## Single Source of Truth

Die Reihenfolge und Struktur werden zentral in folgender Datei gepflegt:

- [scripts/config/docs_navigation_rules.json](../../scripts/config/docs_navigation_rules.json)

Diese Konfiguration steuert:

- Kapitelreihenfolge pro Sprache
- welche Sprachordner geprüft werden
- welches Ziel für den sprachübergreifenden Abschluss-Link genutzt wird

## Navigationsstandard

Für jede Kapiteldatei in

- `docs/programmierung/grundlagen/javascript/`
- `docs/programmierung/grundlagen/python/`
- `docs/programmierung/grundlagen/php/`

gilt:

1. Rücklink zur Sprach-Übersicht (`README.md`)
2. Weiter-Link zum nächsten Kapitel
3. Im letzten Kapitel: Weiter-Link auf den Sprachvergleich

Für Sprach-`README.md` gilt:

1. Link zurück zur Grundlagen-Übersicht (`../README.md`)
2. Link zum Sprachvergleich (`../VERGLEICH_JS_PY_PHP_OPERATOR_DATEI_IO.md`)
3. Kapitel-Links in der Reihenfolge aus der zentralen Konfiguration

## Validierung

Prüfskript:

- [scripts/check_docs_navigation.py](../../scripts/check_docs_navigation.py)

Ausführen:

```bash
python3 scripts/check_docs_navigation.py
```

oder über npm:

```bash
npm run docs:navigation:check
```

Exit-Codes:

- `0`: alles konsistent
- `2`: Regelverletzungen gefunden
- `1`: Konfigurations-/Laufzeitfehler

## Erweiterung ohne Redundanz

Wenn neue Kapitel dazukommen:

1. Kapiteldatei erstellen
2. Kapiteldatei in `scripts/config/docs_navigation_rules.json` an der richtigen Stelle eintragen
3. Sprach-README anpassen
4. `python3 scripts/check_docs_navigation.py` ausführen

Damit bleibt die Pflege auf eine zentrale Regeldatei fokussiert.
