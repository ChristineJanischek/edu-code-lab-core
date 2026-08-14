# A5-Handy-PDF-Routine

`a5_handout.py` versieht schülergerechte Handouts mit dem Standardvermerk:

```text
ki generiert - Fehler bitte ggf. melden!
```

Die Routine unterstützt:

- `.pdf`: Fußzeile auf jeder Seite, anschließend A5- und Textprüfung
- `.docx`: echte Word-Fußzeile im bearbeitbaren Dokument

## Verwendung

```bash
python3 core/tooling/a5_handout.py \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert_A5.pdf \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert_A5_footer.pdf
```

Für eine bearbeitbare DOCX-Fassung:

```bash
python3 core/tooling/a5_handout.py \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert.docx \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert_footer.docx
```

Eine bereits erzeugte PDF wird so geprüft:

```bash
python3 core/tooling/a5_handout.py \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert_A5_footer.pdf \
  --validate-only
```

Der Qualitätscheck prüft zusätzlich A5-Seiten, maschinenlesbaren Text, Fußzeilen,
PDF-Lesezeichen, klickbare Links und meldet erkannte Checklisten-/Tabellenmarker:

```bash
python3 core/tooling/a5_handout.py \
  project-knowledge/03_agent-source/KI_Lernagent_Schritt_fuer_Schritt_Didaktisch_erweitert_A5_footer.pdf \
  --validate-only --quality-check
```

Inhaltsverzeichnis, Links, Checklisten und Tabellen werden nicht künstlich ergänzt,
weil sie fachlich aus dem jeweiligen Kursskript stammen müssen. Fehlende optionale
Merkmale erscheinen als Hinweise; A5-Format, Lesbarkeit und Fußzeile sind harte
Qualitätskriterien.

Die DOCX bleibt die bearbeitbare Quelle. Die PDF wird daraus mit einem vorhandenen
Office-/PDF-Exportwerkzeug erzeugt und danach mit dieser Routine veredelt und geprüft.