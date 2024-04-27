import os
import json
from communi_hub import calendar_functions, mail_functions, slack_functions, weather_functions
from communi_hub.slack_connector import SlackConnector
from communi_hub.calendar_connector import CalendarConnector
from communi_hub.mail_connector import MailConnector
from communi_hub.weather_connector import WeatherConnector
from voice_generator.voice_generator import VoiceGenerator
from voice_reader.voice_reader import VoiceReader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

slack_connector = SlackConnector()
weather_connector = WeatherConnector()
email_connector = MailConnector()
calendar_connector = CalendarConnector()
voice_reader = VoiceReader()

gpt_model = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


available_functions = {
    "get_current_weather": weather_connector.get_current_weather,
    "send_message_on_slack": slack_connector.send_message,
    "read_messages_from_slack": slack_connector.read_messages,
    "send_email": email_connector.send_email,
    "add_appointment_to_calendar": calendar_connector.add_appointment_to_calendar,
}


def run_conversation(messages):
    # Step 1: send the conversation and available functions to the model
    tools = calendar_functions.functions + slack_functions.functions + \
        mail_functions.functions + weather_functions.functions

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
            )
        second_response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
        )
        return second_response


def main():
    # Call the read_voice method on the instance
    transcription = voice_reader.record_voice()
    # Tutaj umieść główną logikę swojego programu
    messages = [
        {"role": "user", "content": "Przeczytaj dwie ostatnie wiadomości na slacku."},
        # # {"role": "user", "content": "Please send email message Hi, when will you start your work today? to the email paweltomkow@gmail.com"},
        {"role": "user", "content": transcription},
        # {"role": "user", "content": "Please add appointment with title Project Onboarding Meeting for a next friday. Today is 22.04.2024"},
        # {"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"},
    ]
    chat_completion = run_conversation(messages)
    print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    main()
