# 🔄 Template-Updates übernehmen

Dieses Repository ist ein **Template** für GitHub Classroom. Wenn du als Student/Schüler mit einem Fork/Clone dieses Templates arbeitest, kannst du spätere Updates (neue Versionen, Dokumentation, Bugfixes) vom Original-Template übernehmen.

## Dokument-Abgrenzung

- Dieses Dokument ist die operative Anleitung (Befehle, Schrittfolgen, Troubleshooting).
- Strategische Entscheidungen und Governance zum Update-Ansatz stehen in [TEMPLATE_UPDATE_STRATEGY.md](TEMPLATE_UPDATE_STRATEGY.md).
- Verbindliche Scope- und Redundanzregeln stehen im [PFLICHTENHEFT.md](PFLICHTENHEFT.md) und im [README.md](README.md) dieses Verzeichnisses.

---

## 📋 Warum Template-Sync?

- ✅ **Neue Versionen** (z.B. Version 4, 5) werden nachträglich verfügbar
- ✅ **Dokumentations-Updates** (`docs/*.md`, `README.md`) verbessern Lernmaterial
- ✅ **Bugfixes** in Musterlösungen oder Starter-Templates
- ✅ **Neue Features** (z.B. zusätzliche Workflows, Scripts)
- ⚠️ **Deine eigene Arbeit** in `version*/aufgabe/` bleibt unberührt!

---

## 🚀 Einmalige Einrichtung

### Schritt 1: Template-Remote hinzufügen

Füge das Original-Template als zusätzliches Remote-Repository hinzu:

```bash
git remote add template https://github.com/ChristineJanischek/web-project-dynamic.git
```

**Prüfen:**
```bash
git remote -v
```

Du solltest jetzt sehen:
```
origin    https://github.com/DEIN-USERNAME/web-project-dynamic.git (fetch)
origin    https://github.com/DEIN-USERNAME/web-project-dynamic.git (push)
template  https://github.com/ChristineJanischek/web-project-dynamic.git (fetch)
template  https://github.com/ChristineJanischek/web-project-dynamic.git (push)
```

### Schritt 2: Template-Änderungen abrufen

```bash
git fetch template
```

Dies lädt die neuesten Änderungen vom Template herunter (ohne sie zu übernehmen).

---

## 📥 Updates selektiv übernehmen

### Option 1: Nur Dokumentation aktualisieren

**Am sichersten!** Übernimmt nur Lernmaterialien, keine Code-Dateien:

```bash
# Alle Docs aktualisieren
git checkout template/main -- docs/

# Haupt-README aktualisieren
git checkout template/main -- README.md

# CONTRIBUTING aktualisieren
git checkout template/main -- CONTRIBUTING.md

# Committen
git add docs/ README.md CONTRIBUTING.md
git commit -m "📚 Dokumentation vom Template aktualisiert"
git push origin main
```

### Option 2: Neue Version übernehmen (z.B. Version 4)

Wenn das Template eine neue Version veröffentlicht:

```bash
# Neue Version komplett übernehmen
git checkout template/main -- version4/

# Committen
git add version4/
git commit -m "✨ Version 4 vom Template hinzugefügt"
git push origin main
```

### Option 3: GitHub Workflows aktualisieren

Neue oder verbesserte CI/CD-Workflows übernehmen:

```bash
git checkout template/main -- .github/workflows/
git add .github/workflows/
git commit -m "🔧 Workflows vom Template aktualisiert"
git push origin main
```

### Option 4: Einzelne Dateien aktualisieren

Nur bestimmte Dateien übernehmen:

```bash
# Beispiel: Nur corporate-design.md
git checkout template/main -- docs/corporate-design.md

# Beispiel: Nur Version 3 README
git checkout template/main -- version3/README.md

# Committen
git add docs/corporate-design.md version3/README.md
git commit -m "📝 Spezifische Dateien vom Template aktualisiert"
git push origin main
```

---

## ⚠️ Wichtige Warnungen

### ❌ NICHT überschreiben:

```bash
# NIEMALS deine eigene Arbeit überschreiben!
# ❌ git checkout template/main -- version1/aufgabe/
# ❌ git checkout template/main -- version2/aufgabe/
# ❌ git checkout template/main -- version3/aufgabe/
```

### ✅ Sicher zu übernehmen:

- `docs/*` - Dokumentation
- `README.md`, `CONTRIBUTING.md` - Anleitungen
- `version*/README.md` - Aufgabenbeschreibungen
- `version*/loesung/*` - Musterlösungen (nur für Lehrende)
- `.github/workflows/*` - CI/CD Workflows
- Neue Versionen (z.B. `version4/`, `version5/`)

---

## 🔍 Updates prüfen, bevor du sie übernimmst

### Welche Dateien wurden im Template geändert?

```bash
# Zeige alle Änderungen seit dem letzten Fetch
git fetch template
git log --oneline --graph template/main ^main

# Zeige geänderte Dateien
git diff main template/main --name-only
```

### Vorschau auf eine spezifische Datei

```bash
# Vorschau ohne zu übernehmen
git diff main template/main -- docs/react.md
```

---

## 🤝 Für GitHub Classroom (Lehrende)

### Template-Updates für alle Studenten verfügbar machen

**Variante A: Manuelle Anleitung**

1. Erstelle ein **Announcement** in GitHub Classroom:
   ```
   📢 Template-Update verfügbar!
   
   Neue Inhalte: Version 4, React-Dokumentation
   
   So übernimmst du die Updates:
   1. git remote add template https://github.com/ChristineJanischek/web-project-dynamic.git
   2. git fetch template
   3. git checkout template/main -- version4/
   4. git commit -m "✨ Version 4 hinzugefügt"
   5. git push
   
   ⚠️ Überschreibe nicht deine Lösungen in aufgabe/!
   ```

