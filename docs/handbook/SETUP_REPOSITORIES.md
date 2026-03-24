# Setup Repositories

## Konfigurationsanleitung fuer `edu-code-lab-core` und `edu-code-lab-courses`

Stand: Maerz 2026

---

## 1 Ziel

Dieses Dokument beschreibt die verbindliche Erstkonfiguration beider Repositories, sodass Entwicklung, Inhaltspflege und Qualitaetssicherung sauber getrennt sind.

---

## 2 Reihenfolge

1. `edu-code-lab-core` erstellen und absichern
2. `edu-code-lab-courses` erstellen und absichern
3. gemeinsame Governance-Regeln synchronisieren
4. CI- und Hook-Strategie aktivieren
5. Integrationspunkte zwischen core und courses dokumentieren

---

## 3 Repository `edu-code-lab-core` einrichten

### 3.1 Repository erstellen

- Sichtbarkeit gemaess Schul-/Projektvorgabe waehlen
- README, Lizenz, CODEOWNERS, CONTRIBUTING initial anlegen
- Default-Branch `main`

### 3.2 Branch Protection (`main`)

- Pull Request Pflicht
- mindestens 1 Review
- erforderliche Status Checks aktiv
- kein direkter Push fuer Standardrollen
- aufgeloeste Review-Konversationen als Merge-Bedingung

### 3.3 Mindeststruktur

```text
core/
  platform/
  tooling/
  templates/
  integrations/
  docs/
  .github/workflows/
```

### 3.4 Core-CI aktivieren

Mindestens folgende Workflows:

- Build
- Unit-Tests
- Lint/Format
- Security/Dependency Scan
- Artefakt- oder Release-Checks

---

## 4 Repository `edu-code-lab-courses` einrichten

### 4.1 Repository erstellen

- eigenes Repository fuer Fachinhalte
- Default-Branch `main`
- gleiche Governance-Baseline wie core

### 4.2 Branch Protection (`main`)

- Pull Request Pflicht
- mindestens 1 Review (fachlich)
- verpflichtende Content-Checks

### 4.3 Mindeststruktur

```text
courses/
  courses/
    <themenbereich>/
      <kurs>/
        module/
        exams/
        solutions/
        media/
  docs/
  .github/workflows/
```

### 4.4 Courses-CI aktivieren

Mindestens folgende Workflows:

- Content-Validierung (Metadaten, Struktur, Konsistenz)
- Duplikat- und Qualitaetspruefung
- Link-/Dokumentationspruefung
- optionale Smoke-Tests fuer lauffaehige Beispiele

---

## 5 Gemeinsame VS-Code- und Toolchain-Konfiguration

1. Extensions zentral empfehlen und versionierbar pflegen
2. Setup-Task fuer Extension-Installation bereitstellen
3. Drift-Check zwischen Manifest und Empfehlungen in CI aktivieren
4. lokale Startprofile fuer statisch, PHP und Python dokumentieren

---

## 6 Hook-Strategie

### 6.1 Lokale Hooks

- `pre-commit`: schnelle Qualitaetspruefungen
- `pre-push` (optional): umfangreichere Checks

### 6.2 Wichtige Einschraenkung

Hooks werden nach `git clone` nicht automatisch aktiv.
Deshalb verbindlich:

- Hook-Installation im Onboarding dokumentieren
- CI als finale Schutzschicht erzwingen

---

## 7 Integrationsvertrag core -> courses

`courses` konsumiert standardisierte Ergebnisse aus `core`:

- Template-Schemata
- Validierungswerkzeuge
- Konfigurationskonventionen
- ggf. Export-/Rendering-Schnittstellen

Dokumentation der Versionen:

- klare Kompatibilitaetsmatrix (`core-version` zu `courses-release`)
- Breaking Changes nur mit Migrationshinweisen

---

## 8 Abnahme-Checkliste

Eine Einrichtung ist abgeschlossen, wenn:

1. beide Repositories vorhanden und geschuetzt sind
2. Pflicht-Workflows auf `main` aktiv sind
3. PR-Merge ohne Checks nicht moeglich ist
4. lokaler Setup-Flow fuer neue Mitwirkende reproduzierbar ist
5. Integrationsvertrag zwischen core und courses dokumentiert ist

---

## 9 Entscheidungsregel: Wann `edu-code-lab-courses` erstellen?

Das `courses`-Repository wird erstellt, sobald folgende Kriterien erfuellt sind:

1. `core`-Pflicht-CI ist stabil gruen (`build`, `unit-tests`, `lint-format`, `security-dependency-scan`, `release-check`)
2. Integrationsvertrag ist konkret versioniert
3. mindestens ein versioniertes Aufgaben-Schema ist veroeffentlicht
4. mindestens ein lauffaehiges Validierungswerkzeug liegt vor
5. Governance-Baseline ist in beiden Repositories gleich definiert

Pragmatische Regel:

- Start `courses` bei Erreichen von M2 (Template- und Validierungs-MVP produktiv).
- Wenn M2 knapp verfehlt wird, ist ein frueher Start nur erlaubt, wenn Punkt 1 bis 4 bereits technisch nachweisbar sind.

---

## 10 Heisser Draht (Assoziation) core <-> courses

Eine konkrete Schritt-fuer-Schritt-Anleitung inkl. Fehlerdiagnose steht in:

- `docs/handbook/WORKSPACE_LIVE_TEST_SETUP.md` (Workspace-Betrieb)
- `docs/handbook/CORE_COURSES_ASSOCIATION_GUIDE.md` (Vertrags- und Repo-Kopplung)

