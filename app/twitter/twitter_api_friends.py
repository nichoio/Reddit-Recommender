
import json
import os
import sys

import twitter

USER_SCREEN_NAME = sys.argv[1]

print(USER_SCREEN_NAME)


api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')
users = api.GetFriends(screen_name=USER_SCREEN_NAME)

as_json = [json.loads(str(u)) for u in users]

# write to file as JSON
with open('/temp/'+USER_SCREEN_NAME+'Friends.json', 'w') as file:
    json.dump(as_json, file)
