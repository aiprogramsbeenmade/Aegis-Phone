from src.modules.base_module import BaseModule
from typing import Dict, Any


class GeolocatorModule(BaseModule):
    def __init__(self, name: str):
        super().__init__(name)
        # Database prefissi
        self.prefix_data = {
            "333": {"reg": "Lombardia (TIM)", "lat": 45.4642, "lon": 9.1899},
            "335": {"reg": "Piemonte (TIM)", "lat": 45.0703, "lon": 7.6868},
            "347": {"reg": "Veneto (Vodafone)", "lat": 45.4343, "lon": 12.3388},
            "348": {"reg": "Lazio (Vodafone)", "lat": 41.8919, "lon": 12.5113},
            "320": {"reg": "Campania (WindTre)", "lat": 40.8518, "lon": 14.2681},
            "328": {"reg": "Sicilia (WindTre)", "lat": 38.1157, "lon": 13.3615},
        }

    # AGGIUNTO: carrier_real=None come argomento
    async def run(self, phone_number: str, carrier_real: str = None) -> Dict[str, Any]:
        clean = phone_number.replace("+39", "").replace(" ", "")
        prefix = clean[:3]

        # Logica: Se Numverify ci dà WindTre ma il prefisso è TIM,
        # diamo priorità al Carrier reale per la zona.
        if carrier_real and "Wind" in carrier_real:
            info = {"reg": "WindTre Network (Hub Sud/Nazionale)", "lat": 40.8518, "lon": 14.2681}
        elif carrier_real and "Vodafone" in carrier_real:
            info = {"reg": "Vodafone Network (Hub Centro)", "lat": 41.8919, "lon": 12.5113}
        else:
            # Fallback sul prefisso originale
            info = self.prefix_data.get(prefix, {"reg": "Italia (Generico)", "lat": 41.8719, "lon": 12.5674})

        return {
            "estimated_region": info["reg"],
            "coordinates": {"lat": info["lat"], "lon": info["lon"]},
            "map_url": f"https://www.google.com/maps?q={info['lat']},{info['lon']}"
        }