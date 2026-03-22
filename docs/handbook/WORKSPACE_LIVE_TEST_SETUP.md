# Workspace Setup für Live-Tests (Schritt für Schritt)

Diese Anleitung stellt sicher, dass alle für den Live-Test notwendigen VS-Code-Erweiterungen konsistent bereitgestellt werden.

## Zielbild

- Zentrale, wartbare Extension-Liste: `scripts/config/vscode_extensions.json`
- Synchronisierte Workspace-Empfehlungen: `.vscode/extensions.json`
- One-Click-Installation:
  - VS Code Task: `Setup: Install Live-Test Extensions`
  - NPM-Skript: `npm run setup:live-test`

## Für Schüler:innen (empfohlener Weg)

1. Repository in VS Code öffnen.
2. `Ctrl+Shift+P` → `Tasks: Run Task`.
3. Task wählen: **Setup: Install Live-Test Extensions**.
4. Danach eine HTML-Datei öffnen und `Open with Live Server` nutzen.

## Für Lehrkräfte/Administratoren

### 1) Extension-Empfehlungen aus Manifest synchronisieren

```bash
python3 scripts/manage_vscode_extensions.py sync
```

### 2) Synchronität prüfen (lokal/CI)

```bash
python3 scripts/manage_vscode_extensions.py check
```

Bei Abweichung liefert das Skript Exit-Code `2`.

### 3) Komplettes Extension-Set installieren (lokal)

```bash
npm run setup:extensions
```

### 4) Nur Live-Test-Set installieren

```bash
npm run setup:live-test
```

## Erweiterung ohne Redundanzen ergänzen

1. Extension in `scripts/config/vscode_extensions.json` in passender `group` eintragen.
2. Profilzuordnung in `profiles` prüfen/anpassen.
3. Sync ausführen:
   ```bash
   npm run setup:extensions:sync
   ```
4. Check ausführen:
   ```bash
   npm run setup:extensions:check
   ```
5. Committen.

## Hinweise

- In Codespaces installiert `.devcontainer/devcontainer.json` Extensions automatisch.
- Für lokale Entwicklung ist diese Routine der verbindliche Weg, damit Empfehlungen und Installation konsistent bleiben.
