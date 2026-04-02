# 🛡️ AegisPhone - Advanced OSINT Framework

AegisPhone è un potente strumento di investigazione digitale (OSINT) progettato per analizzare numeri di telefono. Il tool correla dati tecnici (HLR), presenza sui social media e impronte digitali trovate nel deep web per generare un report investigativo completo.

## ✨ Caratteristiche
- **HLR Real-time Lookup**: Identifica il carrier reale (anche con MNP) tramite Numverify.
- **Social Discovery**: Verifica profili su WhatsApp, Telegram e Instagram.
- **Deep Web Scraping**: Ricerca dorking automatizzata su Google e DuckDuckGo.
- **Intelligence Analysis**: Estrazione automatica di email e username da forum e community.
- **Geolocalizzazione**: Stima della posizione basata sugli hub di rete del carrier.
- **Report Professionale**: Genera report dettagliati in formato JSON e HTML interattivo.

---

## 🚀 Installazione

1. **Clona il repository**:
   ```bash
   git clone https://github.com/aiprogramsbeenmade/Aegis-Phone.git
   cd AegisPhone
   ```
2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configura le chiavi API**:
   ```bash
   NUMVERIFY_API_KEY=la_tua_chiave_qui
   ```
---

## 🛠️ Utilizzo
Modifica il numero target nel file `src/main.py` e avvia la scansione:
```bash
python src/main.py
```
Al termine, troverai i risultati nella cartella `/data.

---

## ⚠️ Disclaimer
Questo strumento è stato creato esclusivamente a scopo educativo e di ricerca sulla sicurezza. L'autore non si assume alcuna responsabilità per l'uso improprio o illegale di questo software. Utilizzare solo su numeri di cui si ha l'autorizzazione all'analisi.

## ⚖️ Licenza
Questo progetto è distribuito sotto la licenza **MIT**. Consulta il file `LICENSE` per ulteriori dettagli.