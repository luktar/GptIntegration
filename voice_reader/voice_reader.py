import io
from time import sleep
import speech_recognition as sr
from openai import OpenAI


class VoiceReader:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.r = sr.Recognizer()
        self.transcriptions = []

    def callback(self, recognizer, audio):
        try:
            # read the audio data from the default microphone
            wav_data = audio.get_wav_data()
            buffer = io.BytesIO(wav_data)
            buffer.name = "recording.wav"
            print("Recognizing...")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=buffer,
                response_format="text"
            )
            self.transcriptions.append(transcription)
        except sr.UnknownValueError:
            print("Whisper Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Whisper Recognition service; {0}".format(e))

    def record_voice(self):
        with sr.Microphone() as source:
            print("Calibrating...")
            self.r.adjust_for_ambient_noise(source, 1)
        print("Listening...")
        stop_listening = self.r.listen_in_background(source, self.callback)

        # stop_listening(wait_for_stop=True)
        listen = True
        while listen:
            if len(self.get_transcriptions()) > 0:
                print(self.get_transcriptions())
                if 'stop' in self.get_transcriptions()[-1].lower():
                    stop_listening(wait_for_stop=True)
                    listen = False
            sleep(0.1)

    def get_transcriptions(self):
        # after calling record_voice, use this to get transcriptions
        return self.transcriptions
