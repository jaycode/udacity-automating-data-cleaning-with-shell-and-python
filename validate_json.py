#!/usr/bin/env python3

import datetime
import json
import os
import sys

LOGS_DIR = "logs"
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOGS_DIR, f"{TODAY}.log")
os.makedirs(LOGS_DIR, exist_ok=True)


def log(message):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - validate_json.py: {message}\n")


def fail(message):
    log(message)
    sys.exit(1)


if len(sys.argv) != 2:
    fail("expected exactly one file path argument")

file_path = sys.argv[1]

if not os.path.exists(file_path):
    fail(f"missing file: {file_path}")

if os.path.getsize(file_path) == 0:
    fail(f"empty file: {file_path}")

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    fail(f"invalid JSON in {file_path}: {e}")
except OSError as e:
    fail(f"could not read {file_path}: {e}")

if not isinstance(data, dict):
    fail(f"invalid record type in {file_path}: expected object")

product = data.get("product")
has_product_id = bool(data.get("product_id")) or (
    isinstance(product, dict) and bool(product.get("id"))
)
has_name = bool(data.get("name")) or (
    isinstance(product, dict) and bool(product.get("name"))
)

required_checks = {
    "product id": has_product_id,
    "name": has_name,
    "category": "category" in data,
    "price": "price" in data,
    "metadata": isinstance(data.get("metadata"), dict),
}

missing = [field for field, present in required_checks.items() if not present]
if missing:
    fail(f"missing required fields in {file_path}: {', '.join(missing)}")

log(f"valid JSON: {file_path}")
sys.exit(0)
