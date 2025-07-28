import time

from config.settings import BLOCKED_EXTENSIONS, COUNTRIES, IRRELEVANT_DOMAINS, KEYWORDS
from core.csv_writer import mark_progress, read_progress, write_csv_row
from core.helpers import (
    deduplicate_base_domains,
    filter_domains_by_extension,
    filter_irrelevant_domains,
)
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
                urls_processed = deduplicate_base_domains(urls)
                urls_domain_filter = filter_irrelevant_domains(
                    urls_processed, blocked_domains=IRRELEVANT_DOMAINS
                )
                urls_domain_ext_filter = filter_domains_by_extension(
                    urls_domain_filter, blocked_extensions=BLOCKED_EXTENSIONS
                )
                print(f"Found URLS {urls_domain_ext_filter}")
                for url in urls_domain_ext_filter:
                    data = process_url(category, keyword, url, country)
                    if data:
                        write_csv_row(data)
                    time.sleep(1.5)
                mark_progress(keyword, country.upper())
                break


if __name__ == "__main__":
    run_pipeline()
