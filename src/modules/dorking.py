import httpx
import asyncio
import random
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from src.modules.base_module import BaseModule
from fake_useragent import UserAgent


class DorkingModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.ua = UserAgent()

    def _generate_variants(self, phone: str) -> List[str]:
        """Genera diverse formattazioni del numero per massimizzare la ricerca."""
        clean = phone.replace("+", "").replace(" ", "")
        # Esempio per +39 333 123 4567
        return [
            f'"{phone}"',  # Standard: "+393331234567"
            f'"{clean}"',  # Solo cifre: "393331234567"
            f'"{clean[2:]}"',  # Senza prefisso: "3331234567"
            f'"{phone[:3]} {phone[3:]}"'  # Con spazio: "+39 3331234567"
        ]

    async def run(self, phone_number: str) -> Dict[str, Any]:
        variants = self._generate_variants(phone_number)
        results = []

        # Siti critici dove spesso trapelano numeri
        targets = ["linkedin.com", "facebook.com", "twitter.com", "pastebin.com", "github.com"]

        async with httpx.AsyncClient(http2=True) as client:
            for variant in variants:
                # Costruiamo una dork specifica
                dork = f"{variant} (site:{' OR site:'.join(targets)})"
                url = f"https://www.google.com/search?q={dork}"

                headers = {"User-Agent": self.ua.random}

                try:
                    # Delay casuale per evitare il ban immediato
                    await asyncio.sleep(random.uniform(1.5, 3.0))

                    response = await client.get(url, headers=headers, timeout=10.0)

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        # Estraiamo i link (Google usa i tag <a> con pattern specifici)
                        for link in soup.find_all("a"):
                            href = link.get("href")
                            if href and "/url?q=" in href and "google.com" not in href:
                                actual_link = href.split("/url?q=")[1].split("&")[0]
                                results.append(actual_link)

                    elif response.status_code == 429:
                        return {"status": "rate_limited", "message": "Google ha rilevato troppe richieste."}

                except Exception as e:
                    continue

        return {
            "links_found": list(set(results)),  # Rimuove duplicati
            "variants_scanned": len(variants)
        }