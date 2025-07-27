import time

from config.settings import COUNTRIES, KEYWORDS
from core.csv_writer import mark_progress, read_progress, write_csv_row
from core.scraper import process_url
from core.search_google import google_search


def run_pipeline():
    seen = read_progress()

    for country in COUNTRIES:
        for category, keywords in KEYWORDS.items():
            for keyword in keywords:
                task_key = f"{keyword}|{country.upper()}"
                if task_key in seen:
                    continue

                print(f"Searching {keyword} in {country.upper()}")
                urls = google_search(keyword, country)

                for url in urls:
                    data = process_url(category, keyword, url, country)
                    if data:
                        write_csv_row(data)
                    time.sleep(1.5)
                mark_progress(keyword, country.upper())
                break


if __name__ == "__main__":
    run_pipeline()
