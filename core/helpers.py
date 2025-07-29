import re
import unicodedata
import urllib.parse
from urllib.parse import urlparse

import tldextract

from config.settings import BLOCKED_EXTENSIONS, IRRELEVANT_DOMAINS


def extract_registered_domain(yahoo_url):
    """
    Extract domain from yahoo url.
    :param yahoo_url:
    :return:
    """
    ru_index = yahoo_url.find("RU=")
    if ru_index == -1:
        return None

    encoded_ru = yahoo_url[ru_index + 3 :]  # after "RU="
    real_url = urllib.parse.unquote(encoded_ru.split("/RK=")[0])  # stop at RK=

    # Step 2: Use tldextract to get the domain parts
    extracted = tldextract.extract(real_url)
    if extracted.domain and extracted.suffix:
        return f"{extracted.domain}.{extracted.suffix}"


def deduplicate_base_domains(urls: list[str]) -> list[str]:
    """
    Deduplicate URLs based on their base domain (e.g., example.com or blog.example.com).
    Returns a list of base URLs like: https://example.com
    """
    seen = set()
    base_urls = []

    for url in urls:
        try:
            extracted = tldextract.extract(url)
            if not extracted.domain or not extracted.suffix:
                continue
            base_domain = f"{extracted.domain}.{extracted.suffix}"
            scheme = "https"  # default if not explicitly provided
            if url.startswith("http://"):
                scheme = "http"
            elif url.startswith("https://"):
                scheme = "https"
            base_url = f"{scheme}://{base_domain}"
            if base_url not in seen:
                seen.add(base_url)
                base_urls.append(base_url)
        except Exception as e:
            print(f"[WARN] Skipping invalid URL: {url} — {e}")
            continue

    return base_urls


def filter_domains_by_extension(
    urls: list[str],
    allowed_extensions: list[str] = None,
    blocked_extensions: list[str] = None,
) -> list[str]:
    """
    Filters URLs by their full domain suffix (e.g., 'com', 'org', 'ac.uk') using tldextract.
    """
    allowed_extensions = [ext.lstrip(".").lower() for ext in allowed_extensions or []]
    blocked_extensions = [ext.lstrip(".").lower() for ext in blocked_extensions or []]
    filtered = []

    for url in urls:
        try:
            extracted = tldextract.extract(url)
            suffix = extracted.suffix.lower()
            if allowed_extensions and suffix not in allowed_extensions:
                continue
            if blocked_extensions and suffix in blocked_extensions:
                continue
            filtered.append(url)
        except Exception as e:
            print(f"[WARN] Skipping invalid URL: {url} — {e}")
            continue

    return filtered


def filter_irrelevant_domains(urls: list[str], blocked_domains: list[str]) -> list[str]:
    """
    Filters out any URL that matches a blocked domain or subdomain using tldextract.

    Example blocked_domains: ['linkedin.com', 'medium.com', 'blog.google']
    """
    blocked_domains = [d.lower() for d in blocked_domains]
    filtered = []

    for url in urls:
        try:
            extracted = tldextract.extract(url)
            full_domain = ".".join(
                part
                for part in [extracted.subdomain, extracted.domain, extracted.suffix]
                if part
            )
            if not any(blocked in full_domain for blocked in blocked_domains):
                filtered.append(url)
        except Exception as e:
            print(f"[WARN] Skipping invalid URL: {url} — {e}")
            continue

    return filtered


def clean_raw_text(text: str) -> str:
    """
    Cleans raw website text by removing unnecessary whitespace,
    newlines, non-printable characters, and poorly formatted blocks.

    Args:
        text (str): The raw input text.

    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""

    # Normalize unicode characters
    text = unicodedata.normalize("NFKC", text)

    # Remove invisible/control characters
    text = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)

    # Replace multiple spaces or tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Replace multiple newlines or newlines with spaces
    text = re.sub(r"\n+", "\n", text)  # Collapse multiple newlines
    text = re.sub(r" *\n *", "\n", text)  # Trim around newlines
    text = re.sub(r"\n", " ", text)  # Replace newlines with space

    # Collapse multiple spaces again, post newline removal
    text = re.sub(r" +", " ", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text


def is_irrelevant_url(url):
    domain = urlparse(url).netloc.lower()
    return any(d in domain for d in IRRELEVANT_DOMAINS)


def process_yahoo_urls(urls):
    urls_processed = deduplicate_base_domains(urls)
    urls_domain_filter = filter_irrelevant_domains(
        urls_processed, blocked_domains=IRRELEVANT_DOMAINS
    )
    urls_domain_ext_filter = filter_domains_by_extension(
        urls_domain_filter, blocked_extensions=BLOCKED_EXTENSIONS
    )
    return urls_domain_ext_filter
