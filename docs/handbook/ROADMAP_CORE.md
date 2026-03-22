# Roadmap Core

## Marschplan fuer `edu-code-lab-core`

Stand: Maerz 2026

---

## 1 Mission

`edu-code-lab-core` liefert die technische Plattform, die von `edu-code-lab-courses` genutzt wird.

---

## 2 Phasenplan

### Phase 0 - Fundament (2 bis 4 Wochen)

Ziele:

- Repo anlegen, Governance aktivieren
- Basisstruktur und Standards definieren
- CI-Grundpipeline aufsetzen

Lieferobjekte:

- geschuetzter `main`
- funktionierende Build-/Test-Workflows
- CONTRIBUTING + CODEOWNERS

### Phase 1 - Plattform-MVP (4 bis 8 Wochen)

Ziele:

- Template-Schema fuer Aufgaben definieren
- Validierungs-Tooling bereitstellen
- erste Integrationsschnittstellen spezifizieren

Lieferobjekte:

- versioniertes Aufgaben-Schema v1
- CLI oder Skript fuer Grundvalidierung
- dokumentierte API-/Dateikontrakte

### Phase 2 - Qualitaet und Erweiterbarkeit (6 bis 10 Wochen)

Ziele:

- robuste Testabdeckung fuer Kernkomponenten
- Hook-Templates und Qualitaetsprofile
- erweiterbare Plugin-Punkte vorbereiten

Lieferobjekte:

- Teststrategie + Mindestabdeckung
- Hook-Bundles
- technische Entwurfsdoku fuer Plugins

### Phase 3 - Betriebsfaehigkeit (6 bis 10 Wochen)

Ziele:

- Self-Hosted-Bausteine stabilisieren
- Export- und Integrationsdienste ausbauen
- Release-Prozess standardisieren

Lieferobjekte:

- Deployment-Runbook
- Export-Schnittstellen (mind. HTML/Markdown)
- geregeltes Versioning/Release Notes

### Phase 4 - KI und fortgeschrittene Automatisierung (optional)

Ziele:

- KI-Adapter als optionale Erweiterung
- keine harte Abhaengigkeit der Kernfunktion von externen KI-Diensten

Lieferobjekte:

- austauschbare KI-Schnittstelle
- Datenschutz- und Fallback-Konzept

---

## 3 Meilensteine

1. M1: Core-Basis laeuft inkl. Pflicht-CI
2. M2: Template- und Validierungs-MVP produktiv
3. M3: Integrationsvertrag fuer courses stabil
4. M4: Betriebs- und Releaseprozess etabliert

---

## 4 Risiken und Gegenmassnahmen

- Risiko: Ueberfrachtung des MVP
  - Gegenmassnahme: strikte Scope-Grenze fuer Phase 1
- Risiko: zu spaete Integrationsklarheit
  - Gegenmassnahme: fruehe, versionierte Kontrakte
- Risiko: KI blockiert Kernentwicklung
  - Gegenmassnahme: KI nur optional in spaeten Phasen

---

## 5 Definition of Done pro Release

Ein Core-Release gilt als fertig, wenn:

1. alle Pflichtchecks gruen sind
2. Schnittstellen dokumentiert und versioniert sind
3. Migrationshinweise bei Breaking Changes vorliegen
4. kompatible Nutzung in `edu-code-lab-courses` nachgewiesen ist

