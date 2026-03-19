# Contributing

## Branching und Merge

- Direkte Commits auf `main` sind nicht erlaubt.
- Änderungen laufen über Pull Requests.
- Mindestens ein Review ist Pflicht.
- Alle Required Checks muessen gruen sein.
- Review-Konversationen muessen aufgeloest sein.

## Commit-Qualitaet

- Kleine, fachlich zusammenhaengende Commits.
- Praezise Commit-Messages im Imperativ.
- Keine toten Dateien oder temporaeren Artefakte committen.

## Lokaler Standard-Flow

```bash
./scripts/install-hooks.sh
git checkout -b feat/<kurze-beschreibung>
# arbeiten
make ci
```

## Definition of Done

- Strukturregeln eingehalten
- Tests und Lint erfolgreich
- Doku bei API-/Vertragsaenderungen aktualisiert
- PR nachvollziehbar beschrieben
