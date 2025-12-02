import requests
import time
import json
from telegram import Bot
from telegram.constants import ParseMode

TOKEN = "8204117648:AAHvr49PHXwcU93jMoFXW0C9bniPoDsBjWY"
CHAT_ID = 710201368

SEARCH_URL = "https://www.vinted.it/api/v2/items?order=newest_first&search_text=beyblade+x"

bot = Bot(token=TOKEN)

try:
    with open("items_cache.json", "r") as f:
        seen = json.load(f)
except:
    seen = []

def send_item(item):
    title = item.get("title", "")
    price = item.get("price_with_currency", "")
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

    response = requests.get(SEARCH_URL).json()
    items = response.get("items", [])

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
            print("Errore:", e)
        time.sleep(60)
