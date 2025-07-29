import json
import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_CSV = os.path.join(DATA_DIR, "out/results.csv")
PROGRESS_CSV = os.path.join(DATA_DIR, "out/scrape_progress.csv")


def load_json(file_name, type="in"):
    path = os.path.join(DATA_DIR, f"{type}/{file_name}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load config data
KEYWORDS = load_json("keywords.json")
TARGET_AUDIENCE_TERMS = load_json("target_audience_terms.json")
IRRELEVANT_DOMAINS = load_json("irrelevant_domains.json")
BLOCKED_EXTENSIONS = load_json("blocked_extensions.json")
WEBSITE_CATEGORY_FILTERS = load_json("website_categories.json")


COUNTRIES = ["uk", "us", "ca", "au", "in"]
MAX_RESULTS_PER_QUERY = 10
MAX_PAGES = 3
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1",
}
