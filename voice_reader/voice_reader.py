import io
from time import sleep
import speech_recognition as sr
from openai import OpenAI


class VoiceReader:
    def __init__(self) -> None:
        self.client = OpenAI()
        self.r = sr.Recognizer()
        self.transcriptions = []
        self.latest_transcription = ""

    def record_voice(self):
        with sr.Microphone() as source:
            print("Kalibrowanie mikrofonu...")
            self.r.adjust_for_ambient_noise(source, 1)
            first_threshold = self.r.energy_threshold
            self.r.adjust_for_ambient_noise(source, 1)
            second_threshold = self.r.energy_threshold
            # selects the higher of two thresholds, if necessary we can multiply it to achieve less noise pickup
            final_threshold = first_threshold if first_threshold > second_threshold else second_threshold
            final_threshold *= 1.1
            self.r.energy_threshold = final_threshold
            
            print("Nasłuchiwanie...")
            audio_data = self.r.listen(source, timeout=20, phrase_time_limit=8)
            self.callback(self.r, audio_data)
            return self.latest_transcription

    def callback(self, recognizer, audio):
        try:
            # read the audio data from the default microphone
            wav_data = audio.get_wav_data()
            buffer = io.BytesIO(wav_data)
            buffer.name = "recording.wav"
            print("Analizowanie...")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=buffer,
                response_format="text"
            )
            self.transcriptions.append(transcription)
            self.latest_transcription = transcription
        except sr.UnknownValueError:
            print("Whisper Recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from Whisper Recognition service; {0}".format(e))

    def record_voice_background(self):
        with sr.Microphone() as source:
            print("Calibrating...")
            self.r.adjust_for_ambient_noise(source, 1)
        print("Listening...")
        stop_listening = self.r.listen_in_background(source, self.callback)

        # stop_listening(wait_for_stop=True)
        listen = True
        while listen:
            if len(self.transcriptions) > 0:
                print(self.transcriptions)
                if 'stop' in self.transcriptions[-1].lower():
                    stop_listening(wait_for_stop=True)
                    listen = False
            sleep(0.1)
