from fastapi import FastAPI, Response, Form
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.services.ai_service import ask_fomo_ai
from app.services.sms_service import send_confirmation_sms
from app.core.config import settings
import sqlite3

app = FastAPI()

# Ce dictionnaire de headers sera réutilisé partout pour bloquer la sécurité ngrok
NGROK_HEADERS = {"ngrok-skip-browser-warning": "true"}

@app.post("/voice")
async def voice_menu():
    resp = VoiceResponse()
    gather = Gather(num_digits=1, action='/menu-selection')
    gather.say(
        "Bienvenue chez Fomo-Health. "
        "Pour connaitre nos heures d'ouverture, tapez 1. "
        "Pour connaitre l'horaire d'un médecin, tapez 2. "
        "Pour prendre un rendez-vous, tapez 3. "
        "Sinon, restez en ligne pour toute autre question.",
        language='fr-FR'
    )
    resp.append(gather)
    resp.redirect('/voice-ai-default') 
    return Response(content=str(resp), media_type="application/xml", headers=NGROK_HEADERS)