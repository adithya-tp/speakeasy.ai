import speech_recognition as sr
import wave

def recognize_speech_and_save_audio():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Please speak now...")
        audio = recognizer.listen(source)

    print(audio.sample_width)
    # Save the captured audio to a .wav file
    with wave.open("captured_audio.wav", "wb") as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(audio.sample_width)
        wave_file.setframerate(audio.sample_rate)
        wave_file.writeframes(audio.get_raw_data())


if __name__ == '__main__':
    recognize_speech_and_save_audio()