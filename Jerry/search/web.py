from ddgs import DDGS
import requests

class WebSearch:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 5) -> str:
        results = self._duckduckgo(query, max_results)
        if not results:
            results = self._google_fallback(query)
        return results

    def _duckduckgo(self, query: str, max_results: int = 5) -> str:
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            if not results:
                return ""
            output = f"Search results for: '{query}'\n\n"
            for i, r in enumerate(results, 1):
                output += f"{i}. {r.get('title', 'No title')}\n"
                output += f"   {r.get('body', 'No description')[:200]}\n"
                output += f"   URL: {r.get('href', '')}\n\n"
            return output
        except Exception as e:
            return ""

    def _google_fallback(self, query: str) -> str:
        try:
            from googlesearch import search
            results = list(search(query, num_results=5))
            if not results:
                return "No results found."
            output = f"Google results for: '{query}'\n\n"
            for i, url in enumerate(results, 1):
                output += f"{i}. {url}\n"
            return output
        except Exception as e:
            return f"Search failed: {str(e)}"

    def news_search(self, query: str) -> str:
        try:
            results = list(self.ddgs.news(query, max_results=5))
            output = f"News for: '{query}'\n\n"
            for r in results:
                output += f"- {r.get('title')}\n  {r.get('url')}\n  {r.get('date', '')}\n\n"
            return output
        except Exception as e:
            return f"News search failed: {str(e)}"
