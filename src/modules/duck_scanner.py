import httpx
from bs4 import BeautifulSoup
from src.modules.base_module import BaseModule
from typing import Dict, Any, List


class DuckScanner(BaseModule):
    async def run(self, phone_number: str) -> Dict[str, Any]:
        # Formato ricerca: "3331234567"
        query = f'"{phone_number}"'
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

        async with httpx.AsyncClient(headers=headers) as client:
            try:
                response = await client.get(url, timeout=15.0)
                soup = BeautifulSoup(response.text, "html.parser")
                links = []

                # DuckDuckGo HTML parsing
                for a in soup.find_all('a', class_='result__a'):
                    links.append(a['href'])

                return {
                    "found_on_ddg": len(links),
                    "top_links": links[:5]  # Prendiamo i primi 5 più rilevanti
                }
            except Exception as e:
                return {"error": str(e)}