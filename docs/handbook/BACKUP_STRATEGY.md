# Backup-Strategie (Best Practice)

Diese Strategie kombiniert lokale Backups mit einer automatisierten, wiederkehrenden Sicherung via GitHub Actions.

## Ziele

- Wiederherstellbarkeit des kompletten Repositories
- Nachvollziehbare, überprüfbare Snapshots
- Geringer manueller Aufwand

## Was wird gesichert?

1. **Git Bundle** (`*.bundle`): vollständige Git-Historie (`--all`)
2. **Source Archive** (`*.tar.gz`): aktueller Arbeitsstand von `HEAD`
3. **Manifest** (`manifest.txt`): Timestamp, Branch, Commit
4. **Checksummen** (`SHA256SUMS.txt`): Integritätsprüfung

## Lokale Sicherung

```bash
chmod +x scripts/create_backup_snapshot.sh
./scripts/create_backup_snapshot.sh
```

Optionales Zielverzeichnis:

```bash
./scripts/create_backup_snapshot.sh /pfad/zum/zielordner
```

## Automatische Sicherung

Workflow: `.github/workflows/backup-snapshot.yml`

- Trigger:
  - wöchentlich (Montag, 02:00 UTC)
  - manuell (`workflow_dispatch`)
- Ergebnis:
  - Upload als GitHub Artifact (`repo-backup-snapshot`)
  - Aufbewahrung: 30 Tage

## Wiederherstellung

### Aus Bundle klonen

```bash
git clone /pfad/repository-<timestamp>.bundle restored-repo
```

### Integrität prüfen

```bash
cd /pfad/zum/backup
sha256sum -c SHA256SUMS.txt
```

## Empfehlung (3-2-1-Prinzip)

- **3 Kopien**: GitHub + lokaler Snapshot + externes Storage
- **2 Medientypen**: lokale Platte + Cloud/Objektspeicher
- **1 Kopie extern/offsite**: getrennt vom Entwicklungsgerät

## Operative Routine

1. Vor größeren Strukturänderungen manuellen Snapshot erstellen
2. Nach Merge in `main` prüfen, ob der geplante Backup-Workflow erfolgreich lief
3. Quartalsweise Restore-Test durchführen (stichprobenartig)
