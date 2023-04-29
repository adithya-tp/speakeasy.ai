import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather


class SpeakieBot():
    def __init__(self):
        account_sid = os.environ['TWILIO_SID']
        auth_token = os.environ['TWILIO_AUTH']
        # Create a Twilio client object, and response object
        self.client = Client(account_sid, auth_token)
        self.response = VoiceResponse()

        # Track recording count for unique filenames
        self.recording_count = 0
        # Bot phone number
        self.phone_number = os.environ['TWILIO_NUMBER']
    
    def call(self, to):
        """
            Construct and return 'call' instance
        """
        call = self.client.calls.create(
            url="https://8069-2601-547-b04-4993-908a-97bc-3ad0-2df1.ngrok.io/speakeasy/make_reservation",
            from_=self.phone_number,
            to=to,
        )
        return call
