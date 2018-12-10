import json

import praw

CLIENT_ID = ''
CLIENT_SECRET = ''
USER_AGENT = ''
REFRESH_TOKEN = ''

JSON_PATH = 'reddit_user.json'


def group_by(list_):
    dict_ = dict()
    for l in list_:
        if l in dict_:
            dict_[l] += 1
        else:
            dict_[l] = 1
    return dict_


reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     refresh_token=REFRESH_TOKEN)

user = reddit.user.me()
subscribed = [s.display_name for s in list(reddit.user.subreddits(limit=None))]
subscribed_data = [{
    'sub_name': s,
    'user_name': user.name,
    'subscribed': True}
    for s in subscribed]

comments_subs = [c.subreddit.display_name for c in user.comments.new()]
comment_freq = group_by(comments_subs)

# get amount of comments for all subscribed subs
for s in subscribed_data:
    if s['sub_name'] in comment_freq:
        s['comments'] = comment_freq[s['sub_name']]
    else:
        s['comments'] = 0

# add subs with comments but no subscription
commented_no_sub = set(list(comment_freq.keys())) - set(subscribed)
commented_data = [{
    'sub_name': c,
    'user_name': user.name,
    'subscribed': False,
    'comments': comment_freq[c]}
    for c in commented_no_sub]

subscribed_data.extend(commented_data)

with open(JSON_PATH, 'w') as outfile:
    json.dump(subscribed_data, outfile)
