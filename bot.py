import os
import requests
import time
import json
from telegram import Bot
from telegram.constants import ParseMode

# 🔥 NON TOCCARE — railway mette qui le variabili
TOKEN = "8589757816:AAEr-2b_ChchbGy3qYm_BlLt3DWiRq031bw"
CHAT_ID = 710201368

# 🔥 Endpoint funzionante (quello del catalogo)
SEARCH_URL = "https://www.vinted.it/api/v2/catalog/items?page=1&per_page=20&search_text=beyblade+x&order=newest_first"

# 🔥 User-Agent per evitare blocchi
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

bot = Bot(token=TOKEN)

# 🔥 Carica ID degli oggetti già notificati
try:
    with open("items_cache.json", "r") as f:
        seen = json.load(f)
except:
    seen = []


def send_item(item):
    """Invia un articolo su Telegram."""
    title = item.get("title", "Senza titolo")
    price = item.get("price_with_currency", "N/A")
    item_id = item["id"]
    url = f"https://www.vinted.it/items/{item_id}"

    photo = None
    if item.get("photo"):
        photo = item["photo"].get("url")

    caption = (
        f"🆕 *Nuovo articolo Beyblade X!*\n\n"
        f"📛 *{title}*\n"
        f"💶 {price}\n"
        f"🔗 [Apri su Vinted]({url})"
    )

    # Se c'è foto → invia immagine
    if photo:
        bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        bot.send_message(
            chat_id=CHAT_ID,
            text=caption,
            parse_mode=ParseMode.MARKDOWN,
        )


def check_vinted():
    global seen

    try:
        r = requests.get(SEARCH_URL, headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"Errore connessione: {e}")
        return

    # 🔥 PARSING PROTETTO
    try:
        response = r.json()
    except Exception:
        print("⚠️ Risposta non JSON da Vinted, salto...")
        print("Contenuto ricevuto:", r.text[:200])
        return

    items = response.get("items", [])
    if not items:
        print("⚠️ Nessun item trovato o risposta vuota.")
        return

    for item in items:
        item_id = item["id"]

        if item_id in seen:
            continue

        if item.get("is_sold", False):
            continue

        send_item(item)

        # Aggiorna lista ultimi 50
        seen.insert(0, item_id)
        seen = seen[:50]

    # Salvare la cache
    with open("items_cache.json", "w") as f:
        json.dump(seen, f)


if __name__ == "__main__":
    print("Bot avviato! Controllo Vinted ogni 60 secondi...")
    while True:
        try:
            check_vinted()
        except Exception as e:
            print("Errore:", e)
        time.sleep(60)
