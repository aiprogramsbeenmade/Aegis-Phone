from typing import Dict, Any


class HTMLReporter:
    @staticmethod
    def generate(data: Dict[str, Any], target: str):
        file_path = f"data/report_{target.replace('+', '')}.html"

        # Recupero coordinate per la mappa (default Italia se non trovate)
        geo = data.get('Geo-IP', {})
        coords = geo.get('coordinates', {'lat': 41.8719, 'lon': 12.5674})

        # Creazione dell'URL per il widget OpenStreetMap
        # Zoom 10 è perfetto per un'area cittadina/hub
        map_iframe_url = f"https://www.openstreetmap.org/export/embed.html?bbox={coords['lon'] - 0.1}%2C{coords['lat'] - 0.1}%2C{coords['lon'] + 0.1}%2C{coords['lat'] + 0.1}&layer=mapnik&marker={coords['lat']}%2C{coords['lon']}"

        html = f"""
        <!DOCTYPE html>
        <html lang="it">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AegisPhone Report - {target}</title>
            <style>
                body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #121212; color: #e0e0e0; padding: 40px; line-height: 1.6; }}
                .container {{ max-width: 900px; margin: auto; }}
                .card {{ background: #1e1e1e; border-radius: 12px; padding: 25px; margin-bottom: 25px; border-left: 6px solid #0078d4; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
                h1 {{ color: #0078d4; text-align: center; margin-bottom: 40px; text-transform: uppercase; letter-spacing: 2px; }}
                h2 {{ margin-top: 0; color: #4fc3f7; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #333; padding-bottom: 10px; }}
                .analysis {{ white-space: pre-wrap; font-family: 'Consolas', monospace; color: #00ffcc; background: #252525; padding: 15px; border-radius: 8px; border: 1px solid #333; }}
                .map-container {{ width: 100%; height: 300px; border-radius: 8px; overflow: hidden; margin-top: 15px; border: 1px solid #444; }}
                ul {{ list-style-type: none; padding: 0; }}
                li {{ margin-bottom: 12px; padding: 10px; background: #2a2a2a; border-radius: 6px; word-break: break-all; transition: 0.3s; }}
                li:hover {{ background: #333; }}
                a {{ color: #4fc3f7; text-decoration: none; }}
                a:hover {{ text-decoration: underline; }}
                .status-ok {{ color: #4caf50; font-weight: bold; }}
                .status-ko {{ color: #f44336; font-weight: bold; }}
                .info-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a2a2a; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🛡️ AegisPhone Intelligence Report</h1>
                <p style="text-align: center;">Target: <strong style="font-size: 1.4em; color: #4fc3f7;">{target}</strong></p>

                <div class="card">
                    <h2>🧠 AI Analysis</h2>
                    <div class="analysis">{data.get('AI-Analysis', 'N/A')}</div>
                </div>

                <div class="card">
                    <h2>📱 Social & Carrier Info</h2>
                    <div class="info-row"><span><strong>Carrier:</strong></span> <span>{data.get('HLR-Check', {}).get('carrier', 'N/A')}</span></div>
                    <div class="info-row"><span><strong>WhatsApp:</strong></span> <span>{'<span class="status-ok">✅ Trovato</span>' if data.get('Whatsapp', {}).get('account_exists') else '<span class="status-ko">❌ Non Trovato</span>'}</span></div>
                    <div class="info-row"><span><strong>Telegram:</strong></span> <span>{'<span class="status-ok">✅ Trovato</span>' if data.get('Telegram', {}).get('account_exists') else '<span class="status-ko">❌ Non Trovato</span>'}</span></div>
                    <div class="info-row"><span><strong>Instagram:</strong></span> <span>{f'<a href="{data.get("Instagram", {}).get("profile_url")}" target="_blank" class="status-ok">✅ Profilo Trovato</a>' if data.get('Instagram', {}).get('exists') else '<span class="status-ko">❌ Non trovato</span>'}</span></div>
                </div>

                <div class="card">
                    <h2>📍 Localizzazione Stimata (Prefisso/Carrier)</h2>
                    <p><strong>Regione/Hub:</strong> {geo.get('estimated_region', 'N/A')}</p>
                    <div class="map-container">
                        <iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{map_iframe_url}"></iframe>
                    </div>
                    <p style="font-size: 0.8em; color: #888; margin-top: 10px;">* La posizione è basata sulla centrale di smistamento del carrier associata al prefisso, non sul GPS reale.</p>
                </div>

                <div class="card">
                    <h2>🌐 Deep Web & Footprint</h2>
                    <ul>
                        {"".join([f"<li>🔗 <a href='{l}' target='_blank'>{l}</a></li>" for l in (data.get('Duck-Scanner', {}).get('top_links', []) or [])])}
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        return file_path