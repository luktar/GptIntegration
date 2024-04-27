import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackConnector:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG)
        self.client = WebClient(token=os.environ['SLACK_API_KEY'])

    def send_message(self, message) -> bool:
        try:
            response = self.client.chat_postMessage(
                channel='#general',
                text=message)
            return 'Sent from slack' + response["message"]["text"]
        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
            return "Unable to send a message on slack"
