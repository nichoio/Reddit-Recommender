import MySQLdb
import sys
import twitter
import facebook

# expected inputs
TWITTER_SCREEN_NAME = sys.argv[1]
FACEBOOK_ACCESS_TOKEN = sys.argv[2]
REDDIT_USER_NAME = sys.argv[3]
USER_NAME = sys.argv[4]

# request additional data from twitter and facebook
twitter_api = twitter.Api(consumer_key='a',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='')
twitter_user = user = twitter_api.GetUser(screen_name=TWITTER_SCREEN_NAME)
graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN, version='3.1')
facebook_user = graph.get_object(id='me', fields='id,name,birthday,gender')

#build SQL statement
statement = "INSERT INTO reddit_recommender.user VALUES ('"
statement += USER_NAME + "', '"
statement += facebook_user['gender'] + "', '"
statement += twitter_user.name + "', "
statement += str(twitter_user.followers_count) + ", "
statement += str(twitter_user.friends_count) + ", '"
statement += twitter_user.description + "', '"
statement += facebook_user['id'] + "', '"
statement += twitter_user.screen_name + "', '"
statement += REDDIT_USER_NAME + "');"

# write to database
connection = MySQLdb.connect(host = "127.0.0.1", user = "", passwd ="", db = "reddit_recommender", use_unicode=True, charset="utf8")
cursor = connection.cursor()
cursor.execute (statement)
connection.commit()