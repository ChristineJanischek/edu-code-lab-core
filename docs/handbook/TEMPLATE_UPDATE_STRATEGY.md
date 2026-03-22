# Template-Update-Strategie: Empfehlungen

## Dokument-Abgrenzung

- Dieses Dokument definiert die strategische Entscheidungsebene (Policy, Risiken, empfohlener Zielprozess).
- Konkrete Ausfuehrungsschritte und Git-Befehle stehen in [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md).
- Fuer Struktur- und Ownership-Regeln im Handbuch siehe [README.md](README.md).

## ⚠️ Warum KEINE vollautomatische Synchronisation?

### Probleme bei Auto-Sync:

1. **🚫 Überschreibt Schülerarbeiten**
   - Automatische Merges können `version*/aufgabe/` überschreiben
   - Schüler verlieren ihre Lösungen → Frustration!
   - Merge-Konflikte bei jedem Update

2. **🔒 GitHub Classroom Beschränkungen**
   - Kein direkter Schreib-Zugriff auf Student-Repos
   - Würde GitHub App/Token für jedes Repo benötigen
   - Datenschutz-Problematik bei automatischem Push

3. **🎯 Pädagogisch fragwürdig**
   - Schüler lernen nicht, Updates selbst zu managen
   - Keine Kontrolle über WANN Updates kommen
   - Kann mitten in Prüfungen/Abgaben stören

4. **⚙️ Technische Komplexität**
   - Fehleranfällig bei unterschiedlichen Repo-Zuständen
   - Schwer zu debuggen bei Problemen
   - Wartungsaufwand für Auto-Sync-Scripts

---

## ✅ Empfohlene Strategie: Semi-Automatisch

### Lösung 1: **GitHub Template Repository Features** (EMPFOHLEN)

GitHub bietet native Template-Funktionen:

```yaml
# In GitHub Repository Settings:
✓ "Template repository" aktivieren
✓ Studenten können "Use this template" nutzen
✓ GitHub zeigt "Fetch upstream" Button wenn Updates verfügbar
```

**Vorteil:**

- ✅ Native GitHub-Integration
- ✅ Schüler haben volle Kontrolle
- ✅ Kein Code nötig

**Einrichtung für Lehrende:**

1. Gehe zu Repository Settings → https://github.com/ChristineJanischek/web-project-dynamic/settings
2. Aktiviere "Template repository" (Checkbox unter Repo-Name)
3. Bei Updates: Erstelle ein **GitHub Release**
4. Schüler sehen "Fetch upstream" Button in ihrem Repo

**Für Schüler:**

1. Klick auf "Fetch upstream"
2. Wähle welche Änderungen übernommen werden
3. Optional: Merge oder Cherry-Pick

---

### Lösung 2: **Notification-Only Workflow** (DEIN AKTUELLER ANSATZ)

Der bereits erstellte `template-sync.yml` Workflow:

**Was er macht:**

- ✅ Erkennt Änderungen im Template
- ✅ Zeigt Benachrichtigung mit Anleitung
- ✅ Gibt klare Befehle für manuelle Updates
- ❌ Macht KEINE automatischen Änderungen

**Vorteile:**

- Schüler werden informiert
- Volle Kontrolle beim Schüler
- Keine Gefahr von Datenverlust

---

### Lösung 3: **Automatische Pull Requests** (Mittelweg)

Erstelle automatisch PRs für Updates (keine direkten Commits):

```yaml
name: Auto-PR für Template Updates

on:
  schedule:
    - cron: "0 0 * * 1" # Jeden Montag
  workflow_dispatch:

jobs:
  create-update-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fetch Template Updates
        run: |
          git remote add template https://github.com/ChristineJanischek/web-project-dynamic.git
          git fetch template

      - name: Create Update Branch
        run: |
          git checkout -b template-updates-$(date +%Y%m%d)

          # Nur sichere Dateien übernehmen
          git checkout template/main -- docs/
          git checkout template/main -- README.md
          git checkout template/main -- CONTRIBUTING.md

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: "📚 Template-Updates verfügbar"
          body: |
            Neue Updates vom Template verfügbar.

            ⚠️ **WICHTIG:** Prüfe vor dem Merge, dass keine deiner Lösungen überschrieben werden!

            **Geänderte Dateien:** Nur Dokumentation
          branch: template-updates-$(date +%Y%m%d)
```

**Vorteile:**

- ✅ Automatisch, aber kontrolliert
- ✅ Schüler müssen PR reviewen und mergen
- ✅ Keine ungewollten Änderungen

**Nachteile:**

- ⚠️ Benötigt GitHub Token in jedem Student-Repo
- ⚠️ Komplexer Setup

---

## 🎯 Meine Empfehlung für dein Projekt

### **Kombination aus:**

1. **GitHub Template Repository** (nativ)
   - Einfachste Lösung
   - Kein Code nötig
   - Schüler-freundlich

