import sys

import facebook
import MySQLdb
import twitter


def load_user(USER_NAME, TWITTER_SCREEN_NAME=None, FACEBOOK_U_ID=None, REDDIT_USER_NAME=None):
    #delete User if already exists
    statement = "DELETE FROM reddit_recommender.user WHERE name = '" + USER_NAME + "';" 
    connection = MySQLdb.connect(host = "reddit-mysql", user = "root", passwd ="password", db = "reddit_recommender", use_unicode=True, charset="utf8")
    cursor = connection.cursor()
    cursor.execute (statement)
    connection.commit()

    # request additional data from twitter and facebook
    if TWITTER_SCREEN_NAME:
        twitter_api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')
        twitter_user = user = twitter_api.GetUser(screen_name=TWITTER_SCREEN_NAME)

    #build SQL statement
    statement = "INSERT INTO reddit_recommender.user "
    #all accounts available
    if TWITTER_SCREEN_NAME and FACEBOOK_U_ID and REDDIT_USER_NAME:
        statement += "VALUES ('"
        statement += USER_NAME + "', '"
        statement += twitter_user.name + "', "
        statement += str(twitter_user.followers_count) + ", "
        statement += str(twitter_user.friends_count) + ", '"
        statement += twitter_user.description + "', '"
        statement += FACEBOOK_U_ID + "', '"
        statement += twitter_user.screen_name + "', '"
        statement += REDDIT_USER_NAME + "');"
    #not all accounts available: restrict to certain fields in database
    else:
        statement += "(name"
        values = " VALUES('" + USER_NAME + "'"
        if TWITTER_SCREEN_NAME:
            statement += ", twitter_name, twitter_followers_count, twitter_friends_count, twitter_description"
            values += ", '" + twitter_user.name + "', " + str(twitter_user.followers_count) + ", " + str(twitter_user.friends_count) + ", '" + twitter_user.description + "'"
        if FACEBOOK_U_ID:
            statement += ", facebook_u_id"
            values += ", '" + FACEBOOK_U_ID + "'"
        if TWITTER_SCREEN_NAME:
            statement += ", twitter_screen_name"
            values += ", '" + twitter_user.screen_name + "'"
        if REDDIT_USER_NAME:
            statement += ", reddit_name"
            values += ", '" + REDDIT_USER_NAME + "'"
        statement += ")"
        values += ");"
        statement += values

    # write to database
    connection = MySQLdb.connect(host = "reddit-mysql", user = "root", passwd ="password", db = "reddit_recommender", use_unicode=True, charset="utf8")
    cursor = connection.cursor()
    cursor.execute (statement)
    connection.commit()

