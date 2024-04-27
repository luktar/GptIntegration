import speech_recognition as sr


class VoiceReader:
    def __init__(self) -> None:
        pass

    def record_voice(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            # read the audio data from the default microphone
            audio_data = r.listen(source, 4)
            print("Recognizing...")
            # convert speech to text
            text = r.recognize_whisper(audio_data, "small")
            print(text)