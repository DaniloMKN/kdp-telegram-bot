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
    "Strategico", "Semplice", "Professionale",
    "Illustrato", "Passo dopo Passo", "Aggiornato"
]

promises = [
    "Anche se Parti da Zero",
    "Senza Sprecare Tempo",
    "Con Budget Ridotto",
    "Senza Errori Costosi",
    "Metodo Testato",
    "Guida per Principianti",
    "Dalla A alla Z"
]

psychology_hooks = [
    "Scopri il Metodo",
    "Impara le Tecniche",
    "Evita gli Errori",
    "Ottieni Risultati",
    "Trasforma la Tua Passione",
    "Raggiungi un Livello Superiore"
]

def detect_intent(keyword):
    if "come" in keyword.lower():
        return "Informazionale"
    if any(char.isdigit() for char in keyword):
        return "Nicchia Specifica"
    if len(keyword.split()) >= 4:
        return "Long Tail Mirata"
    return "Generica / Competitiva"

def difficulty_estimation(keyword):
    words = len(keyword.split())
    if words >= 4:
        return "Bassa"
    if words == 3:
        return "Media"
    return "Alta"

@app.route('/')
def home():
    return "KDP Bot Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 KDP Intelligence Bot Attivo\n\n/keyword parola\n/titolo argomento")

@bot.message_handler(commands=['keyword'])
def keyword(message):
    keyword = message.text.replace("/keyword", "").strip()
    if not keyword:
        bot.reply_to(message, "Inserisci una keyword.")
        return

    intent = detect_intent(keyword)
    difficulty = difficulty_estimation(keyword)

    angles = [
        "Guida per principianti",
        "Metodo con budget ridotto",
        "Approccio passo passo",
        "Strategia professionale",
        "Versione aggiornata"
    ]

    response = f"""
🔎 ANALISI KEYWORD

📌 Keyword: {keyword}
🎯 Intento: {intent}
📉 Competitività Stimata: {difficulty}

💡 Angoli di Mercato:
- {random.choice(angles)}
- {random.choice(angles)}
- {random.choice(angles)}
"""
    bot.reply_to(message, response)

@bot.message_handler(commands=['titolo'])
def titolo(message):
    topic = message.text.replace("/titolo", "").strip()
    if not topic:
        bot.reply_to(message, "Inserisci un argomento.")
        return

    results = []
    for _ in range(3):
        title = f"{topic.title()} - {random.choice(power_words)}"
        subtitle = f"{random.choice(psychology_hooks)} {random.choice(promises)}"
        results.append(f"📘 {title}\n {subtitle}")

    response = "🏆 IDEE TITOLO & SOTTOTITOLO\n\n" + "\n\n".join(results)

    bot.reply_to(message, response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
