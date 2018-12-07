
import json
import os
import sys

import twitter

USER_SCREEN_NAME = sys.argv[1]


api = twitter.Api(consumer_key='cuo7ucRgiJgeNitMDN06sxTCc',
                  consumer_secret='1GPOk1uEI8JVfTh5ZgJx7Mh0LvirimArrx4J8lSAAnQvVBvcjQ',
                  access_token_key='3300929751-42EWTc221XXOLGz3mBvJuEmAkZt1NIRnqk85uWL',
                  access_token_secret='PhGQz9I5Sjf61RNLXN6fPeEMbKQHNTZ6bcNaGJkHf2Rua')

users = api.GetFriends(screen_name=USER_SCREEN_NAME)

as_json = [json.loads(str(u)) for u in users]

# write to file as JSON
with open(USER_SCREEN_NAME+'Friends.json', 'w') as file:
    json.dump(as_json, file)
