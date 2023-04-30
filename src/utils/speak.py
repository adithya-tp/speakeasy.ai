import os
from utils.text2audio import Text2Audio
from fastapi import Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


class SpeakieBot():
    def __init__(self):
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_AUTH']
        # Create a Twilio client object, and response object
        self.client = Client(account_sid, auth_token)
        self.synthesizer = Text2Audio()

        # Track recording count for unique filenames
        self.recording_count = 0
        # Bot phone number
        self.phone_number = os.environ['TWILIO_NUMBER']
        # Base URL
        self.base_url = "http://34.227.31.202:8000"
        self.call_sid = None
    
    def call(self, to):
        """
            Construct and return 'call' instance
        """
        call = self.client.calls.create(
            url=f"{self.base_url}/speakeasy/converse",
            from_=self.phone_number,
            to=to,
        )
        self.call_sid = call.sid

    def talk(self, text, end_convo=False):
        audio_file_path = self.synthesizer.save_audio_path(text)
        audio_file = f"{self.base_url}/static/{audio_file_path}"
        response = VoiceResponse()
        response.play(audio_file)
        if not end_convo:
            response.record(
                action="/speakeasy/process_audio", timeout=3, transcribe=False
            )

        return Response(content=response.to_xml(), media_type="application/xml")
    
    def send_confirmation(self):
        self.client.messages.create(
            body="I've successfully made your reservation John!",
            from_=self.phone_number,
            to=os.environ['TWILIO_TO']
        )