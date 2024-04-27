import io
import speech_recognition as sr
from openai import OpenAI


class VoiceReader:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.r = sr.Recognizer()

    def record_voice(self):
        with sr.Microphone() as source:
            print("Calibrating...")
            self.r.adjust_for_ambient_noise(source)
            print("Listening...")
            # read the audio data from the default microphone
            audio_data = self.r.listen(source, 4)
            wav_data = audio_data.get_wav_data()
            buffer = io.BytesIO(wav_data)
            buffer.name = "recording.wav"
            print("Recognizing...")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=buffer,
                response_format="text"
            )
            print(transcription)
            return transcription
