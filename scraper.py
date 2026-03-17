import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Connection": "keep-alive",
}


def fetch_html(session: requests.Session, url: str, timeout: int = 15) -> str:
    response = session.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
    response.raise_for_status()
    return response.text


def extract_visible_text(html: str, max_chars: int = 5000) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "img"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    return text[:max_chars]


def scrape_multiple_pages(base_url: str) -> str:
    candidate_paths = ["", "/about", "/business", "/enterprise", "/pricing"]
    collected = []

    with requests.Session() as session:
        for path in candidate_paths:
            try:
                url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
                html = fetch_html(session, url)
                text = extract_visible_text(html)

                if text and text not in collected:
                    collected.append(f"[SOURCE: {url}]\n{text}")
            except requests.HTTPError as exc:
                status_code = exc.response.status_code if exc.response is not None else "unknown"
                if status_code == 403:
                    continue
            except Exception:
                continue

    if not collected:
        return "SCRAPE_ERROR: all candidate pages failed or were blocked"

    return "\n\n".join(collected)