functions = [{
    "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send Email message",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text_message": {
                            "type": "string",
                            "description": "Message typed to send",
                        },
                        "email": {
                            "type": "string",
                            "description": "Message receiver email address",
                        }
                    },
                    "required": ["text_message", "email"],
                },
            },
}]
