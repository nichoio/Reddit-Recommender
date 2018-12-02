
import json
import os
import sys

import twitter

USER_SCREEN_NAME = sys.argv[1]

TWEET_AMOUNT = 500  # cannot extend 200
JSON_PATH = os.path.join('', '{}.json'.format(USER_SCREEN_NAME))

# call https://developer.twitter.com/en/apps/app_id to get the credentials
api = twitter.Api(...)

# get latest 200 tweets by this user.
data = api.GetUserTimeline(screen_name=USER_SCREEN_NAME, count=TWEET_AMOUNT)
data2  = api.GetUserTimeline(screen_name=USER_SCREEN_NAME, count=TWEET_AMOUNT, max_id=(data[199].id-1))
as_json = [json.loads(str(d)) for d in data]
as_json.extend([json.loads(str(d)) for d in data2])

# write to file as JSON
with open(JSON_PATH, 'w') as file:
    json.dump(as_json, file)
