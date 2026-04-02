from typing import Dict, Any, List


class OSINTAnalyzer:
    @staticmethod
    def generate_report(data: Dict[str, Any]) -> str:
        """
        Analizza i dati raccolti da tutti i moduli e genera una
        valutazione sintetica del profilo target.
        """
        analysis: List[str] = []

        # --- 1. Carrier & Network Check ---
        hlr = data.get("HLR-Check", {})
        carrier = hlr.get("carrier", "Unknown")
        valid = hlr.get("valid", False)

        if valid:
            analysis.append(f"[*] Numero VALIDATO su rete {carrier}.")
            # Se è un operatore infrastrutturale, è probabilmente una SIM reale
            if any(op in carrier for op in ["Telecom", "Vodafone", "Wind", "Orange", "AT&T"]):
                analysis.append("    -> [User Type]: Probabile SIM fisica (Contratto/Ricaricabile).")
        else:
            analysis.append("[!] Numero NON attivo o non presente nei DB carrier.")

        # --- 2. Social Footprint ---
        wa = data.get("Whatsapp", {}).get("account_exists", False)
        tg = data.get("Telegram", {}).get("account_exists", False)

        if wa and tg:
            analysis.append("[+] Presenza Sociale: ELEVATA (Attivo su WhatsApp e Telegram).")
        elif wa or tg:
            status = "WhatsApp" if wa else "Telegram"
            analysis.append(f"[+] Presenza Sociale: MEDIA (Rilevato solo su {status}).")

        # --- 3. Analisi degli Interessi (Deep Scraping) ---
        deep = data.get("Deep-Analysis", {})
        titles = deep.get("associated_names", [])
        emails = deep.get("emails_found", [])

        # Parole chiave per profilazione automatica
        tech_keywords = ["Home Assistant", "GitHub", "StackOverflow", "Python", "Dev", "Configuration"]
        interest_found = False

        for title in titles:
            # Profilazione tecnica
            if any(key.lower() in title.lower() for key in tech_keywords):
                if not interest_found:
                    analysis.append("[i] Profilo Psicografico: Interessato a DOMOTICA/TECH/SVILUPPO.")
                    interest_found = True

            # Partecipazione a community
            if "Community" in title or "Forum" in title or "Topic" in title:
                analysis.append(f"    -> [Attività]: Partecipa a community online ('{title[:40]}...')")

        # --- 4. Identità Correlate (Email) ---
        if emails:
            unique_emails = list(set(emails))
            analysis.append(f"[!] Identità Trovata: Associate {len(unique_emails)} email ({', '.join(unique_emails)}).")

        # --- 5. Rischio & Leak ---
        leak_data = data.get("Leak-Check", {})
        leaks = leak_data.get("potential_leaks_found", 0)

        if leaks > 0:
            analysis.append(f"[CRITICAL] Il numero appare in {leaks} database di Leak/Pastebin!")
            analysis.append("    -> [Azione]: Verificare i link nel modulo 'Leak-Check'.")

        # --- 6. Conclusione ---
        if not analysis:
            return "Nessuna correlazione significativa rilevata. Impronta digitale minima."

        # Uniamo le stringhe per la visualizzazione nella tabella Rich
        return "\n".join(analysis)