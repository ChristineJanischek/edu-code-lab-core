# Repository Governance (Admin-only Push auf main)

Diese Anleitung stellt sicher, dass Änderungen auf `main` nur über den Admin-Account laufen.

## Bereits im Repository umgesetzt

- `/.github/CODEOWNERS` enthält:
  - `* @ChristineJanischek`
- Branch-Protection-Skript vorhanden:
  - `scripts/configure_branch_protection.sh`

## Schritt-für-Schritt (einmalig als Admin)

## 1) GitHub CLI vorbereiten

```bash
gh --version
gh auth login
```

## 2) Branch Protection automatisiert setzen

```bash
chmod +x scripts/configure_branch_protection.sh
./scripts/configure_branch_protection.sh ChristineJanischek web-project-dynamic main ChristineJanischek
```

Damit werden u. a. gesetzt:

- Push auf `main` nur für den angegebenen Admin-User
- PR-Review erforderlich
- Code-Owner-Review erforderlich
- Conversation-Resolution erforderlich

## 3) In GitHub UI verifizieren

`Settings → Branches` (oder `Rules`) prüfen:

- Branch: `main`
- Restrict who can push: nur `ChristineJanischek`
- Require a pull request before merging: aktiv
- Require review from Code Owners: aktiv

## Wichtiger Hinweis

Technisch kann niemand per Repository-Datei allein globale GitHub-Rechte „erzwingen". Verbindlich wird die Regel erst, wenn die Branch-/Ruleset-Einstellungen im GitHub-Repository aktiv sind.
