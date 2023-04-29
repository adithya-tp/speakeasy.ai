import os
from twilio.rest import Client


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
            url=f"{self.base_url}/speakeasy/make_reservation",
            from_=self.phone_number,
            to=to,
        )
        self.call_sid = call.sid

    def respond(self,audio_file_path):
        assert self.call_sid is not None

        twiml_string = \
        f"""
            <Response>
                <Play>
                    {self.base_url}/static/{audio_file_path}
                </Play>
            </Response>
        """
        self.client.calls(self.call_sid).update(
            twiml=twiml_string
        )

