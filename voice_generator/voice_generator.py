from pathlib import Path
from openai import OpenAI
from playsound import playsound


class VoiceGenerator:
    def __init__(self):
        self.client = OpenAI()

    def generate_voice(self, text):
        response = self.client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )

        response.stream_to_file("output.mp3")
        playsound('output.mp3')