#!/usr/bin/env sh
set -eu

SOURCE_URL_DEFAULT="https://chatgpt.com/g/g-p-6a44a453f26081918fb0c08b8546eafe-e-learning/project"
SOURCE_URL="${CHATGPT_PROJECT_URL:-$SOURCE_URL_DEFAULT}"
SOURCE_FILE=""
OUTPUT_FILE="./reports/idea-brief.md"
MODEL="${OPENAI_MODEL:-gpt-4.1-mini}"
OPENAI_BASE_URL="${OPENAI_BASE_URL:-https://api.openai.com/v1}"

usage() {
  cat <<'EOF'
Usage:
  sh core/integrations/llm/idea_brief_from_chatgpt_project.sh [options]

Options:
  --source-file <path>   Lokale Datei mit exportierten/copypasteten Projektideen
  --source-url <url>     Quelle dokumentieren (Default: ChatGPT-Projekt-URL)
  --output <path>        Ausgabe-Datei (Default: ./reports/idea-brief.md)
  --model <name>         OpenAI-Modell (Default: OPENAI_MODEL oder gpt-4.1-mini)
  --help                 Hilfe anzeigen

Hinweis:
  - Das Skript greift die ChatGPT-Projektseite nicht automatisch ab.
  - Fuer LLM-Zusammenfassung muss OPENAI_API_KEY gesetzt sein.
  - Ohne OPENAI_API_KEY wird ein strukturierter Fallback ohne API erstellt.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --source-file)
      SOURCE_FILE="$2"
      shift 2
      ;;
    --source-url)
      SOURCE_URL="$2"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo "Unbekannte Option: $1"
      usage
      exit 1
      ;;
  esac
done

mkdir -p "$(dirname "$OUTPUT_FILE")"

NOW_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

if [ -n "$SOURCE_FILE" ] && [ -f "$SOURCE_FILE" ]; then
  SOURCE_CONTENT="$(cat "$SOURCE_FILE")"
else
  SOURCE_CONTENT="Kein lokaler Ideen-Export angegeben. Bitte Projektideen aus ChatGPT in eine Datei uebernehmen und --source-file verwenden."
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  {
    echo "# Idea Brief (Fallback ohne LLM-API)"
    echo
    echo "- generated_at_utc: $NOW_UTC"
    echo "- source_url: $SOURCE_URL"
    echo "- mode: fallback-no-api"
    echo
    echo "## Rohinput"
    echo
    printf '%s\n' "$SOURCE_CONTENT"
    echo
    echo "## Naechste Schritte"
    echo
    echo "1. Exportiere die Inhalte des ChatGPT-Projekts in eine lokale Datei."
    echo "2. Setze OPENAI_API_KEY und optional OPENAI_MODEL."
    echo "3. Starte das Skript erneut fuer eine LLM-basierte Verdichtung."
  } >"$OUTPUT_FILE"

  echo "[llm-integration] Fallback-Output erzeugt: $OUTPUT_FILE"
  exit 0
fi

SYSTEM_PROMPT="Du bist ein strenger Produkt- und Curriculum-Redakteur. Verdichte den Input in: Kontext, priorisierte Ideen (max 7), Risiken, offene Fragen, konkrete naechste 3 Umsetzungsaktionen. Antworte in Deutsch."
USER_PROMPT="Quelle: $SOURCE_URL

Input:
$SOURCE_CONTENT"

PAYLOAD_FILE="$(mktemp)"
RESPONSE_FILE="$(mktemp)"

jq -n \
  --arg model "$MODEL" \
  --arg system "$SYSTEM_PROMPT" \
  --arg user "$USER_PROMPT" \
  '{
    model: $model,
    temperature: 0.2,
    messages: [
      {role: "system", content: $system},
      {role: "user", content: $user}
    ]
  }' >"$PAYLOAD_FILE"

curl -sS "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$PAYLOAD_FILE" >"$RESPONSE_FILE"

LLM_TEXT="$(jq -r '.choices[0].message.content // empty' "$RESPONSE_FILE")"

if [ -z "$LLM_TEXT" ]; then
  echo "[llm-integration] Fehler: Keine gueltige LLM-Antwort erhalten"
  echo "Antwort-Auszug:"
  head -n 40 "$RESPONSE_FILE"
  rm -f "$PAYLOAD_FILE" "$RESPONSE_FILE"
  exit 1
fi

{
  echo "# Idea Brief (LLM)"
  echo
  echo "- generated_at_utc: $NOW_UTC"
  echo "- source_url: $SOURCE_URL"
  echo "- model: $MODEL"
  echo
  printf '%s\n' "$LLM_TEXT"
} >"$OUTPUT_FILE"

rm -f "$PAYLOAD_FILE" "$RESPONSE_FILE"

echo "[llm-integration] LLM-Output erzeugt: $OUTPUT_FILE"