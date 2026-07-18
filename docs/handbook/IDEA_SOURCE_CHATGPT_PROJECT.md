# Idea Source: ChatGPT Project

Quelle:
- https://chatgpt.com/g/g-p-6a44a453f26081918fb0c08b8546eafe-e-learning/project
- https://chatgpt.com/share/6a5402a1-83d0-83eb-98c8-edfd8e6ba6cc

## Verwendung

Kopiere hier relevante Ideen, Cluster und Prioritaeten aus dem Projekt hinein.
Diese Datei wird von der LLM-Integration als lokaler Input verwendet.

## Snapshot

- Stand-Datum: 2026-07-18
- Quelle-Typ: manueller Export aus ChatGPT-Projekt und Share-Chat
- Verantwortlich: Team core

## Problemraum

- Ideen und Entscheidungen gehen in Einzelchats verloren und werden nicht systematisch wiederverwendet.
- KI-Funktionen drohen funktionsgetrieben statt bedarfsgetrieben entwickelt zu werden.
- Unterrichtserfahrungen fliessen zu wenig strukturiert in Architektur und Backlog ein.

## Zielgruppen

- Primar: Lehrkraefte in staatlichen Schulen
- Sekundaer: Lernende in Kursen mit Aufgaben-Templates
- Tertiaer: Repo-Maintainer in core/courses

## Lernziele und Outcomes

- Lernende sollen Verstehen und Selbststaendigkeit aufbauen, ohne Loesungen vorgesagt zu bekommen.
- Lehrkraefte sollen Ideen schneller in strukturierte Unterrichtsbausteine ueberfuehren.
- Das System soll aus Erfahrungen lernen: Beobachtung -> Erkenntnis -> wiederverwendbarer Baustein.

## Ideen-Backlog (aus ChatGPT-Projekt)

Nutze pro Idee den folgenden Block:

### Idee 1 - Projektgedaechtnis als verbindliche Steuerzentrale

- Kurzbeschreibung: Aufbau eines zentralen Wissensbereichs fuer Prinzipien, Backlog, Lernprotokolle und Architekturentscheidungen.
- Nutzerwert: Entscheidungen, Muster und Lernergebnisse sind dauerhaft auffindbar und teamweit nutzbar.
- Aufwand (S/M/L): M
- Risiko (niedrig/mittel/hoch): niedrig
- Abhaengigkeiten: Dokumentationskonventionen, klare Ownership
- Messbare Akzeptanzkriterien: Struktur angelegt; Vorlagen vorhanden; jede neue Idee wird als Projektbaustein erfasst.

### Idee 2 - Standardroutine fuer neue Ideen (Intake -> Analyse -> Klassifikation)

- Kurzbeschreibung: Jede freie Eingabe wird in ein einheitliches Format ueberfuehrt und nach Kategorie sowie Reichweite bewertet.
- Nutzerwert: Ideen werden vergleichbar, priorisierbar und schneller umsetzbar.
- Aufwand (S/M/L): M
- Risiko (niedrig/mittel/hoch): mittel
- Abhaengigkeiten: Projektbaustein-Template, Priorisierungsmodell
- Messbare Akzeptanzkriterien: pro Idee liegen Bedarf, Zielgruppe, Wirkung, Risiko, Akzeptanzkriterien und Reichweite vor.

### Idee 3 - Core/Course-Entscheidungsmatrix als Architekturregel

- Kurzbeschreibung: Regeln zur Entscheidung, ob eine Funktion in Aufgabe, Kurs, Core oder Oekosystem gehoert.
- Nutzerwert: weniger Doppelentwicklung und konsistente Modulbildung.
- Aufwand (S/M/L): S
- Risiko (niedrig/mittel/hoch): niedrig
- Abhaengigkeiten: Integrationsvertrag core -> courses
- Messbare Akzeptanzkriterien: jede neue Funktion hat dokumentierte Zuordnung mit Begruendung.

### Idee 4 - Lernschleife aus Unterrichtsretrospektiven

- Kurzbeschreibung: Nach Einsaetzen werden Beobachtungen zu Wirkung, Schwierigkeiten und Verbesserungen systematisch protokolliert.
- Nutzerwert: Produktverbesserung basiert auf realer Nutzung statt auf Vermutungen.
- Aufwand (S/M/L): M
- Risiko (niedrig/mittel/hoch): mittel
- Abhaengigkeiten: Retrospektiven-Template, Datenschutzleitplanken
- Messbare Akzeptanzkriterien: pro Einsatz liegt ein kurzes Lernprotokoll vor; monatliche Auswertung findet statt.

## Priorisierung (Now / Next / Later)

- Now: Projektgedaechtnis einrichten; Projektbaustein-Template festlegen; Entscheidungsmatrix dokumentieren.
- Next: Prototyp "freie Idee -> strukturierter Projektbaustein"; Requirement-Engine-Konzept.
- Later: Halbautomatische Lernschleife mit Mustererkennung und Core-Kandidatenvorschlaegen.

## Architektur- und Integrationsauswirkungen

- Betroffene Dateien/Vertraege in core: docs/INTEGRATIONSVERTRAG.md, core/integrations/llm/*, neue Struktur project-knowledge/*
- Potenzielle Breaking Changes: keine Laufzeit-Breaking-Changes, primär Prozess- und Doku-Erweiterung
- Notwendige Migrationshinweise: Teams muessen neue Intake- und Retrospektiven-Routinen verbindlich nutzen

## Offene Fragen

- Welche Mindestmetadaten pro Idee sind verpflichtend?
- Wie oft erfolgt die monatliche Lernschleife und wer moderiert sie?
- Welche Metriken priorisieren wir in den ersten 8 Wochen?

## Entscheidungen

- Beduerfnisse vor Funktionen ist verbindliches Leitprinzip.
- KI unterstuetzt Menschen beim Denken, ersetzt sie aber nicht.
- Jede Idee durchlaeuft den Lernkreislauf Beobachten -> Verstehen -> Strukturieren -> Erproben -> Lernen.

## Rohnotizen

- Leitsatz: Aus Ideen werden Bausteine, aus Erfahrungen wird Wissen, aus Wissen waechst ein System.