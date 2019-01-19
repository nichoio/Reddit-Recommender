import json

import praw

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:5000/redirect-reddit'
USER_AGENT = 'reddit-recommender:v1.2'
JSON_PATH = '/tmp/reddit_user.json'


def gen_praw_object():
    return praw.Reddit(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT,
                redirect_uri=REDIRECT_URI)


def group_by(list_):
    dict_ = dict()
    for l in list_:
        if l in dict_:
            dict_[l] += 1
        else:
            dict_[l] = 1
    return dict_


def save_subs(refresh_token):
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT,
                         refresh_token=refresh_token)

    user = reddit.user.me()
    subscribed = [s.display_name for s in list(reddit.user.subreddits(limit=None))]
    subscribed_data = [{
        'display_name': s,
        'user_name': user.name,
        'subscribed': 1}
        for s in subscribed]

    comments_subs = [c.subreddit.display_name for c in user.comments.new()]
    comment_freq = group_by(comments_subs)

    # get amount of comments for all subscribed subs
    for s in subscribed_data:
        if s['display_name'] in comment_freq:
            s['comments'] = comment_freq[s['display_name']]
        else:
            s['comments'] = 0

    # add subs with comments but no subscription
    commented_no_sub = set(list(comment_freq.keys())) - set(subscribed)
    commented_data = [{
        'display_name': c,
        'user_name': user.name,
        'subscribed': 0,
        'comments': comment_freq[c]}
        for c in commented_no_sub]

    subscribed_data.extend(commented_data)

    with open(JSON_PATH, 'w') as outfile:
        json.dump(subscribed_data, outfile)
