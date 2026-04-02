import asyncio
import json
import os
import urllib.parse
from dotenv import load_dotenv

from src.core.engine import OSINTEngine
from src.modules.carrier_api import CarrierModule
from src.modules.dorking import DorkingModule
from src.modules.social import WhatsAppModule, TelegramModule
from src.modules.duck_scanner import DuckScanner
from src.modules.deep_scraper import DeepScraper
from src.modules.geolocator import GeolocatorModule
from src.modules.instagram_check import InstagramModule
from src.core.analyzer import OSINTAnalyzer
from src.utils.display import print_rich_table
from src.utils.reporter import HTMLReporter


async def main():
    # 1. Caricamento configurazione da file .env
    load_dotenv()

    if not os.path.exists("data"):
        os.makedirs("data")

    # 2. Inizializzazione Engine
    engine = OSINTEngine()

    # Registrazione moduli Round 1
    engine.register_module(CarrierModule("HLR-Check"))  # Ora usa Numverify tramite .env
    engine.register_module(WhatsAppModule("Whatsapp"))
    engine.register_module(TelegramModule("Telegram"))
    engine.register_module(DorkingModule("Google-Dorking"))
    engine.register_module(DuckScanner("Duck-Scanner"))

    target_number = "+393331234567"  # Inserisci il numero da testare

    try:
        # 3. ROUND 1: Scansione Moduli Base
        results = await engine.scan(target_number)

        # 4. ROUND 2: Geolocalizzazione dinamica basata sul Carrier Reale
        # Recuperiamo il carrier confermato da Numverify per evitare errori di portabilità
        real_carrier = results.get("HLR-Check", {}).get("carrier", "")
        print(f"[*] Carrier rilevato: {real_carrier if real_carrier else 'Sconosciuto'}")

        geo_mod = GeolocatorModule("Geo-IP")
        geo_results = await geo_mod.run(target_number, carrier_real=real_carrier)
        results["Geo-IP"] = geo_results

        # 5. ROUND 3: Pulizia Link e Deep Scraping
        clean_links = []
        if "Duck-Scanner" in results:
            raw_links = results["Duck-Scanner"].get("top_links", [])
            for link in raw_links:
                if "uddg=" in link:
                    parsed_url = urllib.parse.urlparse(link)
                    actual_url = urllib.parse.parse_qs(parsed_url.query).get('uddg')
                    if actual_url:
                        clean_links.append(actual_url[0])
                elif link.startswith("http"):
                    clean_links.append(link)

        if clean_links:
            print(f"[*] Analisi profonda di {len(clean_links)} link reali...")
            scraper = DeepScraper("Deep-Analysis")
            deep_results = await scraper.run_on_links(clean_links)
            results["Deep-Analysis"] = deep_results
            # Salviamo i link puliti per il report HTML
            results["Clean-Links"] = clean_links

        # 6. ROUND 4: Social Identity Check (Instagram)
        usernames = results.get("Deep-Analysis", {}).get("potential_usernames", [])
        if usernames:
            print(f"[*] Verifica identità social per username: {usernames[0]}...")
            insta = InstagramModule("Instagram")
            insta_res = await insta.run_with_username(usernames[0])
            results["Instagram"] = insta_res

        # 7. ROUND 5: AI Correlation & Final Report
        report = OSINTAnalyzer.generate_report(results)
        results["AI-Analysis"] = report

        # 8. Output e Salvataggio
        print_rich_table(results)

        # Salvataggio JSON
        safe_name = target_number.replace("+", "").replace(" ", "")
        json_path = os.path.join("data", f"{safe_name}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        # Generazione Report HTML Professionale
        html_path = HTMLReporter.generate(results, target_number)

        print(f"\n[+] Investigazione completata con successo.")
        print(f"[>] Report JSON: {json_path}")
        print(f"[>] Report HTML: {html_path}")

    except Exception as e:
        print(f"[!] Errore critico durante l'esecuzione: {e}")


if __name__ == "__main__":
    asyncio.run(main())