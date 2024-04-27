import logging
import time
import threading
import pyttsx3

class VoiceGenerator:
    def __init__(self) -> None:
        pass

    def generate_voice(self, text):
            print(text.strip())

            def play_speech():
                try:
                    engine = pyttsx3.init()
                    rate = engine.getProperty('rate')
                    engine.setProperty('rate', rate - 80) 
                    time.sleep(0.5)
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    logging.error(f"An error: {str(e)}")

            speech_thread = threading.Thread(target=play_speech)
            speech_thread.start()