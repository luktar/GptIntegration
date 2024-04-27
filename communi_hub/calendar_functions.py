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
            }
    },
    {
    "type": "function",
            "function": {
                "name": "delete_appointment_from_calendar",
                "description": "Delete appointment from the calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "appointment_date": {
                            "type": "string",
                            "description": "The date of the appointment in YYYY-MM-DD format",
                        }
                    },
                    "required": ["appointment_date"],
                },
            }
}]
