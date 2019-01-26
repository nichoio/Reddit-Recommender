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
	 
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

#Getting the subreddit data from the database
connection = MySQLdb.connect(host="localhost", user="root", passwd="123+#abc", db="reddit_recommender")

cursor = connection.cursor()

#Get the subreddit data
def get_subreddits(): 
	cursor.execute("select title, display_name, advertiser_category, public_description, description from reddit_recommender.subreddits limit 20")
	
	subreddits = cursor.fetchall()
	return subreddits 
	
	
subreddits = get_subreddits()
	
	
def get_user_subreddits():
	cursor.execute("select title, display_name, advertiser_category, public_description, description from reddit_recommender.subreddits limit 5")
	user_subreddits = cursor.fetchall()
	return user_subreddits

	
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
	

def append_subreddits():
	analyze_subreddit_data = []
	subredditWordsList = []
	flatten_subreddits = []
	for subreddit in range(len(subreddits)):
		for word in subreddits[subreddit]: 
			subredditWordsList.append(filterWords(str(word)))
			
		flattenWordsList = list(flatten(subredditWordsList))
		#Additionally add data such as likes_name 'as they are'
		flattenWordsList = flattenWordsList #+ posts_place + likes_name + groups_name + events_name + events_place
		countWords = Counter(flattenWordsList)
		flatten_subreddits.append(countWords)
		
	return flatten_subreddits
	
	
def compareSubreddits(): 
	subredditsWordsList = append_subreddits_to_file()
	for subreddit in range(len(subredditWordsList)):
		for subreddit_subreddit in range(len(subredditWordsList)): 
			get_jaccard_sim()
			

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
	a = set(subreddit1)
	b = set(subreddit2)
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))
	


def compute_jaccard_subreddit_sim():
	userSubreddits = get_user_subreddits()
	subreddit_sim_list = []
	subreddit_subreddit_list = []
	
	for userSubreddit in range(len(userSubreddits)):
		result = []
		for subreddit in range(len(subreddits)): 
			result.append(get_jaccard_sim(userSubreddits[userSubreddit],subreddits[subreddit]))
		subreddit_subreddit_list.append(result)	
	return subreddit_subreddit_list



def compute_subreddit_recommendation(): 
	lists=compute_jaccard_subreddit_sim()

	indices=[]
	recommendation = []
	for list in lists: 
		indices.append(sorted(range(len(list)), key=lambda i: list[i])[-4:])
		
	print(indices)	
	for i in range(len(indices)):
		#deletes the last element in the list of lists as it is the subreddit that gets compared with itself.
		del indices[i][-1]
		for j in indices[i]:
			recommendation.append(subreddits[j][1])
			
	return recommendation
	
print(compute_subreddit_recommendation())