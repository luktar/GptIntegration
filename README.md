# What can I do with this program?

You can talk with your voice or texting and manage google calendar, gmail, Slack and shopping list.
Example commands:
1. Do I have any unread email messages?
2. Get and read all unread email messages
3. Get contact list
4. Send message to someone from the contact list
5. Get 3 last messages from slack
6. Send 'xxxx' on slack
7. Add milk and butter to the shopping list
8. I've bouth milk (it will be market as bouth)
9. Is there anything to buy on a shopping list?
10. Set up meeting tomorrow at 8:00
11. Remove meeting from tomorrow at 8:00

# How to run the project?

Before you start you need to generate:
1. [OpenAPI](https://platform.openai.com/docs/quickstart) token
2. [Slack token](https://api.slack.com/tutorials/tracks/getting-a-token) - you need to create Slack App
3. [Google](https://developers.google.com/calendar/api/quickstart/go) API credentials (JSON)

Put tokens into `.env` file.

```OPENAI_API_KEY='<open_api_token>'
SLACK_API_KEY='<slack_api_token>'
GOOGLE_CRED='<google_json_credentials>'
SLACK_CHANNEL_ID='<slack_channel_id>'```

1. Run: `python websites/shoppingListBackend.py`
2. Open `websites/shoppingList.html` in the web browser
3. Run: `python main.py` for voice mode or `python main.py -t` for text mode

