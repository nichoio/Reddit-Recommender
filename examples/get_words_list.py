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

#Getting the data from the DB
connection = MySQLdb.connect(host = "localhost", user="root", passwd = "123+#abc", db = "reddit_recommender")

cursor = connection.cursor()

cursor.execute("select distinct facebook_u_id from facebook_likes")

users = cursor.fetchall()

cursor.execute("select name, category, about, genre from facebook_likes where facebook_u_id = " + str(users[0][0]))

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

cursor.execute("select message, place from facebook_posts where message is not null and facebook_u_id = " + str(users[0][0]))

posts = cursor.fetchall()
posts_message = []
posts_place = []
for post in range(len(posts)):
	posts_message.append(posts[post][0])
	posts_place.append(posts[post][1])
	

cursor.execute("select name, place, city, zip, country, rsvp_status from facebook_events where facebook_u_id = " + str(users[0][0]))

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

cursor.execute("select name, description from facebook_groups where facebook_u_id = " + str(users[0][0]))

groups = cursor.fetchall()
groups_name = []
groups_description = []
for group in range(len(groups)): 
	groups_name.append(groups[group][0])
	groups_description.append(groups[group][1])


cursor.close()

user_data = posts_message + posts_place + likes_name + likes_about + likes_category + likes_genre + groups_name + groups_description + events_name + events_city + events_country + events_place + events_rsvp + events_zip
#user_data_list.append(likes)
#user_data_list.append(posts)
#user_data_list.append(groups)
#user_data_list.append(events)
#user_data = flatten(user_data_list)
#user_data_clean = Counter(list(user_data))

					
#Natural language processing for posts, tweets etc. 
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
					
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
	flattenWordsList = flattenWordsList + posts_place + likes_name + groups_name + events_name + events_place
	countWords = Counter(flattenWordsList)
	#needs to be written to a file 
	data = dict((x,y) for x, y in countWords.most_common())
	
	with open("output.txt", mode="w") as f: 
		f.write(json.dumps(data))
	
	return countWords
	

print(analyzeData(user_data))
#print(likes)

