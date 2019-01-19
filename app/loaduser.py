import MySQLdb
import sys
import twitter
import facebook

# expected inputs --> if one platform is not used NOTUSED expected
# user_name always required
def loadUser(TWITTER_SCREEN_NAME, FACEBOOK_ACCESS_TOKEN, REDDIT_USER_NAME, USER_NAME):
    #delete User if already exists
    statement = "DELETE FROM reddit_recommender.user WHERE name = '" + USER_NAME + "';" 
    connection = MySQLdb.connect(host = "reddit-mysql", user = "root", passwd ="password", db = "reddit_recommender", use_unicode=True, charset="utf8")
    cursor = connection.cursor()
    cursor.execute (statement)
    connection.commit()

    # request additional data from twitter and facebook
    if TWITTER_SCREEN_NAME != "NOTUSED":
        twitter_api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')
        twitter_user = user = twitter_api.GetUser(screen_name=TWITTER_SCREEN_NAME)
    if FACEBOOK_ACCESS_TOKEN != "NOTUSED":
        graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN, version='3.1')
        facebook_user = graph.get_object(id='me', fields='id,name,birthday,gender')

    #build SQL statement
    statement = "INSERT INTO reddit_recommender.user "
    #all accounts available
    if TWITTER_SCREEN_NAME != "NOTUSED" and FACEBOOK_ACCESS_TOKEN != "NOTUSED" and REDDIT_USER_NAME != "NOTUSED":
        statement += "VALUES ('"
        statement += USER_NAME + "', '"
        statement += facebook_user['gender'] + "', '"
        statement += twitter_user.name + "', "
        statement += str(twitter_user.followers_count) + ", "
        statement += str(twitter_user.friends_count) + ", '"
        statement += twitter_user.description + "', '"
        statement += facebook_user['id'] + "', '"
        statement += twitter_user.screen_name + "', '"
        statement += REDDIT_USER_NAME + "');"
    #not all accounts available: restrict to certain fields in database
    else:
        statement += "(name"
        values = " VALUES('" + USER_NAME + "'"
        if FACEBOOK_ACCESS_TOKEN != "NOTUSED":
            statement += ", facebook_gender"
            values += ", '" + facebook_user['gender'] + "'"
        if TWITTER_SCREEN_NAME != "NOTUSED":
            statement += ", twitter_name, twitter_followers_count, twitter_friends_count, twitter_description"
            values += ", '" + twitter_user.name + "', " + str(twitter_user.followers_count) + ", " + str(twitter_user.friends_count) + ", '" + twitter_user.description + "'"
        if FACEBOOK_ACCESS_TOKEN != "NOTUSED":
            statement += ", facebook_u_id"
            values += ", '" + facebook_user['id'] + "'"
        if TWITTER_SCREEN_NAME != "NOTUSED":
            statement += ", twitter_screen_name"
            values += ", '" + twitter_user.screen_name + "'"
        if REDDIT_USER_NAME != "NOTUSED":
            statement += ", reddit_u_id"
            values += ", '" + REDDIT_USER_NAME + "'"
        statement += ")"
        values += ");"
        statement += values

    # write to database
    connection = MySQLdb.connect(host = "reddit-mysql", user = "root", passwd ="password", db = "reddit_recommender", use_unicode=True, charset="utf8")
    cursor = connection.cursor()
    cursor.execute (statement)
    connection.commit()

