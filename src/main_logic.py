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
from src.utils.reporter import HTMLReporter


async def run_full_scan(target_number: str):
    load_dotenv()

    if not os.path.exists("data"):
        os.makedirs("data")

    engine = OSINTEngine()
    engine.register_module(CarrierModule("HLR-Check"))
    engine.register_module(WhatsAppModule("Whatsapp"))
    engine.register_module(TelegramModule("Telegram"))
    engine.register_module(DorkingModule("Google-Dorking"))
    engine.register_module(DuckScanner("Duck-Scanner"))

    # ROUND 1
    results = await engine.scan(target_number)

    # ROUND 2: Geo
    real_carrier = results.get("HLR-Check", {}).get("carrier", "")
    geo_mod = GeolocatorModule("Geo-IP")
    geo_results = await geo_mod.run(target_number, carrier_real=real_carrier)
    results["Geo-IP"] = geo_results

    # ROUND 3: Deep Analysis
    clean_links = []
    if "Duck-Scanner" in results:
        raw_links = results["Duck-Scanner"].get("top_links", [])
        for link in raw_links:
            if "uddg=" in link:
                parsed_url = urllib.parse.urlparse(link)
                actual_url = urllib.parse.parse_qs(parsed_url.query).get('uddg')
                if actual_url: clean_links.append(actual_url[0])
            elif link.startswith("http"):
                clean_links.append(link)

    if clean_links:
        scraper = DeepScraper("Deep-Analysis")
        deep_results = await scraper.run_on_links(clean_links)
        results["Deep-Analysis"] = deep_results
        results["Clean-Links"] = clean_links

    # ROUND 4: Instagram
    usernames = results.get("Deep-Analysis", {}).get("potential_usernames", [])
    if usernames:
        insta = InstagramModule("Instagram")
        insta_res = await insta.run_with_username(usernames[0])
        results["Instagram"] = insta_res

    # ROUND 5: AI Analysis
    report_ai = OSINTAnalyzer.generate_report(results)
    results["AI-Analysis"] = report_ai

    # Salvataggio
    safe_name = target_number.replace("+", "").replace(" ", "")
    json_path = os.path.join("data", f"{safe_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    html_path = HTMLReporter.generate(results, target_number)

    # Restituiamo i percorsi e il riassunto IA al bot
    return json_path, html_path, report_ai