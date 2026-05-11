#!/usr/bin/env python3

import datetime
import json
import os
import sys

import pandas as pd

LOGS_DIR = "logs"
TODAY = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOGS_DIR, f"{TODAY}.log")
os.makedirs(LOGS_DIR, exist_ok=True)


def log(message):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - merge_to_dataset.py: {message}\n")


CLEAN_DIR = "clean"
DATASET_DIR = "dataset"
OUTPUT_FILE = os.path.join(DATASET_DIR, "clean_products.csv")
COLUMNS = ["product_id", "name", "category", "price", "color", "stock", "created_at"]

os.makedirs(DATASET_DIR, exist_ok=True)

rows = []
log("Starting dataset merge")

for filename in sorted(os.listdir(CLEAN_DIR)):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(CLEAN_DIR, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            rows.append(json.load(f))
        log(f"Loaded {file_path}")
    except Exception as e:
        log(f"Failed to load {file_path}: {e}")

if not rows:
    log("No cleaned rows were loaded")
    sys.exit(1)

df = pd.DataFrame(rows).reindex(columns=COLUMNS)
df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0.0).astype(float)
df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0).astype(int)
df.to_csv(OUTPUT_FILE, index=False)

log(f"Wrote dataset to {OUTPUT_FILE}")
log("Dataset merge complete")
