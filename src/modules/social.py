import httpx
from src.modules.base_module import BaseModule
from typing import Dict, Any


class WhatsAppModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.base_url = "https://api.whatsapp.com/send/?phone="

    async def run(self, phone_number: str) -> Dict[str, Any]:
        # Puliamo il numero (WhatsApp vuole solo cifre)
        clean_number = "".join(filter(str.isdigit, phone_number))
        url = f"{self.base_url}{clean_number}"

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(url)
                # Se il numero NON esiste, WhatsApp spesso reindirizza o mostra
                # messaggi specifici nel corpo HTML.
                # Questa è una versione semplificata:
                if response.status_code == 200:
                    exists = "Chat on WhatsApp with" in response.text
                    return {
                        "platform": "WhatsApp",
                        "account_exists": exists,
                        "link": url if exists else "N/A"
                    }
                return {"status": "error", "message": "WhatsApp API unreachable"}
            except Exception as e:
                return {"status": "error", "message": str(e)}


class TelegramModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.base_url = "https://t.me/"

    async def run(self, phone_number: str) -> Dict[str, Any]:
        # Telegram vuole il numero col + (es: +39333...)
        clean_number = "+" + "".join(filter(str.isdigit, phone_number))
        url = f"{self.base_url}{clean_number}"

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            try:
                response = await client.get(url)
                # Se il numero esiste, Telegram mostra un pulsante "SendMessage"
                # o il nome dell'utente nell'HTML.
                exists = "tgme_page_extra" in response.text or "extra_info" in response.text

                return {
                    "platform": "Telegram",
                    "account_exists": exists,
                    "link": url if exists else "N/A",
                    "note": "Check manuale consigliato per bio/foto" if exists else "Non trovato"
                }
            except Exception as e:
                return {"status": "error", "message": str(e)}