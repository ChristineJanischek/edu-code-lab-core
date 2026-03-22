# Pflichtenheft

## Projekt: Intelligentes webbasiertes eLearning-Kurseditor-System fuer Informatik

Dieses Dokument ist die **verbindliche Single Source of Truth** fuer systemweite Anforderungen.

## Zielbild Repository-Split

1. `edu-code-lab-core` - Plattform, Tooling, Integrationen, Governance
2. `edu-code-lab-courses` - Fachinhalte, Kurse, Aufgaben, Loesungen

## Verbindliche Scope-Trennung

### Scope `edu-code-lab-core`

- Editor- und Rendering-Bausteine
- Aufgaben-/Template-Engine
- Import-/Export-Services
- Validierungs- und Qualitaets-Tooling
- CI-/Hook-Vorlagen und Automatisierung
- Integrationsschnittstellen

### Scope `edu-code-lab-courses`

- Kurse, Module und Lernpfade
- Aufgaben, Loesungen, Bewertungsschemata
- fachliche Beispiele, Medien, Diagramme
- didaktische Hinweise fuer Lehrkraefte und Lernende

## Muss-Anforderungen (MVP)

### Fuer core

1. Reproduzierbares lokales Setup ist dokumentiert und automatisierbar.
2. Build-, Test- und Qualitaetspruefungen liegen als CI-Workflows vor.
3. Hook-Templates (`pre-commit`, optional `pre-push`) sind bereitgestellt.
4. Standardisiertes Aufgaben-Schema ist als Vorlage auslieferbar.
5. Exporte (mindestens Markdown/HTML) sind ueber definierte Schnittstellen nutzbar.
6. Integrationspunkte fuer Mehrsprachen-Runtimes sind dokumentiert.

### Fuer courses

1. Inhalte sind entlang des Themenkatalogs strukturierbar.
2. Jede Aufgabe enthaelt Metadaten (Lernziel, Schwierigkeit, Punkte, Dauer).
3. Jede Aufgabe enthaelt mindestens eine validierbare Musterloesung.
4. Inhalte sind mit core-Validierungen pruefbar.
5. Sprachpfade blockieren sich nicht gegenseitig.
6. Kursinhalte sind versionierbar und releasefaehig.

## Governance

- `main` ist in beiden Repositories geschuetzt.
- Merge nur per Pull Request.
- Required Checks sind Merge-Voraussetzung.
- Offene Review-Konversationen sind vor Merge aufgeloest.

## Dokumentationsregel gegen Redundanz

1. Dieses Pflichtenheft wird nur in `edu-code-lab-core` gepflegt.
2. `edu-code-lab-courses` enthaelt nur eine Verweisdatei auf dieses Dokument.
3. Systemanforderungen werden nicht in mehreren Repositories dupliziert.

## Aenderungsprozess

- Aenderungen am Pflichtenheft ausschliesslich per PR in `edu-code-lab-core`.
- Jede Aenderung muss Scope, Auswirkungen und ggf. Migration enthalten.
