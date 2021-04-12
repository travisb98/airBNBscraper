


# https://slack.dev/python-slack-sdk/installation/index.html#access-tokens

# https://pypi.org/project/slack-sdk/


#  import json
# #########################

# import os
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError

# # client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# try:
#     response = client.chat_postMessage(channel='#big-trip', text="This is a test message message from Trav Bot")
#     assert response["message"]["text"] == "Hello world!"
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")