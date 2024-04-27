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
    }, {
        "type": "function",
        "function": {
            "name": "read_messages_from_slack",
            "description": "Read messages from slack",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Put a number of latest messages you want to read. If use didn't specify this number you can put value 1.",
                    },
                },
                "required": ["amount"],
            },
        },
    }]
