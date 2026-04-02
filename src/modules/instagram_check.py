import httpx
from src.modules.base_module import BaseModule
from typing import Dict, Any


class InstagramModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)

    # Metodo obbligatorio per BaseModule
    async def run(self, phone_number: str) -> Dict[str, Any]:
        return {"status": "use_run_with_username"}

    async def run_with_username(self, username: str) -> Dict[str, Any]:
        """Verifica l'esistenza di un profilo Instagram tramite username."""
        url = f"https://www.instagram.com/{username}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with httpx.AsyncClient(headers=headers, timeout=10.0, follow_redirects=True) as client:
            try:
                resp = await client.get(url)
                # Instagram restituisce 200 se il profilo esiste, 404 se non esiste
                if resp.status_code == 200:
                    return {
                        "exists": True,
                        "profile_url": url,
                        "note": "Profilo rilevato."
                    }
                return {"exists": False}
            except Exception:
                return {"exists": False, "error": "Timeout o blocco connessione"}