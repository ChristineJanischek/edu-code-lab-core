# Repository Governance (Admin-only Push auf main)

Diese Anleitung stellt sicher, dass Aenderungen auf `main` nur ueber den Admin-Account laufen.

## Bereits im Repository umgesetzt

- `/.github/CODEOWNERS` enthaelt:
  - `* @ChristineJanischek`
- Verbindliche Merge-Regeln sind in `CONTRIBUTING.md` beschrieben.

## Schritt-fuer-Schritt (einmalig als Admin)

## 1) GitHub CLI vorbereiten

```bash
gh --version
gh auth login
```

## 2) Branch Protection in GitHub setzen

In `Settings -> Branches` (oder `Rules`) fuer Branch `main` konfigurieren:

Damit werden u. a. gesetzt:

- Push auf `main` nur für den angegebenen Admin-User
- PR-Review erforderlich
- Code-Owner-Review erforderlich
- Conversation-Resolution erforderlich

## 3) In GitHub UI verifizieren

`Settings -> Branches` (oder `Rules`) pruefen:

- Branch: `main`
- Restrict who can push: nur `ChristineJanischek`
- Require a pull request before merging: aktiv
- Require review from Code Owners: aktiv

## Wichtiger Hinweis

Technisch kann niemand per Repository-Datei allein globale GitHub-Rechte erzwingen. Verbindlich wird die Regel erst, wenn die Branch-/Ruleset-Einstellungen im GitHub-Repository aktiv sind.
