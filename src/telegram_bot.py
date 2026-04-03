import os
import asyncio
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from typing import Callable, Dict, Any, Awaitable
import json
import logging


# Importiamo la logica
from src.main_logic import run_full_scan

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_ID = int(os.getenv("ALLOWED_USER_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# --- MIDDLEWARE DI SICUREZZA ---
class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id != ALLOWED_ID:
            await event.answer("❌ Accesso negato. Questo bot è privato.")
            return
        return await handler(event, data)


# Registriamo il middleware
dp.message.outer_middleware(AuthMiddleware())


# --- HANDLERS ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🛡️ **AegisPhone OSINT Bot** pronto.\n\nInvia un numero di telefono (es: +393331234567) per iniziare l'investigazione.")


@dp.message()
async def handle_message(message: types.Message):
    target = message.text.strip()

    if not target.startswith("+") or not target[1:].replace(" ", "").isdigit():
        await message.answer("⚠️ Formato non valido. Usa: +393331234567")
        return

    status_msg = await message.answer(f"🔎 *Investigazione avviata su* `{target}`\.\.\.", parse_mode="MarkdownV2")

    try:
        # Esecuzione logica (restituisce paths e report AI)
        json_path, html_path, summary = await run_full_scan(target)

        # Carichiamo i dati JSON per estrarre le info per la "tabella"
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Costruzione della "Tabella" testuale
        hlr = data.get('HLR-Check', {})
        wa = "✅" if data.get('Whatsapp', {}).get('account_exists') else "❌"
        tg = "✅" if data.get('Telegram', {}).get('account_exists') else "❌"
        ig = "✅" if data.get('Instagram', {}).get('exists') else "❌"
        geo = data.get('Geo-IP', {}).get('estimated_region', 'N/A')

        # Usiamo il font monospaziato per simulare la tabella
        table_msg = (
            f"📊 *RISULTATI SCANNER*\n"
            f"```\n"
            f"TARGET: {target}\n"
            f"--------------------------\n"
            f"CARRIER:  {hlr.get('carrier', 'N/A')}\n"
            f"TYPE:     {hlr.get('line_type', 'N/A')}\n"
            f"REGION:   {geo}\n"
            f"--------------------------\n"
            f"WHATSAPP: {wa}\n"
            f"TELEGRAM: {tg}\n"
            f"INSTAGRM: {ig}\n"
            f"--------------------------\n"
            f"```"
        )

        # 1. Invio Tabella Sintetica
        await message.answer(table_msg, parse_mode="MarkdownV2")

        # 2. Invio Analisi AI (formattata bene)
        await message.answer(f"🧠 *ANALISI INTELLIGENTE*\n\n{summary}")

        # 3. Invio Documento HTML
        report_file = FSInputFile(html_path)
        await bot.send_document(message.chat.id, report_file, caption=f"📄 Report HTML Completo")

    except Exception as e:
        logging.error(f"Errore: {e}")
        await message.answer(f"💥 *Errore durante la scansione*\n`{str(e)}`", parse_mode="MarkdownV2")
    finally:
        try:
            await status_msg.delete()
        except:
            pass


async def main():
    print("[!] AegisPhone Bot in ascolto...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())