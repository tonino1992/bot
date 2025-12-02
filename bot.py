import os
import requests
import time
import json
from telegram import Bot
from telegram.constants import ParseMode

# 🔥 NON TOCCARE — railway mette qui le variabili
TOKEN = "8589757816:AAEr-2b_ChchbGy3qYm_BlLt3DWiRq031bw"
CHAT_ID = 710201368

SEARCH_URL = "https://www.vinted.it/api/v2/items?order=newest_first&search_text=beyblade+x"

bot = Bot(token=TOKEN)

# Carica file degli ID già inviati
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
        parse_mode=ParseMode.MARKDOWN
    )

def check_vinted():
    global seen

def check_vinted():
    global seen

    try:
        r = requests.get(SEARCH_URL, timeout=10)
        
        # Se la risposta NON è JSON → salta
        try:
            response = r.json()
        except:
            print("Risposta non JSON da Vinted, skip...")
            return

        items = response.get("items", [])

    except Exception as e:
        print("Errore nella richiesta:", e)
        return

    for item in items:
        _id = item["id"]

        # Se già visto → salta
        if _id in seen:
            continue

        # Se venduto → non inviare
        if item.get("is_sold", False):
            continue

        # Invia su Telegram
        send_item(item)

        # Aggiungi a lista ultimi 50
        seen.insert(0, _id)
        if len(seen) > 50:
            seen = seen[:50]

    # Salva la cache
    with open("items_cache.json", "w") as f:
        json.dump(seen, f)
    items = response.get("items", [])

    for item in items:
        _id = item["id"]

        # Se già visto → salta
        if _id in seen:
            continue

        # Se venduto → non inviare
        if item.get("is_sold", False):
            continue

        # Invia su Telegram
        send_item(item)

        # Aggiungi a lista ultimi 50
        seen.insert(0, _id)
        if len(seen) > 50:
            seen = seen[:50]

    # Salva la cache
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







