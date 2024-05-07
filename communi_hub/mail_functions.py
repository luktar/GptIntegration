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
}, {
    "type": "function",
            "function": {
                "name": "check_unread_messages",
                "description": "Check if there are any unread messages on the mailbox.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
}, {
    "type": "function",
            "function": {
                "name": "list_unread_messages",
                "description": "Get all unread email messages with title, date, content and thread id.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
}, {
    "type": "function",
            "function": {
                "name": "get_contacts",
                "description": "Get all contacts including user name and email",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            },
}]
