from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config.settings import HEADERS
from core.extractor import extract_seo_meta, is_irrelevant_url


def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] Fetching {url}: {e}")
        return None


def process_url(keyword_category, keyword, url, country_code):
    if is_irrelevant_url(url):
        return None

    soup = get_soup(url)
    if not soup:
        return None

    website_title = soup.title.string.strip() if soup.title else ""
    seo = extract_seo_meta(soup)

    return {
        "keyword_category": keyword_category,
        "keyword": keyword,
        "last_updated": datetime.utcnow().isoformat(),
        "website_title": website_title,
        "website_url": url,
        "search_country": country_code.upper(),
        **seo,
    }
