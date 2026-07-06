# edu-code-lab-core

Core-Repository fuer gemeinsame Plattform-Bausteine, Tooling, Templates und Integrationsvertraege.

## Struktur

```text
core/
  platform/
  tooling/
  templates/
  integrations/
docs/
.github/workflows/
```

## Schnellstart

```bash
git clone https://github.com/ChristineJanischek/edu-code-lab-core.git
cd edu-code-lab-core
./scripts/install-hooks.sh
```

## Qualitaet

Die Pflicht-Checks fuer Pull Requests sind:
- `build`
- `unit-tests`
- `lint-format`
- `security-dependency-scan`
- `release-check`

## Governance

- Beitragsregeln: [CONTRIBUTING.md](CONTRIBUTING.md)
- Sicherheitsprozess: [SECURITY.md](SECURITY.md)
- Integrationsvertrag: [docs/INTEGRATIONSVERTRAG.md](docs/INTEGRATIONSVERTRAG.md)
- Pflichtenheft: [docs/handbook/PFLICHTENHEFT.md](docs/handbook/PFLICHTENHEFT.md)

<!-- CUSTOM_LICENSE_NOTICE_START -->
## License

This repository is licensed under a custom license.

- Attribution required: Christine Janischek - https://emotionalspirit.de
- Non-commercial use only
- Use only within state school systems
- Any other use requires explicit prior written permission
<!-- CUSTOM_LICENSE_NOTICE_END -->
