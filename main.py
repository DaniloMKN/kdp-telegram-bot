from flask import Flask, request
import telebot
import os
import random

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# -------- ANALISI BASE --------

def seo_score(keyword):
    score = 40
    words = len(keyword.split())

    if words >= 4:
        score += 20
    if any(char.isdigit() for char in keyword):
        score += 15

    return min(score, 100)

# -------- STRUTTURE --------

methods = ["Metodo Garage 60 Giorni", "Sistema Ripristino Professionale", "Strategia Restauro Essenziale"]
targets = ["per Principianti Assoluti", "per Appassionati Fai-da-Te", "per Restauratori Indipendenti"]
benefits = ["Senza Errori Costosi", "Con Budget Controllato", "Passo Dopo Passo", "Dalla A alla Z"]

transformations = [
    "Da Auto Ferma a Modello Restaurato Perfetto",
    "Dal Garage alla Strada in Perfette Condizioni",
    "Dal Progetto al Ripristino Professionale"
]

# -------- GENERAZIONE COMBO --------

def generate_combos(keyword):
    base = keyword.title()
    combos = []

    # 1 Metodo + Beneficio
    combos.append({
        "title": f"{base} – {random.choice(methods)}",
        "subtitle": f"Guida Completa {random.choice(benefits)} per un Ripristino Affidabile",
        "angle": "Metodo Proprietario",
        "target": "Appassionati tecnici",
        "psychology": "Sicurezza e controllo"
    })

    # 2 Target specifico
    combos.append({
        "title": f"{base} {random.choice(targets)}",
        "subtitle": f"Manuale Pratico {random.choice(benefits)} per Restaurare in Autonomia",
        "angle": "Accessibilità",
        "target": "Principianti",
        "psychology": "Riduzione paura"
    })

    # 3 Budget
    combos.append({
        "title": f"{base} – Restauro con Budget Ridotto",
        "subtitle": f"Tecniche Concrete {random.choice(benefits)} Senza Compromettere la Qualità",
        "angle": "Risparmio intelligente",
        "target": "Hobbisti attenti ai costi",
        "psychology": "Evitare sprechi"
    })

    # 4 Trasformazione
    combos.append({
        "title": f"{base} – {random.choice(transformations)}",
        "subtitle": f"Strategie Tecniche e Operative per un Risultato Professionale",
        "angle": "Trasformazione visibile",
        "target": "Motivati al risultato",
        "psychology": "Visione finale"
    })

    # 5 Autorità Tecnica
    combos.append({
        "title": f"{base} – Manuale Tecnico Completo",
        "subtitle": f"Procedure, Errori Comuni e Soluzioni Pratiche {random.choice(benefits)}",
        "angle": "Autorità professionale",
        "target": "Esperti e semi-esperti",
        "psychology": "Competenza"
    })

    return combos

# -------- ROUTING --------

@app.route('/')
def home():
    return "KDP Strategist V8 Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🚀 KDP STRATEGIST V8\n\n"
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
    combos = generate_combos(kw)

    response = f"🧠 ANALISI + COMBINAZIONI COMPLETE\n\n"
    response += f"📌 Keyword: {kw}\n"
    response += f"📊 SEO Score: {score}/100\n\n"
    response += "🏆 5 PROPOSTE COMPLETE:\n\n"

    for i, combo in enumerate(combos, start=1):
        response += f"🔹 PROPOSTA {i}\n"
        response += f"📘 Titolo:\n{combo['title']}\n\n"
        response += f"📝 Sottotitolo:\n{combo['subtitle']}\n\n"
        response += f"🎯 Posizionamento:\n{combo['angle']}\n"
        response += f"👥 Target:\n{combo['target']}\n"
        response += f"🧠 Leva Psicologica:\n{combo['psychology']}\n\n"
        response += "-----------------------------\n\n"

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
