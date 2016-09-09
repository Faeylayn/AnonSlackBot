This is a pretty basic outline for a slack bot that takes DMs and posts them
anonymously in a different channel.

It requires 4 environment variables be set up,  
BOT_ID (the user ID hash that slack makes for all users)
SALT (this is added to the user's id so as to anonymize the messages)
ANON_CHANNEL (The channel id hash for the channel that the anonymous messages
   are supposed to be sent to)
and SLACK_BOT_TOKEN (the api token for the slack team)

Possible followups include adding a salt environment variable to would be added
to the user id of incoming messages and then have that hashed again for the user hash
