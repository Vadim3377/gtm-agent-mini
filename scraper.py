import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str, timeout: int = 15) -> str:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def extract_visible_text(html: str, max_chars: int = 8000) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript", "svg", "img"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())

    return text[:max_chars]


def scrape_website_text(url: str) -> str:
    try:
        html = fetch_html(url)
        return extract_visible_text(html)
    except Exception as exc:
        return f"SCRAPE_ERROR: {exc}"