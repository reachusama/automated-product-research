import os
import csv
import pandas as pd
from config.settings import RESULTS_CSV, PROGRESS_CSV

def write_csv_row(row, file=RESULTS_CSV, header=False):
    file_exists = os.path.isfile(file)
    with open(file, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if header and not file_exists:
            writer.writeheader()
        writer.writerow(row)

def read_progress():
    if os.path.exists(PROGRESS_CSV):
        return set(pd.read_csv(PROGRESS_CSV).apply(lambda x: f"{x['keyword']}|{x['search_country']}", axis=1))
    return set()

def mark_progress(keyword, country):
    with open(PROGRESS_CSV, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "search_country"])
        if os.path.getsize(PROGRESS_CSV) == 0:
            writer.writeheader()
        writer.writerow({"keyword": keyword, "search_country": country})
