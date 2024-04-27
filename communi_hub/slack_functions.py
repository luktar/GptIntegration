functions = [{
    "type": "function",
    "function": {
        "name": "send_message_on_slack",
        "description": "Send message on slack",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Message typed to send",
                },
                "receiver_name": {
                    "type": "string",
                    "description": "Message receiver name",
                },
                "receiver_surname": {
                    "type": "string",
                    "description": "Message receiver surname",
                },
            },
            "required": ["message", "receiver_name", "receiver_surname"],
        },
    },
}]
