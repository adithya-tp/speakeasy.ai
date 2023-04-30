from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from utils import speak, transcribe, think


app = FastAPI()
# mount the static files directory
app.mount("/static", StaticFiles(directory="generated_audios"), name="static")
bot: speak.SpeakieBot = None
transcriber: transcribe.Transcriber = None
thinker: think.Thinker = None


@app.on_event("startup")
async def make_reservation():
    global bot, transcriber, thinker
    bot = speak.SpeakieBot()
    transcriber = transcribe.Transcriber()
    user_request = "Book a reservation for 2 people at 5:30pm today."
    thinker = think.Thinker(user_request)
    thinker.reply("Hello")
    bot.call(to="+14122142142")


@app.post("/speakeasy/converse")
async def converse():
    # Update the call's TwiML to play the new audio file using the <Play> verb
    return bot.initiate_convo("test_audio.wav")


@app.post("/speakeasy/process_audio")
async def process_recipient_audio(request: Request):
    form_data = await request.form()
    recording_url = form_data['RecordingUrl']
    transcript = transcriber.get_transcription(recording_url)
    print("Transcription")
    response_text = thinker.reply(transcript)
    print(response_text)
