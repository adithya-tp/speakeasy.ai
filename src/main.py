import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from utils import speak, transcribe, think, think_voiceflow


app = FastAPI()
# mount the static files directory
app.mount("/static", StaticFiles(directory="generated_audios"), name="static")
bot: speak.SpeakieBot = None
transcriber: transcribe.Transcriber = None
# thinker: think.Thinker = None
thinker: think_voiceflow.Thinker = None


@app.on_event("startup")
async def make_reservation():
    global bot, transcriber, thinker

    # Initialize bot, transcriber, thinker, synthesizer
    bot = speak.SpeakieBot()
    transcriber = transcribe.Transcriber()
    user_request = "Book a reservation for 4 people at 2:30pm today."
    thinker = think.Thinker(user_request)
    thinker.reply("Hello")
    # thinker = think_voiceflow.Thinker(user_request)

    # Make call 
    bot.call(to=os.environ['TWILIO_TO'])


@app.post("/speakeasy/converse")
async def start_talking():
    # Update the call's TwiML to play the new audio file using the <Play> verb
    # return bot.talk(thinker.get_reply())
    return bot.talk(thinker._last_msg())


@app.post("/speakeasy/process_audio")
async def converse(request: Request):
    if thinker._talked and thinker._is_done():
        print("Ending conversation!!")
        msg = "Thank you, bye bye!"
        bot.send_confirmation()
        return bot.talk(msg, end_convo=True)

    print("Continuing Conversation!!")
    form_data = await request.form()
    recording_url = form_data['RecordingUrl']
    transcript = transcriber.get_transcription(recording_url)

    thinker.reply(transcript)
    return bot.talk(thinker._last_msg())


@app.post("/speakeasy/process_audio_flow")
async def converse(request: Request):
    if thinker.is_done:
        print("Ending conversation!!")
        msg = "Thank you so much, bye bye!"
        return bot.talk(msg, end_convo=True)
    
    print("Continuing Conversation!!")
    form_data = await request.form()
    recording_url = form_data['RecordingUrl']
    transcript = transcriber.get_transcription(recording_url)

    thinker.update_receptionist_reply(transcript)
    new_reply = thinker.get_reply()
    return bot.talk(new_reply)
