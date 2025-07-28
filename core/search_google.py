from time import sleep

from googleapiclient.discovery import build

from config.settings import API_KEY, MAX_RESULTS_PER_QUERY, SEARCH_ENGINE_ID


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
