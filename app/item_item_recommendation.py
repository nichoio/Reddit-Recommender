from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
import itertools
import MySQLdb
import json
import pickle
	
def get_user_subreddits(user_name): 
    conn = MySQLdb.connect(host="reddit-mysql", user="root", passwd = "password", db = "reddit_recommender")
    cursor = conn.cursor()
    cursor.execute("SELECT title, title, display_name, advertiser_category, public_description from reddit_recommender.subreddits where display_name in (select display_name from reddit_recommender.reddit_personal where user_name = '" + reddit_u_id + "');")
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

def compareSubreddits(subreddit1, subreddit2): 
    subreddit1_pre = preprocess(subreddit1[1:])
    subreddit2_pre = subreddit2[1:]
    similarity_score = get_jaccard_sim(subreddit1_pre, subreddit2_pre)
    return similarity_score

def search_recommendations(user_subs):
    best_matches = [] 
    with open ("../app/output_subreddits_words_list.pkl", "rb") as fp:
        itemlist = pickle.load(fp)
        for sub in user_subs:
            result = []
            best_match = 0.0
            sub_id = sub[0]
            match_id = 'id'
            for subreddit in itemlist:
                score = compareSubreddits(sub, subreddit)
                if(score > best_match and score < 1.0):
                    best_match = score
                    match_id = subreddit[0]
            rec_dict = dict(subreddit="Sub", value= 0.0)
            rec_dict.update({'subreddit': match_id})
            rec_dict.update({'value': best_match})
            best_matches.append(rec_dict)  
    with open('item_item_rec.json', 'w') as outfile:
        json.dump(best_matches, outfile)

#pass username here
user_subreddits = get_user_subreddits(user_name)
search_recommendations(user_subreddits)

