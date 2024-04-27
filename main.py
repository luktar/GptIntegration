import os
import json
from communi_hub.slack_connector import SlackConnector
from communi_hub.calendar_connector import CalendarConnector
from communi_hub.mail_connector import MailConnector
from communi_hub.weather_connector import WeatherConnector
from voice_generator.voice_generator import VoiceGenerator
from voice_reader.voice_reader import VoiceReader
from openai import OpenAI

slack_connector = SlackConnector()
weather_connector = WeatherConnector()
email_connector = MailConnector()
calendar_connector = CalendarConnector()

gpt_model = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


available_functions = {
    "get_current_weather": weather_connector.get_current_weather,
    "send_message_on_slack": slack_connector.send_message,
    "send_email": email_connector.send_email,
    "add_appointment_to_calendar": calendar_connector.add_appointment_to_calendar
}


def run_conversation(messages):
    # Step 1: send the conversation and available functions to the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        },
        {
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
        },
        {
            "type": "function",
            "function": {
                "name": "send_email",
                "description": "Send Email message",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message typed to send",
                        },
                        "email": {
                            "type": "string",
                            "description": "Message receiver email address",
                        }
                    },
                    "required": ["message", "email"],
                },
            },
        },
        {
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
                        "date": {
                            "type": "string",
                            "description": "The start date for the appointment in YYYY-MM-DD format",
                        }
                    },
                    "required": ["appointment_title", "date"],
                },
            },
        }
    ]

    response = client.chat.completions.create(
        model=gpt_model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    print(response.choices[0].message.content)

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:

        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            print("FUNCTION RETURNED: " + function_response)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response


def main():
    # Tutaj umieść główną logikę swojego programu
    # uncomment test propmpts to check if function calling works
    # messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    messages = [
        # {"role": "user", "content": "Add a new event into the calendar and name it a feedback meeting with Rebeca. Set the date on 24th of July 2024."}]
        {"role": "user", "content": "Please send email message Hi, when will you start your work today? to the email paweltomkow@gmail.com"}]
    # messages = [{"role": "user", "content": "Please add appointment with title Project Onboarding Meeting for a next friday. Today is 22.04.2024"}]
    chat_completion = run_conversation(messages)
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
