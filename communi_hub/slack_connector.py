from datetime import datetime
import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackConnector:
    def __init__(self) -> None:
        # logging.basicConfig(level=logging.DEBUG)
        self.client = WebClient(token=os.environ['SLACK_API_KEY'])
        self.channel = 'C070LCPMJH3'

    def send_message(self, message) -> bool:
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=message)
            return 'Sent from slack' + response["message"]["text"]
        except SlackApiError as e:
            print(f"Error: {e.response['error']}")
            return "Unable to send a message on slack"

    def read_messages(self, amount):
        try:
            result = self.client.conversations_history(
                channel=self.channel, limit=amount)
            messages = result['messages']
            
            result = []
            
            if messages:
                for msg in messages:
                    timestamp = datetime.fromtimestamp(
                        float(msg['ts'])).strftime('%Y-%m-%d %H:%M:%S')
                    user_info = self.client.users_info(user=msg['user'])
                    user_name = user_info['user']['real_name']
                    result.append(f"{msg['text']}, Author: {user_name}, Date: {timestamp}")
            else:
                result.append("No messages on this channel")
            return str(result)

        except SlackApiError as e:
            print(f"Problem: {e.response['error']}")
            return "There was a problem with reading messages from channel: "
