from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config.settings import HEADERS
from core.helpers import is_irrelevant_url


def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] Fetching {url}: {e}")
        return None


def extract_seo_meta(soup):
    def get(name):
        tag = soup.find("meta", attrs={"name": name}) or soup.find(
            "meta", attrs={"property": name}
        )
        return tag["content"] if tag and "content" in tag.attrs else ""

    return {
        "seo_title_tag": soup.title.string.strip() if soup.title else "",
        "seo_meta_description": get("description"),
        "seo_og_title": get("og:title"),
        "seo_og_description": get("og:description"),
        "seo_og_locale": get("og:locale"),
        "seo_twitter_title": get("twitter:title"),
        "seo_twitter_description": get("twitter:description"),
        "seo_canonical_link": (
            soup.find("link", rel="canonical")["href"]
            if soup.find("link", rel="canonical")
            else ""
        ),
    }


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
