from flask import Flask, request
import telebot
import os

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

def generate_structured_titles(keyword):
    base = keyword.title()

    titles = []

    # 1. Autorità Tecnica
    titles.append(
        f"📘 {base} – Manuale Tecnico Completo per Restauratori Fai-da-Te"
    )

    # 2. Metodo Proprietario
    titles.append(
        f"📘 {base} – Il Metodo Garage 60 Giorni per un Ripristino Professionale"
    )

    # 3. Target Specifico
    titles.append(
        f"📘 {base} per Principianti Assoluti – Guida Passo Dopo Passo Senza Errori"
    )

    # 4. Problema/Budget
    titles.append(
        f"📘 {base} – Restauro con Budget Ridotto Senza Compromettere la Qualità"
    )

    # 5. Trasformazione Finale
    titles.append(
        f"📘 {base} – Da Auto Ferma a Gioiello Restaurato: Tecniche e Strategie"
    )

    return titles

def generate_amazon_style_titles(keyword):
    base = keyword.title()

    return [
        f"🛒 {base} – Guida Completa",
        f"🛒 {base} – Manuale Illustrato",
        f"🛒 {base} – Edizione Aggiornata",
        f"🛒 {base} – Versione Estesa",
        f"🛒 {base} – Guida per Principianti"
    ]

@app.route('/')
def home():
    return "KDP Strategist V7 Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP STRATEGIST V7\n\n"
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

    strategic_titles = generate_structured_titles(kw)
    amazon_titles = generate_amazon_style_titles(kw)

    response = f"""
🧠 ANALISI STRATEGICA

📌 Keyword: {kw}
📊 SEO Score: {score}/100
🎯 Profilo Mercato: {profile}

🏆 5 TITOLI STRUTTURATI DIFFERENZIATI:

{strategic_titles[0]}

{strategic_titles[1]}

{strategic_titles[2]}

{strategic_titles[3]}

{strategic_titles[4]}

🛒 TITOLI IN STILE AMAZON:

{amazon_titles[0]}
{amazon_titles[1]}
{amazon_titles[2]}
{amazon_titles[3]}
{amazon_titles[4]}
"""

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
