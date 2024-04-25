from communi_hub.calendar_connector import CalendarConnector
from communi_hub.mail_connector import MailConnector
from communi_hub.slack_connector import SlackConnector

from voice_generator.voice_generator import VoiceGenerator
from voice_reader.voice_reader import VoiceReader

import config



def main():
    # Tutaj umieść główną logikę swojego programu
    print("Hello World!")
    configuration = config.load_config("config.json")
    print(configuration.openai_apikey)

if __name__ == "__main__":
    main()