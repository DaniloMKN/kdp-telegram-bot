from flask import Flask, request
import telebot
import os
import random

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

power_words = ["Completo", "Definitivo", "Pratico", "Avanzato", "Strategico", "Illustrato"]
categories = {
    "auto": "Ingegneria Meccanica / Restauro Auto",
    "orto": "Giardinaggio / Coltivazione Domestica",
    "vino": "Enologia / Turismo Enogastronomico",
    "mente": "Crescita Personale / Psicologia Applicata"
}

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
        return "Domanda Alta ma Nicchia Specifica"
    if score >= 60:
        return "Domanda Media Interessante"
    return "Domanda Generica Competitiva"

def search_intent(keyword):
    kw = keyword.lower()
    if "come" in kw or "guida" in kw:
        return "Tutorial / Problema da Risolvere"
    if any(char.isdigit() for char in kw):
        return "Passione / Progetto Specifico"
    return "Commerciale / Generico"

def market_saturation(keyword):
    words = len(keyword.split())
    if words >= 4:
        return "Bassa Saturazione (opportunità)"
    if words == 3:
        return "Media Saturazione"
    return "Alta Saturazione (molta concorrenza)"

def suggest_category(keyword):
    for key in categories:
        if key in keyword.lower():
            return categories[key]
    return "Categoria Generale Fai-da-Te / Manualistica"

@app.route('/')
def home():
    return "KDP Strategic Lab Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP STRATEGIC LAB ATTIVO\n\n"
        "/keyword parola\n"
        "/titolo argomento\n"
        "/idea argomento"
    )

@bot.message_handler(commands=['keyword'])
def keyword(message):
    kw = message.text.replace("/keyword", "").strip()
    if not kw:
        bot.reply_to(message, "Inserisci una keyword.")
        return

    score = seo_score(kw)
    demand = demand_indicator(score)
    intent = search_intent(kw)
    saturation = market_saturation(kw)
    category = suggest_category(kw)

    response = f"""
🔎 ANALISI STRATEGICA AVANZATA

📌 Keyword: {kw}
📊 SEO Score: {score}/100
📈 Domanda Stimata: {demand}
🧠 Intento Ricerca: {intent}
📉 Saturazione Mercato: {saturation}
🎯 Categoria KDP Suggerita:
{category}
"""

    bot.reply_to(message, response)

@bot.message_handler(commands=['idea'])
def idea(message):
    topic = message.text.replace("/idea", "").strip()
    if not topic:
        bot.reply_to(message, "Inserisci un argomento.")
        return

    structure = f"""
🛠 IDEA LIBRO COMPLETA

📘 Titolo:
{topic.title()} – Guida Pratica per Principianti

📚 Struttura Capitoli:
1. Introduzione e errori comuni
2. Strumenti necessari
3. Metodo passo dopo passo
4. Problemi frequenti e soluzioni
5. Tecniche avanzate
6. Manutenzione e ottimizzazione

🎯 Target:
Appassionati e principianti che vogliono risultati pratici.
"""

    bot.reply_to(message, structure)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
