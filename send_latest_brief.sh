#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/.env.gmail}"
RUN_MODE="${1:-}"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing env file: $ENV_FILE" >&2
  exit 1
fi

set -a
. "$ENV_FILE"
set +a

RECIPIENT="${RECIPIENT:-kartikdurgebharatrath@gmail.com}"
FROM_NAME="${FROM_NAME:-Onyx Analytix Automation}"
REPLY_TO="${REPLY_TO:-}"

LATEST_HTML=$(ls -1t "$SCRIPT_DIR"/*_onyx_analytix_weekly_commercial_pharma_brief.html 2>/dev/null | head -n 1 || true)
LATEST_TEXT=$(ls -1t "$SCRIPT_DIR"/*_onyx_analytix_weekly_commercial_pharma_brief.txt 2>/dev/null | head -n 1 || true)
LATEST_MD=$(ls -1t "$SCRIPT_DIR"/*_onyx_analytix_weekly_commercial_pharma_brief.md 2>/dev/null | head -n 1 || true)

if [ -z "$LATEST_HTML" ] && [ -z "$LATEST_TEXT" ] && [ -z "$LATEST_MD" ]; then
  echo "No weekly brief file found in $SCRIPT_DIR" >&2
  exit 1
fi

BODY_FILE="$LATEST_TEXT"
if [ -z "$BODY_FILE" ]; then
  BODY_FILE="$LATEST_MD"
fi

PRIMARY_FILE="$LATEST_HTML"
if [ -z "$PRIMARY_FILE" ]; then
  PRIMARY_FILE="$BODY_FILE"
fi

BASENAME=$(basename "$PRIMARY_FILE")
BRIEF_DATE=$(printf '%s' "$BASENAME" | cut -d '_' -f 1)
SUBJECT="Onyx Analytix Weekly Commercial Pharma Brief - $BRIEF_DATE"

set -- python3 "$SCRIPT_DIR/send_gmail_message.py" \
  --to "$RECIPIENT" \
  --subject "$SUBJECT" \
  --from-name "$FROM_NAME"

if [ -n "$BODY_FILE" ]; then
  set -- "$@" --body-file "$BODY_FILE"
fi

if [ -n "$LATEST_HTML" ]; then
  set -- "$@" --html-file "$LATEST_HTML"
fi

if [ -n "$REPLY_TO" ]; then
  set -- "$@" --reply-to "$REPLY_TO"
fi

if [ "$RUN_MODE" = "--dry-run" ]; then
  "$@" --dry-run
else
  "$@"
fi
