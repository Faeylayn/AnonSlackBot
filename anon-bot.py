import os
import time
import hashlib
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
ANON_CHANNEL = os.environ.get("ANON_CHANNEL")
SALT = os.environ.get("SALT")

# instantiate Slack clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))



def anon_message(message, user):
    """
        This function hashes the user id with the environ salt variable
        so that the user cannot be reverse engineered and the user messages can
        line up under the same name.
    """
    hashed_user = hashlib.sha1(SALT + str(user))
    new_message = "User" + hashed_user.hexdigest() + ": " + message
    slack_client.api_call("chat.postMessage", channel=ANON_CHANNEL,
                          text=new_message)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'channel' in output and 'text' in output:
                print output['channel']
                if output['channel'][0] == "D":
                    return output['text'], output['user']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        while True:
            message, user = parse_slack_output(slack_client.rtm_read())
            if message and user:
                anon_message(message, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
