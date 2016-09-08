import os
import time
import hashlib
from slackclient import SlackClient

# starterbot's ID as an environment variable
# BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U280RFSCB"

# constants
# BOT_DM = os.environ.get("BOT_DM")
BOT_DM = "D28269FUG"
SALT = "1234abcd."

# ANON_CHANNEL = os.environ.get("ANON_CHANNEL")
ANON_CHANNEL = 'C280R4B0T'

# instantiate Slack clients
# slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient('xoxb-76025536419-kXoQ5HjaeX3hEzedIZicBJlY')



def anon_message(message, user):
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
            # if output and 'channel' in output and BOT_DM in output['channel'] and 'text' in output:
            if output and 'channel' in output and 'text' in output:
                # return text after the @ mention, whitespace removed
                if output['channel'][0] == "D":
                    # api_call = slack_client.api_call("channels.info", channel=output['channel'])
                    # print "hi"
                    # print api_call
                    # if api_call.get("ok"):
                    # # if api_call.get('ok') and BOT_ID in api_call.get("channel").get('members'):
                    #     print api_call.get("channel")
                    print output['user']
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
