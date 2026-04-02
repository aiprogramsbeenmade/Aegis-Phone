import httpx
import os
from dotenv import load_dotenv
from src.modules.base_module import BaseModule
from typing import Dict, Any

load_dotenv()


class CarrierModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        self.api_key = os.getenv("NUMVERIFY_API_KEY")
        self.base_url = "http://apilayer.net/api/validate"

    async def run(self, phone_number: str) -> Dict[str, Any]:
        if not self.api_key:
            print("[!] Errore: NUMVERIFY_API_KEY non trovata nel file .env")
            return {"carrier": "Unknown", "valid": False}

        clean_number = phone_number.replace("+", "").replace(" ", "")
        params = {"access_key": self.api_key, "number": clean_number, "format": 1}

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(self.base_url, params=params)
                data = response.json()

                if data.get("valid"):
                    return {
                        "carrier": data.get("carrier", "Unknown"),
                        "location": data.get("location", "Italy"),
                        "line_type": data.get("line_type", "mobile"),
                        "valid": True
                    }
            except Exception as e:
                print(f"[!] Errore API Numverify: {e}")

        return {"carrier": "Unknown", "valid": False}