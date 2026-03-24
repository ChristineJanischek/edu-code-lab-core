# Core-Courses Association Guide

## Ziel

Diese Anleitung definiert:

1. den Zeitpunkt fuer die Erstellung von `edu-code-lab-courses`
2. die fehlerfreie technische Assoziation zwischen `core` und `courses`
3. den operativen Prueffluss vor jedem Release

Stand: Maerz 2026

---

## 1 Go/No-Go fuer Erstellung von `edu-code-lab-courses`

`edu-code-lab-courses` wird erstellt, wenn alle folgenden Bedingungen erfuellt sind:

1. `core`-CI ist stabil gruen
2. Integrationsvertrag ist versioniert dokumentiert
3. Aufgaben-Schema v1 ist veroeffentlicht
4. Validierungswerkzeug ist lauffaehig und in Tests eingebunden

Praktische Entscheidung:

- Go bei M2 aus `ROADMAP_CORE.md`.
- No-Go, wenn Integrationskontrakt nur abstrakt ist oder Validator noch nicht reproduzierbar laeuft.

---

## 2 Assoziationsmodell (heisser Draht)

`courses` konsumiert aus `core`:

1. Schema (`core/templates/task-schema.v1.json`)
2. Validator (`core/tooling/validate_task_template.sh`)
3. Vertragsregeln (`docs/INTEGRATIONSVERTRAG.md`)

Die Verbindung wird ueber einen festen Versionsanker in `courses` hergestellt.

---

## 3 Konfiguration in `edu-code-lab-courses`

### 3.1 Lock-Datei anlegen

Datei: `.core-association.lock`

```env
CORE_REPO=https://github.com/ChristineJanischek/edu-code-lab-core.git
CORE_REF=main
TASK_SCHEMA_VERSION=1.0
VALIDATOR_PATH=core/tooling/validate_task_template.sh
```

Hinweis:

- fuer produktive Releases sollte `CORE_REF` auf einen Tag zeigen (z. B. `v0.2.0`), nicht dauerhaft auf `main`.

### 3.2 Core in CI auschecken

Beispiel-Workflow in `courses`: `.github/workflows/core-association-check.yml`

```yaml
name: core-association-check

on:
  pull_request:
  push:
    branches: [main]

jobs:
  core-association-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Load lock values
        run: |
          set -eu
          . ./.core-association.lock
          echo "CORE_REPO=$CORE_REPO" >> $GITHUB_ENV
          echo "CORE_REF=$CORE_REF" >> $GITHUB_ENV

      - name: Checkout core contract source
        uses: actions/checkout@v4
        with:
          repository: ChristineJanischek/edu-code-lab-core
          ref: ${{ env.CORE_REF }}
          path: core

      - name: Validate all task files
        run: |
          set -eu
          found=0
          for file in $(find courses -type f -name '*.task.json'); do
            found=1
            sh core/tooling/validate_task_template.sh "$file"
          done
          if [ "$found" -eq 0 ]; then
            echo "Keine *.task.json Dateien gefunden"
            exit 1
          fi
```

### 3.3 Branch-Schutz in `courses`

`main` in GitHub absichern mit:

1. PR-Pflicht
2. mind. 1 Review
3. Required Check `core-association-check`
4. Conversation Resolution aktiv

---

## 4 Lokaler Prueffluss

Im `core`-Repository:

```bash
sh scripts/verify_courses_association.sh /pfad/zu/edu-code-lab-courses
```

Dieser Check prueft:

1. Lock-Datei vorhanden und vollstaendig
2. Task-Dateien vorhanden
3. alle Task-Dateien gegen den `core`-Validator validierbar

---

## 5 Betriebsregel fuer Aenderungen

Bei Breaking Changes im Schema/Validator:

1. neue Version in `core` veroeffentlichen
2. Migrationshinweis dokumentieren
3. `.core-association.lock` in `courses` anheben
4. `core-association-check` in `courses` muss gruen sein

Ohne diese 4 Schritte kein Merge in `courses/main`.