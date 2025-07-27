import os
import json

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# Load helper
def load_json(file_name):
    path = os.path.join(DATA_DIR, file_name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load config data
KEYWORDS = load_json("keywords.json")
TARGET_AUDIENCE_TERMS = load_json("target_audience_terms.json")
FEATURE_TERMS = load_json("feature_terms.json")

API_KEY = "YOUR_GOOGLE_API_KEY"
SEARCH_ENGINE_ID = "YOUR_CUSTOM_SEARCH_ID"
MAX_RESULTS_PER_QUERY = 100

RESULTS_CSV = "data/results.csv"
PROGRESS_CSV = "data/scrape_progress.csv"

COUNTRIES = ["uk", "us", "ca", "au", "in"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1"
}
