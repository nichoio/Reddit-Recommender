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


#Getting the data from the DB
connection = MySQLdb.connect(host = "localhost", user="root", passwd = "123+#abc", db = "reddit_recommender")

cursor = connection.cursor()

cursor.execute("select name from facebook_likes")

likes = cursor.fetchall()

cursor.execute("select message from facebook_posts where message is not null")

post_messages = cursor.fetchall()

cursor.execute("select name from facebook_events")

events = cursor.fetchall()

cursor.execute("select name, description from facebook_groups")

groups = cursor.fetchall()
groups_name = []
groups_description = []
for g in groups: 
	groups_name.append(groups[1][0])
	groups_description.append(groups[1][1])


cursor.close()

#Some similaritiy measures	
def get_vectors(*strs): 
	text = [t for t in strs]
	vectorizer = CountVectorizer(text)
	vectorizer.fit(text)
	return vectorizer.transform(text).toarray()
	
def get_cosine_sim(*strs): 
	vectors = [t for t in get_vectors(*strs)]
	return cosine_similarity(vectors)

def get_jaccard_sim(str1, str2):
	a = set(str1.split())
	b = set(str2.split())
	c = a.intersection(b)
	return float(len(c)) / (len(a) + len(b) - len(c))


#simple recommendation	
def check(str, list): 
	if str in list: 
		print("You are already subscribes to " + str + ".")
	else: 
		print("You might also like this subreddit: " + str + ".")
		
def recommend(likeslist, subredditlist): 
	for i in likeslist:
		for j in subredditlist:
			if fuzz.partial_token_set_ratio(i, j) == 100:
				if j in sublist: 
					print("You are already subscribes to " + i + ".")
				else: 
					print("You might also like this subreddit: " + j + ".")	

					
#Natural language processing for posts, tweets etc. 
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
	
def flatten(list):
  for i in list:
    for j in i:
      yield j
					
def filterWords(text):
	data = text
	stopWords = set(stopwords.words('german'))
	tokenizer = RegexpTokenizer(r'\w+')
	words = tokenizer.tokenize(data)
	wordsFiltered = []

	for w in words: 
		if w not in stopWords: 
			wordsFiltered.append(w)
			
	wordsForRec = unique_list(wordsFiltered)
	return wordsForRec
	
def analyzePosts(): 
	userWordsList = []
	for i in post_messages: 
		userWordsList.append(filterWords(str(i)))
		
	flattenWordsList = flatten(userWordsList)
	countWords = Counter(list(flattenWordsList))
	return countWords
	
#print(get_jaccard_sim("Will Smith", "Will Smith"))
#print(get_cosine_sim("I am Will Smith", "Do you want to be Will Smith?"))
#print(fuzz.partial_token_set_ratio("mouse","house"))
#recommend(likes, subreddits)

#print(BeautifulSoup(str(post_messages[6]),features="html.parser"))
#for row in likes: 
#	print(row[0])
#print(analyzePosts())
print(groups_name)
#for post in post_messages: 
#	print(post[0])


