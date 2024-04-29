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
                        },
                        "appointment_hour": {
                            "type": "string",
                            "description": "The hour of the appointment in 24 hour format (0-23) and 2 digits",
                        }
                    },
                    "required": ["appointment_title", "appointment_date", "appointment_hour"],
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
                        },
                        "appointment_hour": {
                            "type": "string",
                            "description": "The hour of the appointment in 24 hour format (0-23) and 2 digits",
                        }
                    },
                    "required": ["appointment_date", "appointment_hour"],
                },
            }
}]
