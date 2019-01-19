
import json
import os
import sys

import twitter

USER_SCREEN_NAME = sys.argv[1]

TWEET_AMOUNT = 200 # cannot exceed 200 per call

# call https://developer.twitter.com/en/apps/app_id to get the credentials
api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')

# get latest 2 * TWEET_AMOUNT tweets by this user.
data = api.GetUserTimeline(screen_name=USER_SCREEN_NAME, count=TWEET_AMOUNT)
as_json = [json.loads(str(d)) for d in data]
if len(data) > 199:
    data2  = api.GetUserTimeline(screen_name=USER_SCREEN_NAME, count=TWEET_AMOUNT, max_id=(data[199].id-1))
    as_json.extend([json.loads(str(d)) for d in data2])

# write to file as JSON
with open(USER_SCREEN_NAME+'Tweets.json', 'w') as file:
    json.dump(as_json, file)

user = api.GetUser(screen_name=USER_SCREEN_NAME)
user_as_json = [json.loads(str(user))]
with open(USER_SCREEN_NAME+'User.json', 'w') as file:
    json.dump(user_as_json, file)
