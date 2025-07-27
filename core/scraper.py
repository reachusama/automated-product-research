from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from config.settings import HEADERS
from core.extractor import (
    extract_contact_info,
    extract_matches,
    extract_seo_meta,
    get_main_text,
)


def get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[ERROR] Fetching {url}: {e}")
        return None


def process_url(keyword_category, keyword, url, country_code):
    soup = get_soup(url)
    if not soup:
        return None

    raw_text = get_main_text(soup)
    audience = extract_matches(raw_text, "TARGET_AUDIENCE")
    features = extract_matches(raw_text, "FEATURES")
    email, phone, address = extract_contact_info(raw_text)
    seo = extract_seo_meta(soup)

    return {
        "keyword_category": keyword_category,
        "keyword": keyword,
        "product_name": soup.title.string.strip() if soup.title else "",
        "website_url": url,
        "country": urlparse(url).netloc.split(".")[-1],
        "search_country": country_code.upper(),
        "address": address,
        "email": email,
        "phone_number": phone,
        "target_audience": ", ".join(audience),
        "delivery_platform": ", ".join(
            [f for f in features if f in ["web app", "LMS", "plugin", "mobile app"]]
        ),
        "integrations": ", ".join(
            [f for f in features if f not in ["web app", "LMS", "plugin", "mobile app"]]
        ),
        "raw_homepage_text": raw_text,
        "llm_summary": "",
        "business_description_point_1": "",
        "business_description_point_2": "",
        "business_description_point_3": "",
        "business_category_tags": "",
        "pricing_info": "",
        "product_stage": "",
        "funding_info": "",
        "partner_names": "",
        "source_url": url,
        "last_updated": datetime.utcnow().isoformat(),
        "scrape_notes": "",
        **seo,
    }
