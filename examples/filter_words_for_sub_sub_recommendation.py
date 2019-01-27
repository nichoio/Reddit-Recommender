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



#Get the subreddit data
def get_subreddits(cursor): 
	cursor.execute("select title, display_name, subscribers, advertiser_category, public_description, description from reddit_recommender.subreddits")
	
	subreddits = cursor.fetchall()
	return subreddits 
	
def filterWords(text):
	data = text
	stopWords = set(stopwords.words('english'))
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
	

def append_subreddits_to_file(subreddits):
	
	analyze_subreddit_data = []
	file = open("../app/output_subreddits_words_list.txt", mode="w")
	for subreddit in range(len(subreddits)):
		subredditWordsList = []
		for word in subreddits[subreddit]: 
			subredditWordsList.append(filterWords(str(word)))
			
		flattenWordsList = list(flatten(subredditWordsList))
		
		file.write(json.dumps(flattenWordsList)+'\n')
		
	file.close()
		

def start():
	#Getting the subreddit data from the database
	connection = MySQLdb.connect(host="localhost", user="root", passwd="123+#abc", db="reddit_recommender")
	
	cursor = connection.cursor()
	subreddits = get_subreddits(cursor)
	append_subreddits_to_file(subreddits)
	cursor.close()
	
start()