import os
from communi_hub.calendar_connector import CalendarConnector
from communi_hub.mail_connector import MailConnector
from communi_hub.slack_connector import SlackConnector
from voice_generator.voice_generator import VoiceGenerator
from voice_reader.voice_reader import VoiceReader
import config
from openai import OpenAI
import json

gpt_model = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API


def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def send_message_on_slack(message, receiver_name, receiver_surname):
    return 'Slack message sent: ' + message + " receiver_name: " + receiver_name + " receiver_surname: " + receiver_surname


def send_email(message, email):
    return 'Email message sent ' + message + ' email'


def add_appointment_to_calendar(appointment_title, date):
    return 'Added appointment to calendar: ' + appointment_title + " for date " + date


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
        tool_choice="auto",  # auto is default, but we'll be explicit
    )

    print(response.choices[0].message.content)

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "send_message_on_slack": send_message_on_slack,
            "send_email": send_email,
            "add_appointment_to_calendar": add_appointment_to_calendar
        }
        # extend conversation with assistant's reply
        messages.append(response_message)
        # Step 4: send the info for each function call and function response to the model
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
        {"role": "user", "content": "Please send slack message Hi, when will you start your work today? to the user Pawel Tomków"}]
    # messages = [{"role": "user", "content": "Please send email message Hi, when will you start your work today? to the email paweltomkow@gmail.com"}]
    # messages = [{"role": "user", "content": "Please add appointment with title Project Onboarding Meeting for a next friday. Today is 22.04.2024"}]
    chat_completion = run_conversation(messages)
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
