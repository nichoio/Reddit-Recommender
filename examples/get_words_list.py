# -*- coding: iso-8859-1 -*-
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
from fuzzywuzzy import fuzz 
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import MySQLdb
import sys
import itertools
import csv
import pickle
import json

#Helper functions
def flatten(list):
  for i in list:
    for j in i:
      yield j
	  
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

#Getting the data from the DB
#Set up connection
connection = MySQLdb.connect(host = "localhost", user="root", passwd = "123+#abc", db = "reddit_recommender")

cursor = connection.cursor()

#Get the user our recommender should recommend subreddits to
def get_user(name):
	cursor.execute("select * from reddit_recommender.user where name = '" + name + "';")

	user = cursor.fetchall()
	return user
		
#Facebook
def get_facebook_data(facebook_u_id):
	if(facebook_u_id == None):
		print("The user has no Facebook account")
		
	cursor.execute("select name, category, about, genre from facebook_likes where facebook_u_id = " + facebook_u_id + ";")

	likes = cursor.fetchall()
	likes_name = []
	likes_category = []
	likes_about = []
	likes_genre = []
	for like in range(len(likes)):
		likes_name.append(likes[like][0])
		likes_category.append(likes[like][1])
		likes_about.append(likes[like][2])
		likes_genre.append(likes[like][3])
		
	facebook_likes = likes_name + likes_category + likes_about + likes_genre

	cursor.execute("select message, place from facebook_posts where message is not null and facebook_u_id = " + facebook_u_id + ";")

	posts = cursor.fetchall()
	posts_message = []
	posts_place = []
	for post in range(len(posts)):
		posts_message.append(posts[post][0])
		posts_place.append(posts[post][1])
		
	facebook_posts = posts_message + posts_place
		

	cursor.execute("select name, place, city, zip, country, rsvp_status from facebook_events where facebook_u_id = " + facebook_u_id + ";")

	events = cursor.fetchall()
	events_name = []
	events_place = []
	events_city = []
	events_zip = []
	events_country = []
	events_rsvp = []
	for event in range(len(events)):
		events_name.append(events[event][0])
		events_place.append(events[event][1])
		events_city.append(events[event][2])
		events_zip.append(events[event][3])
		events_country.append(events[event][4])
		events_rsvp.append(events[event][5])
		
	facebook_events = events_name + events_place + events_city + events_zip + events_country + events_rsvp

	cursor.execute("select name, description from facebook_groups where facebook_u_id = " + facebook_u_id + ";")

	groups = cursor.fetchall()
	groups_name = []
	groups_description = []
	for group in range(len(groups)): 
		groups_name.append(groups[group][0])
		groups_description.append(groups[group][1])
		
	facebook_groups = groups_name + groups_description
		
	facebook_data = facebook_likes + facebook_posts + facebook_events + facebook_groups
	
	return facebook_data
	
#Twitter
def get_twitter_data(twitter_screen_name):
	if(twitter_screen_name == None):
		print("The user has no Twitter account")
		
	cursor.execute("select text from twitter_tweets")
	tweets = cursor.fetchall()
	tweets_text = []
	for tweet in range(len(tweets)):
		tweets_text.append(tweets[tweet][0])
		
	twitter_tweets = tweets_text
		
	cursor.execute("select hashtag from twitter_hashtags")
	hashtags = cursor.fetchall()
	for hashtag in range(len(hashtags)): 
		tweets_hashtag.append(hashtags[hastag][0])
		
	twitter_hashtags = tweets_hashtag
		
	cursor.execute("select display_name, description from twitter_friends")
	twitter_friends_users = cursor.fetchall()
	twitter_friends_users_display_name = []
	twitter_friends_users_description = []
	for friends_user in range(len(twitter_friends_users)):
		twitter_friends_users_display_name.append(twitter_friends_users[friends_user][0])
		twitter_friends_users_description.append(twitter_friends_users[friends_user][1])
	
	twitter_friends = twitter_friends_users_display_name + twitter_friends_users_description
	
	twitter_data = twitter_tweets + twitter_hashtags + twitter_friends
	
	return twitter_data
	
#Reddit 
def get_reddit_data(reddit_u_id):
	if(reddit_u_id == None):
		print("The user has no Reddit account")
	cursor.execute("select title, display_name, advertiser_category, public_description from subreddits")
	subreddits = cursor.fetchall()
	subreddits_title = []
	subreddits_display_name = []
	subreddits_advertiser_category = []
	subreddits_public_description  = []
	for subreddit in range(len(subreddits)):
		subreddits_title.append(subreddits[subreddit][0])
		subreddits_display_name.append(subreddits[subreddit][1])
		subreddits_advertiser_category.append(subreddits[subreddit][2])
		subreddits_public_description.append(subreddits[subreddit][3])
		
	reddit_subreddits = subreddits_title + subreddits_display_name + subreddits_advertiser_category + subreddits_public_description

	cursor.execute("select comments from reddit_personal")
	reddit_personal = cursor.fetchall()
	reddit_personal_comments = []
	for comment in range(len(reddit_personal)): 
		reddit_personal_comments.append(reddit_personal[comment][0])
		
	reddit_comments = reddit_personal_comments
		
	reddit_data = reddit_subreddits + reddit_comments
	
	return reddit_data

					
#Natural language processing for posts, tweets etc. 
def filterWords(text):
	data = text
	stopWords = set(stopwords.words('german'))
	unwantedWords = ['None','Impressum', 'impressum']
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(data)
	wordsFiltered = []

	#for w in words: 
	#	if w not in stopWords: 
	#		wordsFiltered.append(w)
	wordsFiltered = [word for word in words if word not in stopWords]
	removeUnwanted = [word for word in wordsFiltered if word not in unwantedWords]	
	wordsForRec = unique_list(removeUnwanted)
	return wordsForRec
	
def analyzeData(data): 
	userWordsList = []
	for word in data: 
		userWordsList.append(filterWords(str(word)))
		
	flattenWordsList = list(flatten(userWordsList))
	#Additionally add data such as likes_name 'as they are'
	flattenWordsList = flattenWordsList #+ posts_place + likes_name + groups_name + events_name + events_place
	countWords = Counter(flattenWordsList)
	#needs to be written to a file 
	data = dict((x,y) for x, y in countWords.most_common())
	
	with open("output.txt", mode="w") as f: 
		f.write(json.dumps(data))
	
	return countWords
	
rec_user = get_user('Dominik Mollers')
user_data = get_facebook_data(rec_user[0][1]) + get_twitter_data(rec_user[0][2]) + get_reddit_data(rec_user[0][3])
print(analyzeData(user_data))
#print(rec_user[0][3])

cursor.close()