2. **Release-basierter Workflow**
   - Erstelle GitHub Releases für wichtige Updates
   - Benachrichtige Schüler per Classroom Announcement
   - Klare Versionen (v2.0, v3.0, v4.0)

3. **Dokumentation** (bereits erstellt)

- [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md) erklärt manuelle Updates
- Schüler lernen Git-Skills
- Volle Transparenz

---

## 📋 Konkrete Umsetzung

### Schritt 1: Template-Repository aktivieren

```bash
# Via GitHub Web UI:
1. Settings → Template repository ✓
2. Fertig!
```

### Schritt 2: Release-Workflow

Wenn du neue Version veröffentlichst:

````bash
# Lokaler Release
git tag -a v3.0 -m "Version 3: MiFa - Mission Future Academy"
git push origin v3.0

# GitHub Release erstellen (Web UI)
1. Releases → New Release
2. Tag: v3.0
3. Titel: "Version 3: MiFa Project + Neue Docs"
4. Beschreibung:
   ## Neue Features
   - ✨ Version 3 komplett
   - 📚 Corporate Design Docs
   - 🎨 Grünes Farbschema

   ## Update-Anleitung für Schüler
   ```bash
   git remote add template https://github.com/ChristineJanischek/web-project-dynamic.git
   git fetch template
   git checkout template/main -- version3/ docs/
   git commit -m "✨ Version 3 vom Template"
````

````

### Schritt 3: Classroom Announcement

Bei jedem wichtigen Update:

```markdown
📢 **Neues Template-Update: v3.0**

Neue Inhalte:
- Version 3: MiFa-Projekt mit Konzeption & Implementierung
- Neue Dokumentation: Corporate Design, Zielgruppenanalyse
- Version 2: Grünes Farbschema

**So übernimmst du die Updates:**
1. Klicke in deinem Repo auf "Fetch upstream"
2. ODER folge der Anleitung in [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md)

⚠️ Überschreibe NICHT deine eigenen Lösungen!
````

---

## 🚀 Für fortgeschrittene Szenarien

### Option: Dependabot-Style Updates (für Tools/Scripts)

Nur für **nicht-Code-Dateien** sinnvoll:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

Funktioniert nur für Actions, nicht für eigene Dateien.

---

## ❌ Was du NICHT tun solltest

```yaml
# ❌ GEFÄHRLICH: Auto-Force-Push
- name: Force Update (NICHT VERWENDEN!)
  run: |
    git reset --hard template/main
    git push --force
# → Löscht alle Schülerarbeiten!
# ❌ GEFÄHRLICH: Auto-Merge ohne Check
- name: Auto-Merge (NICHT VERWENDEN!)
  run: |
    git merge template/main
    git push
# → Merge-Konflikte, überschriebene Lösungen
# ❌ DATENSCHUTZ: Token in Student-Repos
- name: Mit PAT pushen (PROBLEMATISCH!)
  env:
    GITHUB_TOKEN: ${{ secrets.PERSONAL_TOKEN }}
# → Datenschutz-Problem, Sicherheitsrisiko
```

---

## 📊 Vergleichstabelle

| Methode               | Automatisierung | Kontrolle | Risiko          | Aufwand      | Empfehlung    |
| --------------------- | --------------- | --------- | --------------- | ------------ | ------------- |
| **Vollautomatisch**   | 100%            | 0%        | 🔴 Hoch         | Niedrig      | ❌ Nein       |
| **Auto-PR**           | 80%             | 20%       | 🟡 Mittel       | Mittel       | ⚠️ Optional   |
| **GitHub Template**   | 50%             | 50%       | 🟢 Niedrig      | Sehr niedrig | ✅ **JA**     |
| **Notification-Only** | 30%             | 70%       | 🟢 Sehr niedrig | Niedrig      | ✅ **JA**     |
| **Manuell**           | 0%              | 100%      | 🟢 Keins        | Hoch         | ✅ Lerneffekt |

---

## 🎓 Fazit

### Für GitHub Classroom: **NICHT vollautomatisch!**

**Beste Lösung:**

1. ✅ **GitHub Template Repository aktivieren**
2. ✅ **Releases für wichtige Updates**
3. ✅ **Manuelle Anleitung** ([TEMPLATE_SYNC.md](TEMPLATE_SYNC.md))
4. ✅ **Notification Workflow** (bereits vorhanden)
5. ❌ **KEINE Auto-Merges/Force-Pushes**

**Vorteile:**

- Schüler behalten Kontrolle
- Keine Datenverlust-Gefahr
- Pädagogisch wertvoll (Git-Skills)
- Einfacher Support
- Datenschutz-konform

**Kommunikation:**

- Release Notes bei jedem Update
- Classroom Announcements
- Klare Anleitung in [TEMPLATE_SYNC.md](TEMPLATE_SYNC.md)
- Office Hours für Fragen
