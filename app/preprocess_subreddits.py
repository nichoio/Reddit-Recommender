from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
import itertools
import MySQLdb
import json
import pickle

#Get the subreddit data
def get_subreddits(): 
    conn = MySQLdb.connect(host="reddit-mysql", user="root", passwd = "password", db = "reddit_recommender")
    cursor = conn.cursor()
    cursor.execute("SELECT title, title, display_name, advertiser_category, public_description from reddit_recommender.subreddits where subscribers > 1000;")
    subreddits = cursor.fetchall()
    cursor.close()
    return subreddits 
    
def flatten(list):
  for i in list:
    for j in i:
      yield j

def get_jaccard_sim(subreddit1, subreddit2):
    a = set(subreddit1)
    b = set(subreddit2)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def filterWords(text):
    stopWords = set(stopwords.words('english'))
    unwantedWords = ['None','Impressum', 'impressum', 'r']
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)
    wordsFiltered = []
    wordsFiltered = [word for word in words if word not in stopWords]
    removeUnwanted = [word for word in wordsFiltered if word not in unwantedWords]
    return removeUnwanted
    
def preprocess(subreddits):
    subredditWordsList = []
    for subreddit in range(len(subreddits)):
        for word in subreddits: 
            subredditWordsList.append(filterWords(str(word)))
        flattenWordsList = list(set(flatten(subredditWordsList))) 
    return flattenWordsList

def append_subreddits_to_file():
    subreddits = get_subreddits()
    all = []
    with open("../app/output_subreddits_words_list.pkl", "wb") as fp:
        for sub in subreddits:
            liste = preprocess(sub)
            liste.insert(0, sub[0])
            all.append(liste)
        pickle.dump(all, fp)
    fp.close()

    
append_subreddits_to_file()
