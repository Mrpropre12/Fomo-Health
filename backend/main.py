from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'database/fomo_health.db'

#Méthode post pour présenter le menu
@app.route("/voice", methods=['POST'])
def voice_menu():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/handle-input', method='POST')
    gather.say("Bienvenue chez Fomo-Health. "
        "Pour connaitre nos heures d'ouverture, tapez 1. "
        "Pour prendre un rendez-vous, tapez 2. "
        "Pour connaitre l'horaire d'un médecin, tapez 3. "
        "Sinon, restez en ligne pour toute autre question.",
        language='fr-FR')
    response.append(gather)
    response.redirect('/voice')
    return Response(str(response), mimetype="text/xml")

#Gestion de la réponse choix de l'utilisateur pour les options du menu
@app.route("/handle-input", methods=['POST'])
def handle_input():
    response = VoiceResponse()
    choice = request.form.get('Digits', 'timeout')
    
    if choice == '1':
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute('SELECT hours FROM clinic_info WHERE id=1')
        clinic = cursor.fetchone()
        conn.close()

        msg = clinic[0] if clinic else "Infos non disponibles."
        
        gather = Gather(input='speech', action='/process-query', language='fr-FR', speech_timeout='auto')
        gather.say(msg + " Souhaitez-vous autre chose ? Je vous écoute.", language='fr-FR')
        response.append(gather)
    
    elif choice == '2':
        # Ajoute une logique pour les médecins ou redirige
        response.say("Cette fonctionnalité sera bientôt disponible.", language='fr-FR')
        response.redirect('/voice')
        
    else:
        # Gestion du timeout ou des mauvais choix
        response.say("Je n'ai pas reçu de sélection valide.", language='fr-FR')
        response.redirect('/voice')

    return str(response)

#Cette route permet à l'agent de pas haluciner
#et de répondre uniquement avec des informations issu de la base de donnée
@app.route("/process-query", methods=['POST'])
def process_query():
    response = VoiceResponse()
    # Récupération de ce que le client a dit
    user_speech = request.form.get('SpeechResult', '').lower()
    
    if not user_speech:
        response.say("Je n'ai pas bien entendu. Pouvez-vous répéter ?", language='fr-FR')
        response.redirect('/handle-input') # Renvoie au menu ou à l'écoute
        return str(response)

    # Connexion à la base de données
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
   # Recherche un mot-clé de la DB est présent dans la phrase
    cursor.execute("SELECT info_content FROM clinic_services WHERE ? LIKE '%' || keyword_trigger || '%'", (user_speech,))
    result = cursor.fetchone()
    conn.close()

    if result:
        # Si on trouve l'info dans la DB
        reply = result[0]
        response.say(reply + " Souhaitez-vous autre chose ?", language='fr-FR')
        # On relance l'écoute pour permettre une autre question
        gather = Gather(input='speech', action='/process-query', language='fr-FR')
        response.append(gather)
    else:
        # PROTECTION ANTI-HALLUCINATION
        # On crée un nouveau Gather pour capturer le choix 1 ou 2
        gather = Gather(num_digits=1, action='/handle-fallback-choice', method='POST')
        gather.say("Je suis désolé, je n'ai pas cette information dans mes dossiers. "
                   "Pour revenir au menu principal, tapez 1. "
                   "Pour parler à un agent, tapez 2.", language='fr-FR')
        response.append(gather)
        # Si l'utilisateur ne tape rien, on le renvoie au menu principal par défaut
        response.redirect('/voice')
        
    return str(response)
    
   
        
#Cette route permet de diriger l'utilisateur vers la bonne destination saisie
@app.route("/handle-fallback-choice", methods=['POST'])
def handle_fallback_choice():
    response = VoiceResponse()
    choice = request.form.get('Digits')

    if choice == '1':
        # Retour au menu de départ
        response.redirect('/voice')
    elif choice == '2':
        target_number = "+1XXXXXXXXXX"

        response.say("Très bien, je vous transfère à un conseiller. Veuillez patienter.", language='fr-FR')
        # La balise Dial connecte l'appelant actuel au numéro cible
        response.dial(target_number)
    else:
        response.say("Choix non reconnu. Retour au menu principal.", language='fr-FR')
        response.redirect('/voice')

    return str(response)
if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
