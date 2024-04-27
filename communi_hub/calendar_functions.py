functions = [{
    "type": "function",
            "function": {
                "name": "add_appointment_to_calendar",
                "description": "Add appointment to the calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_title": {
                            "type": "string",
                            "description": "Appointment title",
                        },
                        "appointment_date": {
                            "type": "string",
                            "description": "The start date for the appointment in YYYY-MM-DD format",
                        }
                    },
                    "required": ["appointment_title", "appointment_date"],
                },
            },
            "function": {
                "name": "del_appoinment_from_calendar",
                "description": "Add appointment to the calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_title": {
                            "type": "string",
                            "description": "Appointment title",
                        },
                        "appointment_date": {
                            "type": "string",
                            "description": "The start date for the appointment in YYYY-MM-DD format",
                        }
                    },
                    "required": ["appointment_title", "appointment_date"],
                },
            },
}]
