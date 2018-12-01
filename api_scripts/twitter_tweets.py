import json
import os

import twitter


# call http://gettwitterid.com/ to get the id by username
USER_ID = 123

TWEET_AMOUNT = 200  # cannot extend 200
JSON_PATH = os.path.join('', '{}.json'.format(USER_ID))

# call https://developer.twitter.com/en/apps/app_id to get the credentials
api = twitter.Api(
    consumer_key='consumer_key',
    consumer_secret='consumer_secret',
    access_token_key='access_token_key',
    access_token_secret='access_token_secret')

# get latest 200 tweets by this user.
data = api.GetUserTimeline(user_id=USER_ID, count=TWEET_AMOUNT)
as_json = [json.loads(str(d)) for d in data]

# write to file as JSON
with open(JSON_PATH, 'w') as file:
    json.dump(as_json, file, ensure_ascii=False)
