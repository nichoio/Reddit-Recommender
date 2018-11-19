import twitter

# call http://gettwitterid.com/ to get the id by username
USER_ID = 123

# call https://developer.twitter.com/en/apps/app_id to get the credentials
api = twitter.Api(
    consumer_key='consumer_key',
    consumer_secret='consumer_secret',
    access_token_key='access_token_key',
    access_token_secret='access_token_secret')

# get latest 20 tweets by this user.
data = api.GetUserTimeline(user_id=3300929751)

for d in data:
    print(str(d) + '\n')