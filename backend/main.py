from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'database/fomo_health.db'

@app.route("/voice", methods=['POST'])
def voice_menu():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/handle-input', method='POST')
    gather.say("Bienvenue chez Fomo-Health. "
        "Pour connaitre nos heures d'ouverture, tapez 1. "
        "Pour connaitre l'horaire d'un médecin, tapez 2. "
        "Pour prendre un rendez-vous, tapez 3. "
        "Sinon, restez en ligne pour toute autre question.",
        language='fr-FR')
    response.append(gather)
    response.redirect('/voice')
    return Response(str(response), mimetype="text/xml")

@app.route("/handle-input", methods=['POST'])
def handle_input():
    response = VoiceResponse()
    choice = request.form.get('Digits', 'timeout')
    
    if choice == '1':
        # LIT DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute('SELECT hours FROM clinic_info WHERE id=1')
        clinic = cursor.fetchone()
        conn.close()
        
        if clinic:
            msg = clinic[0]
        else:
            msg = "Infos non disponibles."
        
        gather = Gather(num_digits=1, action='/handle-input', method='POST')
        gather.say(msg + " Autre chose? 1 menu.", language='fr-FR')
        response.append(gather)
    
    elif choice == '2':
        response.say("RDV: Appelez reception au 418-XXX-XXXX.", language='fr-FR')
        response.redirect('/voice')
    
    elif choice == '0':
        response.say("Merci, au revoir!", language='fr-FR')
        response.hangup()
    
    else:
        response.say("Choix invalide.", language='fr-FR')
        response.redirect('/voice')
    
    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
