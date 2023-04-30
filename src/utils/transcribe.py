import os
import requests
import time
from pywhispercpp.model import Model


class Transcriber():
    def __init__(self):
        self.model = Model('small.en', print_progress=False)

    def get_transcription(self, recording_url):
        time.sleep(2)
        # Download the audio file from the recording URL
        response = requests.get(f"{recording_url}.wav")
        audio_data = response.content

        # Save the audio file temporarily (for transcribing)
        temp_file_path = "generated_audios/temp_audio.wav"
        with open(temp_file_path, "wb") as audio_file:
            audio_file.write(audio_data)

        # Transcribe the audio file using a OpenAI's whisper api
        segments = self.model.transcribe(temp_file_path, new_segment_callback=print)
        transcript = " ".join(segment.text for segment in segments)

        # Delete the temporary audio file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Return the transcription
        return transcript
