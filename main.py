from flask import Flask, request
import telebot
import os
import random

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def seo_score(keyword):
    score = 40
    words = len(keyword.split())

    if words >= 4:
        score += 20
    if any(char.isdigit() for char in keyword):
        score += 15
    if "guida" in keyword.lower():
        score += 10

    return min(score, 100)

def demand_indicator(score):
    if score >= 75:
        return "Alta (Verticale Specifica)"
    if score >= 60:
        return "Media Interessante"
    return "Generica Competitiva"

def search_intent(keyword):
    kw = keyword.lower()
    if "come" in kw or "guida" in kw:
        return "Tutorial / Problema"
    if any(char.isdigit() for char in kw):
        return "Passione Specifica"
    return "Commerciale Generico"

def market_saturation(keyword):
    words = len(keyword.split())
    if words >= 4:
        return "Bassa (Opportunità)"
    if words == 3:
        return "Media"
    return "Alta"

def commercial_value(score, saturation):
    if score >= 75 and "Bassa" in saturation:
        return "Ottimo potenziale Micro-Nicchia"
    if score >= 60:
        return "Buon potenziale ma competitivo"
    return "Serve differenziazione forte"

def price_suggestion(score):
    if score >= 75:
        return "Prezzo consigliato: 14.99€ - 19.99€"
    if score >= 60:
        return "Prezzo consigliato: 12.99€ - 14.99€"
    return "Prezzo consigliato: 9.99€ - 12.99€"

def pages_suggestion(score):
    if score >= 75:
        return "Lunghezza consigliata: 120-180 pagine"
    if score >= 60:
        return "Lunghezza consigliata: 90-130 pagine"
    return "Lunghezza consigliata: 70-100 pagine"

@app.route('/')
def home():
    return "KDP RADAR Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP RADAR COMPLETO ATTIVO\n\n"
        "Scrivi semplicemente una keyword dopo /radar\n"
        "Esempio:\n"
        "/radar restauro fiat uno 1990"
    )

@bot.message_handler(commands=['radar'])
def radar(message):
    kw = message.text.replace("/radar", "").strip()
    if not kw:
        bot.reply_to(message, "Inserisci una keyword dopo /radar")
        return

    score = seo_score(kw)
    demand = demand_indicator(score)
    intent = search_intent(kw)
    saturation = market_saturation(kw)
    commercial = commercial_value(score, saturation)
    price = price_suggestion(score)
    pages = pages_suggestion(score)

    collection_strategy = f"""
📚 Strategia Collana:

1. Libro Base: {kw.title()} – Guida Completa
2. Versione Budget / Principianti
3. Versione Avanzata Tecnica
4. Manuale Illustrato
5. Workbook / Checklist Operativa
"""

    response = f"""
🔎 KDP RADAR ANALYSIS

📌 Keyword: {kw}
📊 SEO Score: {score}/100
📈 Domanda: {demand}
🧠 Intento: {intent}
📉 Saturazione: {saturation}

💰 Valore Commerciale:
{commercial}

🏷 {price}
📖 {pages}

{collection_strategy}
"""

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
