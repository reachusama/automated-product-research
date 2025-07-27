import csv
import os

import pandas as pd

from config.settings import PROGRESS_CSV, RESULTS_CSV


def ensure_directory(file_path):
    """Ensure the directory for the file exists."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def write_csv_row(row, file=RESULTS_CSV, header=False):
    ensure_directory(file)
    file_exists = os.path.isfile(file)
    with open(file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if header and not file_exists:
            writer.writeheader()
        writer.writerow(row)


def read_progress():
    ensure_directory(PROGRESS_CSV)
    if os.path.exists(PROGRESS_CSV) and os.path.getsize(PROGRESS_CSV) > 0:
        df = pd.read_csv(PROGRESS_CSV)
        return set(df.apply(lambda x: f"{x['keyword']}|{x['search_country']}", axis=1))
    return set()


def mark_progress(keyword, country):
    ensure_directory(PROGRESS_CSV)
    new_row = {"keyword": keyword, "search_country": country}
    file_exists = os.path.exists(PROGRESS_CSV)
    with open(PROGRESS_CSV, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "search_country"])
        if not file_exists or os.path.getsize(PROGRESS_CSV) == 0:
            writer.writeheader()
        writer.writerow(new_row)
