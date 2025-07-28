import tldextract


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
            full_domain = ".".join(part for part in [extracted.subdomain, extracted.domain, extracted.suffix] if part)
            if not any(blocked in full_domain for blocked in blocked_domains):
                filtered.append(url)
        except Exception as e:
            print(f"[WARN] Skipping invalid URL: {url} — {e}")
            continue

    return filtered
