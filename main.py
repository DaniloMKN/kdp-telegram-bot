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

def market_profile(score, words):
    if score >= 75 and words >= 4:
        return "Micro-Nicchia Verticale"
    if score >= 60:
        return "Nicchia Intermedia"
    return "Mercato Ampio Competitivo"

def positioning_strategy(profile):
    if "Micro" in profile:
        return "Dominio specifico + Autorità tecnica"
    if "Intermedia" in profile:
        return "Differenziazione forte + Metodo proprietario"
    return "Brand personale + Volume alto"

def authority_level(profile):
    if "Micro" in profile:
        return "Media/Alta (esperienza reale consigliata)"
    if "Intermedia" in profile:
        return "Media"
    return "Base / divulgativo"

def cover_type(profile):
    if "Micro" in profile:
        return "Copertina tecnica, concreta, professionale"
    return "Copertina emozionale / promessa forte"

def funnel_strategy(profile):
    if "Micro" in profile:
        return "Checklist + Gruppo Telegram + Versione avanzata"
    if "Intermedia" in profile:
        return "Mini ebook bonus + Newsletter"
    return "Lead magnet generico"

def operational_risk(words):
    if words >= 4:
        return "Basso rischio (target chiaro)"
    if words == 3:
        return "Rischio medio"
    return "Alto rischio saturazione"

@app.route('/')
def home():
    return "KDP Intelligent Strategist Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP INTELLIGENT STRATEGIST\n\n"
        "Scrivi:\n"
        "/analyze tua keyword"
    )

@bot.message_handler(commands=['analyze'])
def analyze(message):
    kw = message.text.replace("/analyze", "").strip()

    if not kw:
        bot.reply_to(message, "Inserisci una keyword dopo /analyze")
        return

    score = seo_score(kw)
    words = len(kw.split())
    profile = market_profile(score, words)
    positioning = positioning_strategy(profile)
    authority = authority_level(profile)
    cover = cover_type(profile)
    funnel = funnel_strategy(profile)
    risk = operational_risk(words)

    response = f"""
🧠 ANALISI STRATEGICA AVANZATA

📌 Keyword: {kw}
📊 SEO Score: {score}/100
🎯 Profilo Mercato: {profile}

🚀 Posizionamento Consigliato:
{positioning}

🎓 Livello Autorità Necessario:
{authority}

🎨 Tipo Copertina:
{cover}

📦 Strategia Funnel:
{funnel}

⚠️ Rischio Operativo:
{risk}

📚 Espansione Consigliata:
1. Libro Base
2. Versione Specializzata
3. Workbook operativo
4. Edizione Illustrata
5. Upsell avanzato
"""

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
