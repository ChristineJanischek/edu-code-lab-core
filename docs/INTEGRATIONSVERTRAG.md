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

## Optionaler LLM-Ideation-Kontrakt (v1.1)

- `core/integrations/llm/idea_brief_from_chatgpt_project.sh`
- `core/integrations/llm/README.md`
- `docs/handbook/IDEA_SOURCE_CHATGPT_PROJECT.md`

Zweck:
- Externe Ideenquelle als lokales Artefakt dokumentieren
- Wiederholbare LLM-Verdichtung in ein Umsetzungsbriefing

Nicht-Ziel:
- Kein direkter API- oder Browser-Zugriff auf private ChatGPT-Projektseiten ohne expliziten Export

Beispielpruefung:

```bash
sh core/tooling/validate_task_template.sh tests/fixtures/templates/valid-task-v1.json
```

## Versionierung

- Breaking Changes nur mit Migrationshinweis
- Kompatibilitaetsaussagen pro Release dokumentieren
