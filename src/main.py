import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from utils import speak, transcribe, think, text2audio


app = FastAPI()
# mount the static files directory
app.mount("/static", StaticFiles(directory="generated_audios"), name="static")
bot: speak.SpeakieBot = None
transcriber: transcribe.Transcriber = None
thinker: think.Thinker = None


@app.on_event("startup")
async def make_reservation():
    global bot, transcriber, thinker

    # Initialize bot, transcriber, thinker, synthesizer
    bot = speak.SpeakieBot()
    transcriber = transcribe.Transcriber()
    user_request = "Book a reservation for 2 people at 5:30pm today."
    thinker = think.Thinker(user_request)
    thinker.reply("Hello")

    # Make call 
    bot.call(to=os.environ['TWILIO_TO'])


@app.post("/speakeasy/converse")
async def start_talking():
    # Update the call's TwiML to play the new audio file using the <Play> verb
    return bot.talk(thinker._last_msg())


@app.post("/speakeasy/process_audio")
async def converse(request: Request):
    if thinker._talked and thinker._is_done():
        print("Ending conversation!!")
        msg = "Thank you, bye bye!"
        return bot.talk(msg, end_convo=True)

    form_data = await request.form()
    recording_url = form_data['RecordingUrl']
    transcript = transcriber.get_transcription(recording_url)

    thinker.reply(transcript)
    return bot.talk(thinker._last_msg())
