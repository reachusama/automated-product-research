from googleapiclient.discovery import build
from config.settings import API_KEY, SEARCH_ENGINE_ID, MAX_RESULTS_PER_QUERY

def google_search(query, country_code="us"):
    country_params = {
        "uk": {"gl": "uk", "cr": "countryUK"},
        "us": {"gl": "us", "cr": "countryUS"},
        "ca": {"gl": "ca", "cr": "countryCA"},
        "au": {"gl": "au", "cr": "countryAU"},
        "in": {"gl": "in", "cr": "countryIN"},
    }
    params = country_params.get(country_code, country_params["us"])
    service = build("customsearch", "v1", developerKey=API_KEY)

    result = service.cse().list(
        q=query,
        cx=SEARCH_ENGINE_ID,
        gl=params["gl"],
        cr=params["cr"],
        num=MAX_RESULTS_PER_QUERY
    ).execute()

    return [item["link"] for item in result.get("items", [])]
