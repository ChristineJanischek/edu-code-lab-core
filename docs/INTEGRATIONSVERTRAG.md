# Integrationsvertrag core -> courses

`edu-code-lab-courses` konsumiert aus `edu-code-lab-core` ausschliesslich standardisierte Artefakte.

## Vertragsobjekte

- Template-Schemata aus `core/templates/`
- Validierungswerkzeuge aus `core/tooling/`
- Konfigurationskonventionen aus `docs/`
- Integrationsschnittstellen aus `core/integrations/`

## Konkreter v1-Dateikontrakt (MVP)

- `core/templates/task-schema.v1.json`
- `core/tooling/validate_task_template.sh`

Beispielpruefung:

```bash
sh core/tooling/validate_task_template.sh tests/fixtures/templates/valid-task-v1.json
```

## Versionierung

- Breaking Changes nur mit Migrationshinweis
- Kompatibilitaetsaussagen pro Release dokumentieren
