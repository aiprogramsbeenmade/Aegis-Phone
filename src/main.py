import asyncio
from src.main_logic import run_full_scan
from src.utils.display import print_rich_table
import json


async def main():
    target = input("Inserisci il numero (compreso di prefisso): ")  # Cambia col numero che vuoi
    json_p, html_p, summary = await run_full_scan(target)

    # Carichiamo i risultati per la tabella grafica
    with open(json_p, "r") as f:
        res = json.load(f)
    print_rich_table(res)
    print(f"\n[+] Analisi completata. Report: {html_p}")


if __name__ == "__main__":
    asyncio.run(main())