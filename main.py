from flask import Flask, request
import telebot
import os
import random

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ---------- MOTORE ANALISI ----------

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

# ---------- GENERATORE TITOLI STRATEGICI ----------

power_angles = [
    "Guida Tecnica Completa",
    "Manuale Pratico",
    "Metodo Definitivo",
    "Approccio Professionale",
    "Sistema Step-by-Step"
]

promises = [
    "Senza Errori Costosi",
    "Con Budget Ridotto",
    "Anche se Parti da Zero",
    "Dalla A alla Z",
    "Con Risultati Concreti"
]

def generate_strategic_titles(keyword):
    base = keyword.title()
    titles = []

    for _ in range(5):
        angle = random.choice(power_angles)
        promise = random.choice(promises)
        titles.append(f"📘 {base} – {angle}: {promise}")

    return titles

# ---------- SIMULAZIONE TITOLI AMAZON ----------

amazon_patterns = [
    "Guida Completa",
    "Manuale Illustrato",
    "Edizione Aggiornata 2024",
    "Versione Estesa",
    "Guida per Principianti"
]

def generate_amazon_style_titles(keyword):
    base = keyword.title()
    titles = []

    for pattern in amazon_patterns:
        titles.append(f"🛒 {base} – {pattern}")

    return titles

# ---------- FLASK ROUTING ----------

@app.route('/')
def home():
    return "KDP Strategist V6 Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# ---------- COMANDO START ----------

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP STRATEGIST V6\n\n"
        "Scrivi:\n"
        "/analyze tua keyword"
    )

# ---------- COMANDO ANALYZE ----------

@bot.message_handler(commands=['analyze'])
def analyze(message):
    kw = message.text.replace("/analyze", "").strip()

    if not kw:
        bot.reply_to(message, "Inserisci una keyword dopo /analyze")
        return

    score = seo_score(kw)
    words = len(kw.split())
    profile = market_profile(score, words)

    strategic_titles = generate_strategic_titles(kw)
    amazon_titles = generate_amazon_style_titles(kw)

    response = f"""
🧠 ANALISI STRATEGICA

📌 Keyword: {kw}
📊 SEO Score: {score}/100
🎯 Profilo Mercato: {profile}

🏆 5 TITOLI STRATEGICI DIFFERENZIANTI:

{strategic_titles[0]}
{strategic_titles[1]}
{strategic_titles[2]}
{strategic_titles[3]}
{strategic_titles[4]}

🛒 TITOLI IN STILE AMAZON (attualmente comuni sul mercato):

{amazon_titles[0]}
{amazon_titles[1]}
{amazon_titles[2]}
{amazon_titles[3]}
{amazon_titles[4]}
"""

    bot.reply_to(message, response)

# ---------- AVVIO ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
