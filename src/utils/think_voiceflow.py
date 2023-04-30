import os
import json
import time
import requests

class Thinker:
    def __init__(self, user_reservation_transcript):
        self.checkin_msg = "Is your conversation done?"
        self._talked = False
        self.user_id = int(time.time())
        self.api_key = os.environ['VOICEFLOW_API_KEY']
        self.is_done = False
        self._set_request(user_reservation_transcript)

    def _set_request(self, msg):
        url = "https://general-runtime.voiceflow.com/state/user/{userID}/variables"
        headers = {
            "Content-Type": "application/json",
            "versionID": "development",
            "Authorization": self.api_key
        }
        payload = {
            "user_reservation_transcript": msg,
        }

        status = requests.post(
            url.format(userID=self.user_id), 
            headers=headers, data=json.dumps(payload)
        )
        print("Update status: ", status)
    
    def get_reply(self):
        response = requests.post(
            f'https://general-runtime.voiceflow.com/state/user/{self.user_id}/interact',
            headers={ 'Authorization': self.api_key },
        )
        print(response.json())
        # Add logic to check if done (based on reply)
        return response.json()[0]['payload']['message']

    def update_receptionist_reply(self, receptionist_response):
        url = "https://general-runtime.voiceflow.com/state/user/{userID}/variables"
        headers = {
            "Content-Type": "application/json",
            "versionID": "development",
            "Authorization": self.api_key
        }
        payload = {
            "receptionist_response": receptionist_response,
        }

        requests.post(
            url.format(userID=self.user_id), 
            headers=headers, data=json.dumps(payload)
        )

