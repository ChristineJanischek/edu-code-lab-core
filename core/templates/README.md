# Templates in `edu-code-lab-core`

Dieses Verzeichnis enthaelt die versionierten Aufgaben-Schemata fuer `edu-code-lab-courses`.

## Aktueller Stand

- `task-schema.v1.json`: JSON-Schema fuer Aufgaben-Metadaten und Musterloesung

## Schneller Check

```bash
sh core/tooling/validate_task_template.sh tests/fixtures/templates/valid-task-v1.json
```

## Vertragshinweis

Breaking Changes am Schema erfordern:

1. neue Schemaversion (z. B. `v2`)
2. Migrationshinweis in den Release Notes
3. Anpassung in `docs/INTEGRATIONSVERTRAG.md`