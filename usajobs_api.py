import requests

from utils.config import USAJOBS_API_KEY


def fetch_usajobs(keyword, location=None, results_per_page=10):
    """
    Fetch job listings from USAJOBS API.

    Returns:
        tuple: (jobs_list, error_message). jobs_list is a list of job items;
        error_message is None on success, or a string describing the problem.
    """
    if not (USAJOBS_API_KEY or "").strip():
        return [], "USAJOBS API key is missing. Add USAJOBS_API_KEY to your .env file."

    headers = {
        "Authorization-Key": USAJOBS_API_KEY.strip(),
        "Accept": "application/json",
        "User-Agent": "JobHuntAssistant/1.0 (Streamlit; USAJOBS API client)",
    }
    params = {
        "Keyword": keyword,
        "ResultsPerPage": min(results_per_page, 25),
    }
    if location and str(location).strip():
        params["LocationName"] = str(location).strip()

    url = "https://data.usajobs.gov/api/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
    except requests.RequestException as e:
        return [], f"Request failed: {e}"

    if response.status_code != 200:
        try:
            body = response.json()
            msg = body.get("Message") or body.get("message") or response.text[:200]
        except Exception:
            msg = response.text[:200] if response.text else f"HTTP {response.status_code}"
        return [], f"USAJOBS API error (HTTP {response.status_code}): {msg}"

    data = response.json()
    jobs = data.get("SearchResult", {}).get("SearchResultItems", [])
    return jobs, None
