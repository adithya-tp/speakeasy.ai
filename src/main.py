from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from twilio.twiml.voice_response import VoiceResponse


from utils import speak


app = FastAPI()
# mount the static files directory
app.mount("/static", StaticFiles(directory="generated_audios"), name="static")
bot = speak.SpeakieBot()

@app.on_event("startup")
async def make_call():
    bot.call(to="+14122142142")


@app.post("/speakeasy/make_reservation")
async def twilio_webhook():
    # Update the call's TwiML to play the new audio file using the <Play> verb
    bot.respond("test_audio.wav")
