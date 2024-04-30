from datetime import datetime
import os
import json
import sys
from communi_hub import calendar_functions, mail_functions, slack_functions, weather_functions
from communi_hub.slack_connector import SlackConnector
from communi_hub.calendar_connector import CalendarConnector
from communi_hub.mail_connector import MailConnector
from communi_hub.weather_connector import WeatherConnector
from voice_generator.voice_generator import VoiceGenerator
from voice_reader.voice_reader import VoiceReader
from openai import OpenAI
from dotenv import load_dotenv
import langdetect
from datetime import datetime

load_dotenv()

slack_connector = SlackConnector()
weather_connector = WeatherConnector()
email_connector = MailConnector()
calendar_connector = CalendarConnector()
voice_reader = VoiceReader()
voice_generator = VoiceGenerator()

gpt_model = "gpt-3.5-turbo-0125"
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

messages = []

available_functions = {
    "get_current_weather": weather_connector.get_current_weather,
    "send_message_on_slack": slack_connector.send_message,
    "read_messages_from_slack": slack_connector.read_messages,
    "send_email": email_connector.send_email,
    "add_appointment_to_calendar": calendar_connector.add_appointment_to_calendar,
    "delete_appointment_from_calendar": calendar_connector.delete_appointment_from_calendar
}

tools = calendar_functions.functions + slack_functions.functions + \
    mail_functions.functions + weather_functions.functions


def function_call(tool_calls):
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

def run_conversation(messages):
    response = client.chat.completions.create(
        model=gpt_model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    messages.append(response_message)

    if tool_calls:
        return function_call(tool_calls)
    return response_message

def is_polish(text):
    try:
        return langdetect.detect(text) == 'pl'
    except Exception as e:
        print("Error in language detection:", e)
        return False

def run_conversation(messages):
    response = client.chat.completions.create(
        model=gpt_model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    messages.append(response_message)

    if tool_calls:
        return function_call(tool_calls)
    return response_message

def is_polish(text):
    try:
        return langdetect.detect(text) == 'pl'
    except Exception as e:
        print("Error in language detection:", e)
        return False

def main():
    current_date = datetime.now().strftime('%m-%d-%Y')
    messages.append({"role": "system", "content": "Nazywam się Kazimierz Kowalski. Dzisiejsza data to: " +
                    current_date + ". Posługuj się wyłącznie językiem polskim."})

    while True:
        user_input = ''
        if '-t' in sys.argv:
            user_input = input("Wpisz tekst: ")
        else:
            user_input = voice_reader.record_voice()
            print(user_input)

        if(not is_polish(user_input)):
            print("Nie udało się wysłać wiadomości. Spróbuj ponownie...")
            continue

        messages.append(
            {"role": "user", "content": user_input})
        # {"role": "user", "content": "Przeczytaj dwie ostatnie wiadomości na slacku."}]
        # # {"role": "user", "content": "Please send email message Hi, when will you start your work today? to the email paweltomkow@gmail.com"},
        # {"role": "user", "content": transcription}]
        # {"role": "user", "content": "Please add appointment with title Project Onboarding Meeting for a next friday. Today is 22.04.2024"},
        # {"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"},
        # {"role": "user", "content": "Please add appointment to the calendar with title Project Onboarding Meeting for a next friday. Today is 27.04.2024"}]
        # {"role": "user", "content": "Please add appointment to the calendar with title Project Onboarding Meeting for a tomorrow. Today is 27.04.2024"}]
        # {"role": "user", "content": "Please add appointment to the calendar with title Project Onboarding Meeting for a second Monday on the next month. Today is 27.04.2024"}]
        # {"role": "user", "content": "Please delete appointment from the calendar from a next friday. Today is 27.04.2024"}]
        # {"role": "user", "content": "Please delete appointment from the calendar from a tomorrow. Today is 27.04.2024"}]
        # {"role": "user", "content": "Please delete appointment from the calendar from a second Monday on the next month. Today is 27.04.2024"}]

        chat_completion = run_conversation(messages)

        result = ''
        if (hasattr(chat_completion, 'content')):
            result = chat_completion.content
        elif (hasattr(chat_completion.choices[0].message, 'content')):
            result = chat_completion.choices[0].message.content
    
        print(result)
        if not '-t' in sys.argv:
            voice_generator.generate_voice(result)


if __name__ == "__main__":
    main()
