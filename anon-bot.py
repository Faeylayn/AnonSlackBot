import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
BOT_DM = os.environ.get("BOT_DM")

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

ANON_CHANNEL = os.environ.get("ANON_CHANNEL")

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            message = parse_slack_output(slack_client.rtm_read())
            if message:
                anon_message(message)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


def anon_message(message):

    slack_client.api_call("chat.postMessage", channel=ANON_CHANNEL,
                          text=message, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'channel' in output and BOT_DM in output['channel'] and 'text' in output:
                # return text after the @ mention, whitespace removed
                return output['text']
    return None, None
