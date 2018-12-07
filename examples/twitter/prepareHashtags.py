import json
import sys

with open(sys.argv[1]+'Tweets.json') as json_data:
	data = json.load(json_data)
	for tweet in data:
            for hashtag in tweet['hashtags']:
                if 'text' in hashtag:
                    tweet['hashtags'].append({u'withId':{u'tweetId':tweet['id'],u'text':hashtag['text']}})
            #tweet['hashtags'].append({u'tweetId':tweet['id']})
            #print(tweet['hashtags'])
with open(sys.argv[1]+'Hashtags.json', 'w') as file:
        json.dump(data, file)
