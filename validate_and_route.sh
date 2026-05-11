#!/usr/bin/env bash
set -uo pipefail

RAW_DIR="raw"
INVALID_DIR="invalid"
VALID_FILE_LIST="valid_files.txt"
PYTHON_BIN="${PYTHON_BIN:-python3}"
LOGS_DIR="logs"
TODAY="$(date -u +"%Y-%m-%d")"
log_file="$LOGS_DIR/$TODAY.log"

mkdir -p "$INVALID_DIR" "$LOGS_DIR"

log() {
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - validate_and_route.sh: $1" >> "$log_file"
}

rm -f "$INVALID_DIR"/*.json 2>/dev/null
> "$VALID_FILE_LIST"

for file in "$RAW_DIR"/*.json; do
    [[ -e "$file" ]] || continue

    log "validating $file"
    "$PYTHON_BIN" validate_json.py "$file"
    status=$?

    if [[ "$status" -eq 0 ]]; then
        echo "$file" >> "$VALID_FILE_LIST"
        log "valid $file"
    else
        cp "$file" "$INVALID_DIR/"
        log "copied invalid file $file to $INVALID_DIR/"
    fi
done
