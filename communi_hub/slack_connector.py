class SlackConnector:
    def __init__(self) -> None:
        pass

    def send_message(self, message, receiver_name, receiver_surname) -> bool:
        return 'Slack message sent: ' + message + " receiver_name: " + receiver_name + " receiver_surname: " + receiver_surname
