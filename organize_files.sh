#!/usr/bin/env bash
set -euo pipefail

RAW_DIR="raw"
DUMPS_DIR="json_dump"
LOGS_DIR="logs"
TODAY="$(date -u +"%Y-%m-%d")"
log_file="$LOGS_DIR/$TODAY.log"

mkdir -p "$LOGS_DIR" "$RAW_DIR"

log() {
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - organize_files.sh: $1" >> "$log_file"
}

log "started"

# Keep this phase re-runnable without touching json_dump/.
rm -f "$RAW_DIR"/*.json 2>/dev/null
shopt -s nullglob

for src in "$DUMPS_DIR"/*; do
    base="$(basename "$src")"

    if [[ "$base" == "README.md" ]]; then
        continue
    fi

    newname="$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')"
    newname="$(printf '%s' "$newname" | sed 's/[ -]/_/g')"
    name_without_ext="${newname%.*}"
    ts="$(date -u +"%Y%m%dT%H%M%SZ")"
    final_name="${name_without_ext}_${ts}.json"
    dest="$RAW_DIR/$final_name"

    cp "$src" "$dest"
    log "copied $src to $dest"
done

log "finished"
