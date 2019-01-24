
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

#Helper functions
def flatten(list):
  for i in list:
    for j in i:
      yield j

#Some similaritiy measures
def get_vectors(*strs):
	text = [t for t in strs]
	vectorizer = CountVectorizer(text)
	vectorizer.fit(text)
	return vectorizer.transform(text).toarray()

def get_cosine_sim(*strs):
	vectors = [t for t in get_vectors(*strs)]
	return cosine_similarity(vectors)

def get_jaccard_sim(subreddit1, subreddit2):
	a = set(subreddit1.split())
	b = set(subreddit2.split())
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))


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
	

def append_subreddits_to_file():
	subreddits = get_subreddits()
	analyze_subreddit_data = []
	subredditWordsList = []
	flatten_subreddits = []
	for subreddit in range(len(subreddits)):
		for word in subreddits[i]: 
			subredditWordsList.append(filterWords(str(word)))
		flattenWordsList = list(flatten(userWordsList))
		#Additionally add data such as likes_name 'as they are'
		flattenWordsList = flattenWordsList #+ posts_place + likes_name + groups_name + events_name + events_place
		countWords = Counter(flattenWordsList)
		flatten_subreddits.append(countWords)
		
	return flatten_subreddits
	
	
def compareSubreddits(): 
	subredditsWordsList = append_posts_to_file()
	all_similarities = []

	for subreddit in range(len(subredditsWordsList)):
		similarities = []
		for subreddit_subreddit in range(len(subredditsWordsList)):
			similarities.append(get_jaccard_sim(subredditsWordsList[subreddit],subredditsWordsList[subreddit_subreddit]))
		all_similarities.append(similarities)

	return all_similarities

def getBest(ranking, best):
	result = sorted(range(len(ranking)), key=lambda i: ranking[i])[-best:]
	return result

def getAllBest(best):
	data = compareSubreddits()
	allRankings = []
	for datum in data:
		allRankings.append(getBest(datum, best))

	return allRankings

def mapRanking(subreddits, allRankings, best):
	allRanklists = []
	for ranking in allRankings:
		ranklist = []
		for index in best:
			list = []
			list.append(subreddits[index][0])
			list.append(allRankings[index])
			ranklist.append(list)
	allRanklists.append(ranklist)
	return(allRanklists)

#rec_user = get_user('Dominik Mollers')
#user_data = get_facebook_data(rec_user[0][1]) #+ get_twitter_data(rec_user[0][2]) + get_reddit_data(rec_user[0][3])
#print(analyzeData(user_data))

postsList = append_posts_to_file()

subreddits = append_posts_to_file()
rankings = compareSubreddits()[0]
best = getAllBest(5)[0]


print(mapRanking(subreddits, rankings, best))
#print(mapRanking(subreddits, rankings, best))



cursor.close()
