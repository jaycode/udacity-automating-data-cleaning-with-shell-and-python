#!/usr/bin/env bash
set -euo pipefail

if [[ -x ".venv/bin/python" ]]; then
    PYTHON_BIN=".venv/bin/python"
else
    PYTHON_BIN="python3"
fi
export PYTHON_BIN

LOGS_DIR="logs"
TODAY="$(date -u +"%Y-%m-%d")"
log_file="$LOGS_DIR/$TODAY.log"
mkdir -p "$LOGS_DIR"

log() {
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - run_pipeline.sh: $1" >> "$log_file"
}

echo "Pipeline started"
log "started"

echo "Starting filename organization"
log "starting filename organization"
./organize_files.sh

echo "Starting validation and routing"
log "starting validation and routing"
./validate_and_route.sh

echo "Starting JSON processing"
log "starting JSON processing"
"$PYTHON_BIN" process_jsons.py

echo "Starting dataset merge"
log "starting dataset merge"
"$PYTHON_BIN" merge_to_dataset.py

echo "Pipeline completed successfully"
log "completed successfully"
