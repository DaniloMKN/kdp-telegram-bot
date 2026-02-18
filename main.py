from flask import Flask, request
import telebot
import os
import random
import re

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

power_words = [
    "Completo", "Definitivo", "Pratico", "Avanzato",
    "Strategico", "Professionale", "Illustrato",
    "Passo dopo Passo", "Aggiornato", "Intensivo"
]

time_frames = ["in 30 Giorni", "in 60 Giorni", "in 7 Step", "Senza Sprecare 12 Mesi"]

mechanisms = [
    "Metodo da Garage",
    "Sistema Progressivo",
    "Strategia Budget Zero",
    "Tecnica Restauro Essenziale",
    "Approccio Meccanico Guidato"
]

def seo_score(keyword):
    score = 40
    words = len(keyword.split())

    if words >= 4:
        score += 20
    elif words == 3:
        score += 10

    if any(char.isdigit() for char in keyword):
        score += 15

    if "guida" in keyword.lower():
        score += 10

    if "per" in keyword.lower():
        score += 5

    return min(score, 100)

def keyword_type(keyword):
    if "come" in keyword.lower():
        return "Informazionale"
    if any(char.isdigit() for char in keyword):
        return "Nicchia Specifica"
    if len(keyword.split()) >= 4:
        return "Long Tail Mirata"
    return "Generica Competitiva"

@app.route('/')
def home():
    return "KDP PRO Bot Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP PRO ENGINE ATTIVO\n\n"
        "/keyword parola\n"
        "/titolo argomento"
    )

@bot.message_handler(commands=['keyword'])
def keyword(message):
    kw = message.text.replace("/keyword", "").strip()

    if not kw:
        bot.reply_to(message, "Inserisci una keyword.")
        return

    score = seo_score(kw)
    ktype = keyword_type(kw)

    angles = [
        "Versione Budget Ridotto",
        "Guida per Principianti Assoluti",
        "Approccio Professionale",
        "Metodo Ultra Specifico Modello/Anno",
        "Restauro Fai-da-Te Domestico"
    ]

    response = f"""
🔎 ANALISI STRATEGICA KDP

📌 Keyword: {kw}
🎯 Tipo: {ktype}
📊 SEO Score: {score}/100

🎯 Angolo Consigliato:
{random.choice(angles)}

💡 Long Tail Strategiche:
- {kw} guida pratica completa
- come {kw} senza errori
- {kw} per principianti passo dopo passo
"""

    bot.reply_to(message, response)

@bot.message_handler(commands=['titolo'])
def titolo(message):
    topic = message.text.replace("/titolo", "").strip()

    if not topic:
        bot.reply_to(message, "Inserisci un argomento.")
        return

    normal_titles = []
    for _ in range(2):
        title = f"{topic.title()} - {random.choice(power_words)}"
        subtitle = f"{random.choice(mechanisms)} {random.choice(time_frames)}"
        normal_titles.append(f"📘 {title}\n {subtitle}")

    aggressive = f"🔥 {topic.title()} – {random.choice(mechanisms)} {random.choice(time_frames)} Anche se Parti da Zero"

    ultra_niche = f"🎯 {topic.title()} per Principianti Assoluti – Manuale Pratico da Garage con Budget Ridotto"

    response = "🏆 KDP PRO TITOLI\n\n"
    response += "\n\n".join(normal_titles)
    response += "\n\n"
    response += aggressive
    response += "\n\n"
    response += ultra_niche

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
