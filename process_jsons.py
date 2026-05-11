#!/usr/bin/env python3

import datetime
import json
import os
import shutil
import sys

LOGS_DIR = "logs"
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOGS_DIR, f"{TODAY}.log")
os.makedirs(LOGS_DIR, exist_ok=True)


def log(message):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - process_jsons.py: {message}\n")


RAW_DIR = "raw"
CLEAN_DIR = "clean"
ARCHIVE_DIR = "archive"
VALID_FILES = "valid_files.txt"

os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

for filename in os.listdir(CLEAN_DIR):
    if filename.endswith(".json"):
        os.remove(os.path.join(CLEAN_DIR, filename))

for filename in os.listdir(ARCHIVE_DIR):
    if filename.endswith(".json"):
        os.remove(os.path.join(ARCHIVE_DIR, filename))

if not os.path.exists(VALID_FILES):
    log(f"{VALID_FILES} not found")
    sys.exit(1)

with open(VALID_FILES, "r", encoding="utf-8") as f:
    files = [line.strip() for line in f if line.strip()]

log(f"Processing {len(files)} valid files")


def normalize_json(data):
    product = data.get("product", {})
    if not isinstance(product, dict):
        product = {}

    metadata = data.get("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}

    try:
        price = float(data.get("price", 0.0))
    except (TypeError, ValueError):
        price = 0.0

    try:
        stock = int(metadata.get("stock", 0))
    except (TypeError, ValueError):
        stock = 0

    return {
        "product_id": data.get("product_id") or product.get("id"),
        "name": data.get("name") or product.get("name"),
        "category": data.get("category") or "unknown",
        "price": price,
        "color": metadata.get("color"),
        "stock": stock,
        "created_at": metadata.get("created_at") or metadata.get("created"),
    }


for file_path in files:
    filename = os.path.basename(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        log(f"Failed to read {file_path}: {e}")
        continue

    cleaned_data = normalize_json(data)
    clean_path = os.path.join(CLEAN_DIR, filename)

    try:
        with open(clean_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_data, f, indent=2)
            f.write("\n")
    except Exception as e:
        log(f"Failed to write cleaned file {clean_path}: {e}")
        continue

    log(f"Wrote cleaned file {clean_path}")

    archive_path = os.path.join(ARCHIVE_DIR, filename)
    shutil.copy2(file_path, archive_path)
    log(f"Archived original file to {archive_path}")

log("Processing complete")
