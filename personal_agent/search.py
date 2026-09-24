import httpx
from bs4 import BeautifulSoup


def search_web(query: str, limit: int = 5) -> list[dict[str, str]]:
    response = httpx.get("https://html.duckduckgo.com/html/", params={"q": query}, timeout=10, headers={"User-Agent": "personal-ai-agent/1.0"})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select(".result")[:limit]:
        link = item.select_one(".result__a")
        snippet = item.select_one(".result__snippet")
        if link:
            results.append({"title": link.get_text(" ", strip=True), "url": link.get("href", ""), "snippet": snippet.get_text(" ", strip=True) if snippet else ""})
    return results
