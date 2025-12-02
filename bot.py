import os
import requests
import time
import json
from telegram import Bot
from telegram.constants import ParseMode

# 🔥 NON TOCCARE — railway mette qui le variabili
TOKEN = "8589757816:AAEr-2b_ChchbGy3qYm_BlLt3DWiRq031bw"
CHAT_ID = 710201368

# 🔥 ENDPOINT STABILE DI VINTED
SEARCH_URL = (
    "https://www.vinted.it/api/v2/catalog/items"
    "?page=1&per_page=50&search_text=beyblade+x&order=newest_first"
)

# Header per evitare blocchi Cloudflare
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

bot = Bot(token=TOKEN)

# Carica lista degli ID già inviati
try:
    with open("items_cache.json", "r") as f:
        seen = json.load(f)
except:
    seen = []


def send_item(item):
    title = item.get("title", "Senza titolo")
    price = item.get("price_with_currency", "N/A")
    url = f"https://www.vinted.it/items/{item['id']}"
    photo = item["photo"]["url"]

    caption = (
        f"🆕 *Nuovo articolo Beyblade X!*\n\n"
        f"📛 *{title}*\n"
        f"💶 {price}\n"
        f"🔗 [Apri su Vinted]({url})"
    )

    bot.send_photo(
        chat_id=CHAT_ID,
        photo=photo,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
    )


def check_vinted():
    global seen

    try:
        r = requests.get(SEARCH_URL, headers=HEADERS, timeout=10)

        # Tenta di interpretare la risposta come JSON
        try:
            response = r.json()
        except Exception:
            print("⚠️ Risposta non JSON da Vinted, salto...")
            print("Contenuto ricevuto:", r.text[:200])
            return

        items = response.get("items", [])
        if not items:
            print("⚠️ Nessun item trovato, possibile filtro attivo da Vinted.")
            return

    except Exception as e:
        print("Errore nella richiesta:", e)
        return

    for item in items:
        _id = item["id"]

        if _id in seen:
            continue
        if item.get("is_sold", False):
            continue

        send_item(item)

        seen.insert(0, _id)
        if len(seen) > 50:
            seen = seen[:50]

    with open("items_cache.json", "w") as f:
        json.dump(seen, f)


if __name__ == "__main__":
    print("Bot avviato! Controllo Vinted ogni 60 secondi...")
    while True:
        try:
            check_vinted()
        except Exception as e:
            print("🛑 Errore generale:", e)
        time.sleep(60)
