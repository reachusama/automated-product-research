from time import sleep

from googleapiclient.discovery import build

from config.settings import API_KEY, MAX_RESULTS_PER_QUERY, SEARCH_ENGINE_ID
from playwright.sync_api import sync_playwright
from time import sleep


def google_search(query, country_code="us", max_pages=3):
    country_params = {
        "uk": {"gl": "uk", "cr": "countryUK"},
        "us": {"gl": "us", "cr": "countryUS"},
        "ca": {"gl": "ca", "cr": "countryCA"},
        "au": {"gl": "au", "cr": "countryAU"},
        "in": {"gl": "in", "cr": "countryIN"},
    }

    if country_code not in country_params:
        country_code = "us"
    params = country_params[country_code]

    service = build("customsearch", "v1", developerKey=API_KEY)

    urls = []
    for i in range(max_pages):
        start = 1 + i * 10
        try:
            result = (
                service.cse()
                .list(
                    q=query,
                    cx=SEARCH_ENGINE_ID,
                    gl=params["gl"],
                    cr=params["cr"],
                    num=MAX_RESULTS_PER_QUERY,
                    start=start,
                )
                .execute()
            )
            page_urls = [item["link"] for item in result.get("items", [])]
            urls.extend(page_urls)
            sleep(1)
        except Exception as e:
            print(f"[ERROR] Google CSE page {i + 1}: {e}")
            break

    return urls


def google_search_playwright(query, country_code="us", max_pages=3):
    # Google country localization codes
    country_params = {
        "uk": "gl=uk",
        "us": "gl=us",
        "ca": "gl=ca",
        "au": "gl=au",
        "in": "gl=in",
    }

    gl_param = country_params.get(country_code.lower(), "gl=us")

    urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        for i in range(max_pages):
            start = i * 10
            search_url = f"https://www.google.com/search?q={query}&start={start}&{gl_param}"

            try:
                page.goto(search_url, timeout=15000)
                sleep(2)  # Allow content to load

                # Extract result URLs
                results = page.locator("div.yuRUbf > a")  # Google's organic results
                count = results.count()

                for i in range(count):
                    href = results.nth(i).get_attribute("href")
                    if href:
                        urls.append(href)

                sleep(1)  # Avoid hitting rate limits

            except Exception as e:
                print(f"[ERROR] Google page {i + 1}: {e}")
                break

        browser.close()

    return list(set(urls))  # Deduplicate URLs
