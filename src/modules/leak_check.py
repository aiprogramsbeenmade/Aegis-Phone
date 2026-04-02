import httpx
from bs4 import BeautifulSoup
from src.modules.base_module import BaseModule
from typing import Dict, Any


class LeakCheckModule(BaseModule):
    async def run(self, phone_number: str) -> Dict[str, Any]:
        # Puliamo il numero per diverse ricerche nei leak
        clean_number = "".join(filter(str.isdigit, phone_number))

        # Dork specifica per archivi di testo e paste
        query = f'"{phone_number}" OR "{clean_number}" site:pastebin.com OR site:ghostbin.co OR site:github.com'
        url = f"https://html.duckduckgo.com/html/?q={query}"

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                resp = await client.get(url)
                soup = BeautifulSoup(resp.text, "html.parser")
                leaks = []

                for a in soup.find_all('a', class_='result__a'):
                    leaks.append(a['href'])

                return {
                    "potential_leaks_found": len(leaks),
                    "sources": leaks[:3],
                    "critical_alert": len(leaks) > 0
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}