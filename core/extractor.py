import re

import spacy
from bs4 import BeautifulSoup
from spacy.matcher import PhraseMatcher

from config.settings import FEATURE_TERMS, HEADERS, TARGET_AUDIENCE_TERMS

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

matcher.add("TARGET_AUDIENCE", [nlp.make_doc(term) for term in TARGET_AUDIENCE_TERMS])
matcher.add("FEATURES", [nlp.make_doc(term) for term in FEATURE_TERMS])


def get_main_text(soup: BeautifulSoup) -> str:
    for tag in soup(["header", "footer", "nav", "aside", "script", "style"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)


def extract_matches(text, label):
    doc = nlp(text)
    matches = matcher(doc)
    return sorted(
        set(
            doc[start:end].text.lower()
            for match_id, start, end in matches
            if nlp.vocab.strings[match_id] == label
        )
    )


def extract_contact_info(text):
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.search(r"\+?\d[\d\s().-]{7,}", text)
    address = re.search(r"\d{1,5}\s\w+(\s\w+)+", text)
    return (
        email.group() if email else "",
        phone.group() if phone else "",
        address.group() if address else "",
    )


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
