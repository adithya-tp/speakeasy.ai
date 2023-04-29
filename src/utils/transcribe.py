import os
import openai
import requests

def get_transcription(recording_url):
    # # Download the audio file from the recording URL
    response = requests.get(recording_url)
    audio_data = response.content

    # Save the audio file temporarily (for transcribing)
    temp_file_path = "../generated_audios/temp_audio.wav"
    with open(temp_file_path, "wb") as audio_file:
        audio_file.write(audio_data)

    # Transcribe the audio file using a OpenAI's whisper api
    audio = open(temp_file_path, "rb")
    transcription = openai.Audio.transcribe(
        "whisper-1",
        audio,
        prompt="Hello, how may I help you?"
    )

    # Delete the temporary audio file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    # Return the transcription
    return transcription["text"]
