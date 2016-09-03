import os
from slackclient import SlackClient


BOT_NAME = 'anon-bot'

slack_client = SlackClient('xoxb-76025536419-kXoQ5HjaeX3hEzedIZicBJlY')


if __name__ == "__main__":
    api_call = slack_client.api_call("channels.list")
    if api_call.get('ok'):
        channels = api_call.get('channels')
        for channel in channels:
            print(channel)
        # retrieve all users so we can find our bot
        # users = api_call.get('members')
        # for user in users:
        #     if 'name' in user and user.get('name') == BOT_NAME:
        #         print(user)
    else:
        print("could not find bot user with the name " + BOT_NAME)
