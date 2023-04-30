import os
import io
from elevenlabs import generate, set_api_key
from pydub import AudioSegment

class Text2Audio:
    def __init__(self):
        ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        set_api_key(ELEVENLABS_API_KEY)

    def save_audio_path(self, text, filename="audio.wav"):
        path = 'generated_audios/' + filename
        audio_bytes = generate(text)
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        audio.export(path, format="wav")
        return filename