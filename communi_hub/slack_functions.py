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
                    "description": "Put a message content here",
                },
            },
            "required": ["message"],
        },
    },
}]
