from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 
from fuzzywuzzy import fuzz 
import MySQLdb
import sys
import praw 

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')

connection = MySQLdb.connect(host = "localhost", user="root", passwd = "123+#abc", db = "reddit_recommender")

cursor = connection.cursor()

cursor.execute("select name from likes")

likes = cursor.fetchall()

sublist = [""]
subreddits = ["cronos consulting","All about Samsung","Texel","Walt Disney", "Never mind", "Bill Gates"]
	
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
	

#print(get_jaccard_sim("Will Smith", "Will Smith"))
#print(get_cosine_sim("I am Will Smith", "Do you want to be Will Smith?"))
print(fuzz.partial_token_set_ratio("mouse","house"))
#recommend(likes, subreddits)

#for row in likes: 
#	print(row[0])

cursor.close()