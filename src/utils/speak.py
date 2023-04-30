import os
from fastapi import Response
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse


class SpeakieBot():
    def __init__(self):
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_AUTH']
        # Create a Twilio client object, and response object
        self.client = Client(account_sid, auth_token)

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

    def initiate_convo(self, audio_file_path):
        response = VoiceResponse()
        response.play(f"{self.base_url}/static/{audio_file_path}")
        response.record(
            action="/speakeasy/process_audio", timeout=3, transcribe=False
        )

        return Response(content=response.to_xml(), media_type="application/xml")
