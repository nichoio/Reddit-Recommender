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

#Getting the subreddit data from the database
connection = MySQLdb.connect(host="localhost", user="root", passwd="password", db="reddit_recommender")

cursor = connection.cursor()

#Get the subreddit data
def get_subreddits(): 
	cursor.execute("select title, display_name, advertiser_category, public_description, description from reddit_recommender.subreddits")
	
	subreddits = cursor.fetchall()
	return subreddits 
	
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
	

def append_subreddits_to_file():
	subreddits = get_subreddits()
	analyze_subreddit_data = []
	file = open("output_subreddits.txt", mode="w")
	for subreddit in range(len(subreddits)):
		subredditWordsList = []
		for word in subreddits[i]: 
			subredditWordsList.append(filterWords(str(word))
			
		flattenWordsList = list(flatten(subredditWordsList))
		countWords = Counter(flattenWordsList)
		data = dict((x,y) for x, y in countWords.mostCommon())
		
		file.write(json.dumps(data)+'\n')
		
	file.close()
		


append_subreddits_to_file()

cursor.close()