**Variante B: GitHub Classroom Sync (automatisch)**

GitHub Classroom unterstützt Template-Sync:

1. Gehe zu **Classroom Settings** → **Repository**
2. Aktiviere **"Allow students to pull updates from template"**
3. Studenten können dann auf **"Fetch upstream"** klicken

**Variante C: Pull Request-Workflow**

Erstelle einen **Draft Pull Request** vom Template:

```bash
# Im Student-Repo
git fetch template
git checkout -b template-updates
git merge template/main --no-commit

# Nur gewünschte Änderungen behalten
git reset HEAD version1/aufgabe/
git reset HEAD version2/aufgabe/
git reset HEAD version3/aufgabe/

# Committen und PR erstellen
git commit -m "📦 Template-Updates (Review erforderlich)"
git push origin template-updates
```

---

## 📚 Beispiel-Workflows

### Scenario 1: Neue Version 4 ist verfügbar

```bash
# 1. Template abrufen
git fetch template

# 2. Prüfen was neu ist
git diff main template/main -- version4/

# 3. Version 4 übernehmen
git checkout template/main -- version4/

# 4. Optional: Auch neue Docs
git checkout template/main -- docs/react.md

# 5. Committen
git add version4/ docs/react.md
git commit -m "✨ Version 4: React Grundlagen hinzugefügt"
git push origin main
```

### Scenario 2: Bugfix in Musterlösung

```bash
# 1. Template abrufen
git fetch template

# 2. Nur Musterlösung aktualisieren (nicht deine Arbeit!)
git checkout template/main -- version2/loesung/

# 3. Committen
git add version2/loesung/
git commit -m "🐛 Musterlösung Version 2 Bugfix vom Template"
git push origin main
```

### Scenario 3: Alle Docs auf neuesten Stand bringen

```bash
# 1. Template abrufen
git fetch template

# 2. Kompletten docs/-Ordner übernehmen
git checkout template/main -- docs/

# 3. Haupt-Dokumentation
git checkout template/main -- README.md CONTRIBUTING.md

# 4. Committen
git add docs/ README.md CONTRIBUTING.md
git commit -m "📚 Vollständige Dokumentation vom Template aktualisiert"
git push origin main
```

---

## 🆘 Problemlösung

### Problem: "Merge conflict"

Wenn Konflikte auftreten:

```bash
# Option 1: Konflikt manuell lösen
# Bearbeite die Datei mit Konflikt-Markern
# Dann:
git add <datei>
git commit

# Option 2: Template-Version bevorzugen
git checkout --theirs <datei>
git add <datei>

# Option 3: Eigene Version behalten
git checkout --ours <datei>
git add <datei>
```

### Problem: "Already up to date"

Das ist gut! Du hast bereits alle Updates.

### Problem: Versehentlich Arbeit überschrieben

Wenn du deine Lösungen überschrieben hast:

```bash
# Letzte Version wiederherstellen
git reflog
git checkout HEAD@{1} -- version1/aufgabe/

# Oder: Kompletten Commit rückgängig machen
git revert HEAD
```

---

## 🤖 Automatisiert mit Skript (für Lehrende)

Für Lehrende gibt es ein Hilfsskript, das den Update-Prozess vereinfacht:

```bash
# Mache das Script ausführbar
chmod +x scripts/sync-template.sh

# Setup: Richte Template-Fernverbindung ein
./scripts/sync-template.sh setup

# Check: Prüfe auf verfügbare Updates
./scripts/sync-template.sh check

# List: Zeige alle Änderungen
./scripts/sync-template.sh list-changes

# Dry-Run: Siehe was übernommen würde (ohne zu pushen)
./scripts/sync-template.sh apply --dry-run

# Apply: Übernehme Updates tatsächlich
./scripts/sync-template.sh apply

# Status: Zeige Sync-Status
./scripts/sync-template.sh status
```

**Vorteil:** Das Skript kümmert sich um:
- ✅ Automatic Conflict-Handling
- ✅ Backup-Branch vor Update
- ✅ Dry-Run zum Testen
- ✅ Detaillierte Logs

---

## 📊 Template-Updates überwachen

### GitHub Watch einrichten

1. Gehe zu https://github.com/ChristineJanischek/web-project-dynamic
2. Klicke auf **"Watch"** → **"Custom"**
3. Aktiviere **"Releases"** und **"Discussions"**
4. Du erhältst E-Mails bei neuen Releases

### Regelmäßig checken

```bash
# Einmal pro Woche/Monat
git fetch template
git log --oneline main..template/main
```

---

## 🎓 Best Practices

1. **Nie direkt mergen:** `git merge template/main` kann alles überschreiben!
2. **Selektiv übernehmen:** Nutze `git checkout template/main -- <pfad>`
3. **Immer committen:** Commit vor und nach Updates
4. **Review vor Push:** Prüfe `git diff` bevor du pushst
5. **Backup:** Bei Unsicherheit Branch erstellen: `git checkout -b template-update-backup`

---

## 📞 Support

- **Fragen?** Erstelle ein Issue im Template-Repo
- **Bugs?** Bug Report auf GitHub
- **Unklarheiten?** Frag deine:n Lehrer:in

---

**Erstellt:** Dezember 2025  
**Template:** https://github.com/ChristineJanischek/web-project-dynamic  
**Lizenz:** Bildung & Unterricht
