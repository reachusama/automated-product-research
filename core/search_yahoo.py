from time import sleep

import requests
from bs4 import BeautifulSoup

from config.settings import MAX_PAGES, MAX_RESULTS_PER_QUERY
from core.helpers import extract_registered_domain


def yahoo_search(query, country_code="us", max_pages=MAX_PAGES):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    country_domains = {
        "us": "https://search.yahoo.com/search",
        "uk": "https://uk.search.yahoo.com/search",
        "ca": "https://ca.search.yahoo.com/search",
        "in": "https://in.search.yahoo.com/search",
        "au": "https://au.search.yahoo.com/search",
    }

    base_url = country_domains.get(
        country_code.lower(), "https://search.yahoo.com/search"
    )
    all_links = []

    for page in range(max_pages):
        start = (
            page * MAX_RESULTS_PER_QUERY + 1
        )  # Yahoo uses 1-based pagination with 'b' param
        params = {"p": query, "b": start}
        try:
            response = requests.get(
                base_url, params=params, headers=headers, timeout=10
            )
            soup = BeautifulSoup(response.text, "html.parser")

            results = soup.select("div.dd.algo.algo-sr h3.title > a")
            links = [a["href"] for a in results if a.get("href", "").startswith("http")]
            all_links.extend(links)

            sleep(1)

        except Exception as e:
            print(f"[ERROR] Yahoo page {page + 1}: {e}")
            break

    all_links_processed = [extract_registered_domain(link) for link in all_links]
    return list(set(all_links_processed))  # Deduplicate
