import httpx
import re
import urllib.parse
from bs4 import BeautifulSoup
from src.modules.base_module import BaseModule
from typing import Dict, Any, List


class DeepScraper(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        # Regex avanzata per catturare email evitando falsi positivi comuni
        self.email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        # Regex per catturare menzioni social comuni (es. @username)
        self.social_regex = r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9_]+)'

    def _extract_potential_username(self, url: str) -> str:
        """Tenta di estrarre uno username analizzando la struttura dell'URL."""
        parsed = urllib.parse.urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        # Pattern comuni: /u/username, /profile/username, /user/username
        trigger_keywords = ['u', 'user', 'users', 'profile', 'member', 'author']

        for i, part in enumerate(path_parts):
            if part.lower() in trigger_keywords and i + 1 < len(path_parts):
                return path_parts[i + 1]

        # Se non trova keyword, restituisce l'ultima parte del path se sembra un nome
        if path_parts and len(path_parts[-1]) > 3:
            return path_parts[-1]

        return None

    async def run_on_links(self, links: List[str]) -> Dict[str, Any]:
        """Visita i link forniti ed estrae dati sensibili."""
        results = {
            "emails_found": [],
            "associated_names": [],
            "potential_usernames": [],
            "social_mentions": []
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
        }

        async with httpx.AsyncClient(headers=headers, timeout=12.0, follow_redirects=True) as client:
            for link in links:
                try:
                    # Estrazione username dall'URL stesso (prima di scaricare)
                    url_username = self._extract_potential_username(link)
                    if url_username:
                        results["potential_usernames"].append(url_username)

                    # Download della pagina
                    response = await client.get(link)
                    if response.status_code != 200:
                        continue

                    html_content = response.text
                    soup = BeautifulSoup(html_content, "html.parser")

                    # 1. Estrazione Titolo (Identità della pagina)
                    if soup.title and soup.title.string:
                        results["associated_names"].append(soup.title.string.strip())

                    # 2. Estrazione Email
                    emails = re.findall(self.email_regex, html_content)
                    results["emails_found"].extend(emails)

                    # 3. Estrazione Menzioni Social (@username)
                    # Spesso gli utenti firmano i post con il loro handle
                    socials = re.findall(self.social_regex, html_content)
                    results["social_mentions"].extend(socials)

                except Exception:
                    # In OSINT, molti link possono essere morti o bloccare i bot
                    continue

        blacklist = ['context', 'keyframes', 'media', 'type', 'import', 'font']

        cleaned_socials = [s for s in results["social_mentions"] if s.lower() not in blacklist and len(s) > 2]
        cleaned_emails = [e for e in results["emails_found"] if "discourse" not in e and "admin" not in e]

        return {
            "emails_found": list(set(cleaned_emails)),
            "associated_names": list(set(results["associated_names"])),
            "potential_usernames": list(set(results["potential_usernames"])),
            "social_mentions": list(set(cleaned_socials))
        }

    async def run(self, phone_number: str) -> Dict[str, Any]:
        """Implementazione obbligatoria dell'interfaccia BaseModule."""
        return {"status": "ready", "instruction": "Use run_on_links(links) after search modules"}