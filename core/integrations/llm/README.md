# LLM Integration fuer Ideation

Diese Integration verbindet lokale Ideen-Exporte mit einem LLM-gestuetzten Briefing.

## Ziel

- ChatGPT-Projekt als Ideenquelle dokumentieren
- Ideen in ein umsetzbares Briefing verdichten
- reproduzierbarer Ablauf fuer Team und CI-nahe Nutzung

## Einstieg

1. Inhalte aus dem ChatGPT-Projekt lokal ablegen, z. B. in einer Markdown-Datei.
2. Optional API setzen: `OPENAI_API_KEY` (und optional `OPENAI_MODEL`, `OPENAI_BASE_URL`).
3. Skript starten:

```bash
sh core/integrations/llm/idea_brief_from_chatgpt_project.sh \
  --source-file docs/handbook/IDEA_SOURCE_CHATGPT_PROJECT.md \
  --output reports/idea-brief.md
```

## Ergebnis

- Ausgabe in `reports/idea-brief.md`
- mit API-Key: LLM-basierte Strukturierung
- ohne API-Key: Fallback-Report mit klaren naechsten Schritten

## Hinweis zu ChatGPT-Projekt-URL

Die URL wird als Quelle referenziert. Ein automatisches Crawling der Projektseite ist absichtlich nicht Teil des Skripts, da die Seite in der Regel Authentifizierung und Session-Kontext benoetigt.