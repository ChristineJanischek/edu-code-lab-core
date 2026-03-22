# Handbuch-Index

Dieses Verzeichnis ist die zentrale Einstiegsebene fuer Strategie-, Architektur-, Governance- und Betriebsdokumente.

## Ziele dieser Struktur

- Erweiterbar: neue Themen lassen sich als eigenstaendige Dokumente ergaenzen.
- Wartbar: jedes Thema hat ein primaeres Referenzdokument.
- Praezise: inhaltliche Abgrenzungen vermeiden Doppelpflege.
- Vollstaendig: kein Inhalt geht verloren; Querverweise verbinden zusammengehoerige Themen.

## Leseweg (empfohlen)

1. [PFLICHTENHEFT.md](PFLICHTENHEFT.md): verbindliche Anforderungen und Scope-Trennung.
2. [ROADMAP_CORE.md](ROADMAP_CORE.md): zeitliche Planung und Meilensteine.
3. [SETUP_REPOSITORIES.md](SETUP_REPOSITORIES.md): Erstkonfiguration von `core` und `courses`.
4. [REPO_GOVERNANCE.md](REPO_GOVERNANCE.md): Branch-Schutz und Merge-Regeln.
5. [ARCHITECTURE.md](ARCHITECTURE.md) und [ARCHITEKTUR-PRINZIPIEN.md](ARCHITEKTUR-PRINZIPIEN.md): Architekturbewertung und Architekturprinzipien.
6. [TEMPLATE_UPDATE_STRATEGY.md](TEMPLATE_UPDATE_STRATEGY.md) und [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md): Strategie und operative Umsetzung fuer Template-Updates.
7. [BACKUP_STRATEGY.md](BACKUP_STRATEGY.md), [WORKSPACE_LIVE_TEST_SETUP.md](WORKSPACE_LIVE_TEST_SETUP.md), [QUICKSTART_LIVE_SERVER.md](QUICKSTART_LIVE_SERVER.md): Betrieb und lokales Arbeiten.

## Dokument-Verantwortung (Single Source of Truth)

- Anforderungen und verbindlicher Scope: [PFLICHTENHEFT.md](PFLICHTENHEFT.md)
- Phasen, Meilensteine, DoD: [ROADMAP_CORE.md](ROADMAP_CORE.md)
- Repo-Ersteinrichtung und Integrationsvertrag: [SETUP_REPOSITORIES.md](SETUP_REPOSITORIES.md)
- Governance-Regeln fuer Branches: [REPO_GOVERNANCE.md](REPO_GOVERNANCE.md)
- Template-Update-Policy und Entscheidungslogik: [TEMPLATE_UPDATE_STRATEGY.md](TEMPLATE_UPDATE_STRATEGY.md)
- Konkrete Update-Befehle und Troubleshooting: [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md)
- Navigations- und Pflegeprinzipien fuer Dokumentation: [DOCS_NAVIGATION_RULES.md](DOCS_NAVIGATION_RULES.md)

## Regeln gegen Redundanz

1. Strategische Entscheidung in genau einem Dokument halten.
2. Operative Schritt-fuer-Schritt-Anleitungen in genau einem Dokument halten.
3. In angrenzenden Dokumenten nur Kurzfassung plus Link auf die primaere Quelle pflegen.
4. Bei inhaltlicher Ueberschneidung die primaere Quelle in diesem Index aktualisieren.

## Aenderungsroutine

1. Betroffenes primaeres Dokument aktualisieren.
2. Querverweise in diesem Index pruefen.
3. Redundanzcheck: gleiche Regeln oder Befehle nicht in mehreren Dateien parallel pflegen.
4. Review: Vollstaendigkeit, Praezision, Widerspruchsfreiheit.
