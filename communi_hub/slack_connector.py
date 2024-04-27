import sys
import logging
from slack_sdk import WebClient

class SlackConnector:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        client = WebClient()

    def send_message(self, message, receiver_name, receiver_surname) -> bool:
        return 'Slack message sent: ' + message + " receiver_name: " + receiver_name + " receiver_surname: " + receiver_surname
