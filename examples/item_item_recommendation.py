from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords
import nltk
#nltk.download('stopwords')
import itertools
import psycopg2
import json
import pickle


conn = psycopg2.connect(database = "postgres", user = "postgres", password = "326935", host = "localhost", port = "5432")
cursor = conn.cursor()

#Get the subreddit data
def get_subreddits(): 
    cursor.execute("SELECT title, title, display_name, advertiser_category, public_description FROM reddit_recommender.subreddits")
    subreddits = cursor.fetchall()
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

def compareSubreddits_bck(subreddit1, subreddit2): 
    subreddit1_pre = preprocess(subreddit1[1:])
    subreddit2_pre = preprocess(subreddit2[1:])
    similarity_score = get_jaccard_sim(subreddit1_pre, subreddit2_pre)
    return similarity_score

def compareSubreddits(subreddit1, subreddit2): 
    subreddit1_pre = preprocess(subreddit1[1:])
    subreddit2_pre = subreddit2[1:]
    similarity_score = get_jaccard_sim(subreddit1_pre, subreddit2_pre)
    return similarity_score

def search_recommendations_bck(user_subs, all_subreddits):
    best_matches = []
    for sub in user_subs:
        result = []
        best_match = 0.0
        sub_id = sub[0]
        match_id = 'id'
        for subreddit in all_subreddits:
            print(subreddit)
            score = compareSubreddits_bck(sub, subreddit)
            if(score > best_match and score < 1.0):
                best_match = score
                match_id = subreddit[0]
        result.append(best_match)
        result.append(sub_id)
        result.append(match_id)
        best_matches.append(result)        
    return best_matches

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
            result.append(best_match)
            result.append(sub_id)
            result.append(match_id)
            best_matches.append(result)        
    return best_matches

def append_subreddits_to_file(subreddits):
    all = []
    with open("../app/output_subreddits_words_list.pkl", "wb") as fp:
        for sub in subreddits:
            liste = preprocess(sub)
            liste.insert(0, sub[0])
            all.append(liste)
            #flattenWordsList.append(preprocess(sub))
        pickle.dump(all, fp)
    fp.close()

    
#alt
subreddits = get_subreddits()
user_subs = subreddits[100:105]
result = search_recommendations(user_subs)
print(result)
#append_subreddits_to_file(subreddits)


#with open ("../app/output_subreddits_words_list.pkl", "rb") as fp:
#    itemlist = pickle.load(fp)
#    print(itemlist)
                
cursor.close()
