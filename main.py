from flask import Flask, request
import telebot
import os
import random
from openpyxl import Workbook
from io import BytesIO

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ---------- ANALISI BASE ----------

def seo_score(keyword):
    score = 40
    words = len(keyword.split())

    if words >= 4:
        score += 20
    elif words == 3:
        score += 10

    if any(char.isdigit() for char in keyword):
        score += 15

    return min(score, 100)

def market_saturation(words):
    if words >= 4:
        return "Bassa"
    if words == 3:
        return "Media"
    return "Alta"

def demand_level(score):
    if score >= 75:
        return "Alta Verticale"
    if score >= 60:
        return "Media"
    return "Generica"

def price_suggestion(score):
    if score >= 75:
        return 17.99
    if score >= 60:
        return 14.99
    return 11.99

def monthly_sales_estimate(saturation):
    if saturation == "Bassa":
        return random.randint(60, 120)
    if saturation == "Media":
        return random.randint(40, 80)
    return random.randint(15, 40)

def decision_logic(score, saturation):
    if score >= 75 and saturation == "Bassa":
        return "GO"
    if score >= 60:
        return "CAUTION"
    return "NO"

# ---------- GENERATORE TITOLI ----------

methods = ["Metodo Garage 60 Giorni", "Sistema Ripristino Professionale", "Strategia Restauro Essenziale"]
benefits = ["Senza Errori Costosi", "Con Budget Controllato", "Passo Dopo Passo", "Dalla A alla Z"]
targets = ["per Principianti Assoluti", "per Appassionati Fai-da-Te", "per Restauratori Indipendenti"]
transformations = [
    "Da Auto Ferma a Modello Restaurato Perfetto",
    "Dal Garage alla Strada in Perfette Condizioni",
    "Dal Progetto al Ripristino Professionale"
]

def generate_combos(keyword):
    base = keyword.title()

    combos = []

    combos.append({
        "title": f"{base} – {random.choice(methods)}",
        "subtitle": f"Guida Completa {random.choice(benefits)} per un Ripristino Affidabile"
    })

    combos.append({
        "title": f"{base} {random.choice(targets)}",
        "subtitle": f"Manuale Pratico {random.choice(benefits)} per Restaurare in Autonomia"
    })

    combos.append({
        "title": f"{base} – Restauro con Budget Ridotto",
        "subtitle": f"Tecniche Concrete {random.choice(benefits)} Senza Compromettere la Qualità"
    })

    combos.append({
        "title": f"{base} – {random.choice(transformations)}",
        "subtitle": "Strategie Tecniche Operative per un Risultato Professionale"
    })

    combos.append({
        "title": f"{base} – Manuale Tecnico Completo",
        "subtitle": f"Procedure, Errori Comuni e Soluzioni Pratiche {random.choice(benefits)}"
    })

    return combos

# ---------- FLASK ----------

@app.route('/')
def home():
    return "KDP Ecosystem FULL Online"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🚀 KDP ECOSYSTEM FULL\n\n"
        "/analyze keyword → Titoli completi\n"
        "/business keyword → Simulazione profitto\n"
        "/export + keyword per riga → File Excel"
    )

# ---------- ANALYZE ----------

@bot.message_handler(commands=['analyze'])
def analyze(message):
    kw = message.text.replace("/analyze", "").strip()

    if not kw:
        bot.reply_to(message, "Inserisci una keyword dopo /analyze")
        return

    score = seo_score(kw)
    combos = generate_combos(kw)

    response = f"🧠 ANALISI EDITORIALE\n\n"
    response += f"📌 Keyword: {kw}\n"
    response += f"📊 SEO Score: {score}/100\n\n"

    for i, combo in enumerate(combos, start=1):
        response += f"🔹 PROPOSTA {i}\n"
        response += f"📘 {combo['title']}\n"
        response += f"📝 {combo['subtitle']}\n\n"

    bot.reply_to(message, response)

# ---------- BUSINESS ----------

@bot.message_handler(commands=['business'])
def business(message):
    kw = message.text.replace("/business", "").strip()

    if not kw:
        bot.reply_to(message, "Inserisci una keyword dopo /business")
        return

    score = seo_score(kw)
    words = len(kw.split())
    saturation = market_saturation(words)
    demand = demand_level(score)

    price = price_suggestion(score)
    monthly_sales = monthly_sales_estimate(saturation)
    royalty = round(price * 0.7, 2)
    monthly_profit = round(royalty * monthly_sales, 2)
    decision = decision_logic(score, saturation)

    response = f"""
📊 SIMULAZIONE BUSINESS

Keyword: {kw}
SEO: {score}/100
Domanda: {demand}
Saturazione: {saturation}

Prezzo: {price}€
Copie stimate: {monthly_sales}
Profitto stimato: {monthly_profit}€

Decisione: {decision}
"""
    bot.reply_to(message, response)

# ---------- EXPORT ----------

@bot.message_handler(commands=['export'])
def export_keywords(message):

    lines = message.text.split("\n")[1:]

    if not lines:
        bot.reply_to(message, "Dopo /export scrivi una keyword per riga.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "KDP Analysis"

    ws.append([
        "Keyword", "SEO Score", "Domanda",
        "Saturazione", "Prezzo",
        "Copie Stimate", "Profitto Stimato", "Decisione"
    ])

    for kw in lines:
        kw = kw.strip()
        if not kw:
            continue

        score = seo_score(kw)
        words = len(kw.split())
        saturation = market_saturation(words)
        demand = demand_level(score)
        price = price_suggestion(score)
        monthly_sales = monthly_sales_estimate(saturation)
        royalty = price * 0.7
        monthly_profit = round(royalty * monthly_sales, 2)
        decision = decision_logic(score, saturation)

        ws.append([
            kw, score, demand,
            saturation, price,
            monthly_sales, monthly_profit, decision
        ])

    file_stream = BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    bot.send_document(
        message.chat.id,
        file_stream,
        visible_file_name="kdp_keyword_analysis.xlsx"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
