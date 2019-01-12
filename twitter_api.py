
import json
import os

import twitter


# call http://gettwitterid.com/ to get the id by username
USER_ID = 123
USER_NAME = "LinusTech"

TWEET_AMOUNT = 500  # cannot extend 200
JSON_PATH = os.path.join('', '{}.json'.format(USER_ID))

# call https://developer.twitter.com/en/apps/app_id to get the credentials
api = twitter.Api(consumer_key='consumer_key',
                  consumer_secret='consumer_secret',
                  access_token_key='token_key',
                  access_token_secret='token_secret')

# get latest 200 tweets by this user.
data = api.GetUserTimeline(screen_name=USER_NAME, count=TWEET_AMOUNT)
data2  = api.GetUserTimeline(screen_name=USER_NAME, count=TWEET_AMOUNT, max_id=(data[199].id-1))
as_json = [json.loads(str(d)) for d in data]
as_json.extend([json.loads(str(d)) for d in data2])

# write to file as JSON
with open(JSON_PATH, 'w') as file:
    json.dump(as_json, file)
