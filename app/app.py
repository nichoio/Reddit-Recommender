import json
import os

from flask import Flask, abort, jsonify, redirect, render_template, request

from . import reddit_subscriptions as rs
from . import commands as cmd
from . import item_item_recommendation as iir
from . import loaduser as lu
from . import get_words_list as gwl
from ._facebook import api as fbapi

REDDIT_CLIENT_ID = ''
REDDIT_PERMISSIONS = 'mysubreddits+identity+history'
FACEBOOK_APP_ID = ''
FACEBOOK_PERMISSIONS = 'public_profile,email,user_likes,user_posts,user_gender,user_events,groups_access_member_info'

OAUTH_REDDIT = 'https://www.reddit.com/api/v1/authorize?state=123456&duration=permanent&scope={}&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect-reddit&client_id={}&response_type=code'.format(REDDIT_PERMISSIONS, REDDIT_CLIENT_ID)
OAUTH_FB = 'https://www.facebook.com/v3.2/dialog/oauth?client_id={}&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect-facebook&state=6548211&scope={}&response_type=token'.format(FACEBOOK_APP_ID, FACEBOOK_PERMISSIONS)

VAR_STORE = '/tmp/usertemp.json'
SUBS_TXT = '/app/output_subreddits.txt'
SUBS_SCREENNAME_TXT = '/app/output_subreddit_screen_name.txt'

REC_AMOUNT_SOCIAL = 99  # output of recommendations
# REC_AMOUNT_SUBS = 10  # output of recommendations based on subscriptions
REC_ABO_MIN = 0  # amount of subscriptoins sub must have to be considered (Twitter & FB)

app = Flask(__name__)


@app.route('/')
def start(name=None):
    return render_template('start.html', name=name)


@app.route('/store-initial')
def store_initial(name=None):
    params = _get_params(request.args)
    try:
        os.remove(VAR_STORE)
    except FileNotFoundError:
        pass  # ignore non existing file
    _update_json(params)
    return redirect('/userdata')


@app.route('/userdata')
def userdata(name=None):
    if _read_json('use-twitter'):
        return redirect('/twitter', code=302)
    else:
        if _read_json('use-facebook'):
            return redirect('/auth-facebook', code=302)
        else:
            if _read_json('use-reddit'):
                return redirect('/auth-reddit', code=302)
            else:
                return redirect('/load-user', code=302)


@app.route('/twitter')
def twitter(name=None):
    return render_template('twitter.html')


@app.route('/redirect-twitter')
def redirect_twitter(name=None):
    _update_json({'name-twitter': request.args.get('twittername'), 'use-twitter': False})
    return redirect('/userdata')


@app.route('/redirect-facebook')
def redirect_facebook(name=None):  # parse masked query string through js
    return '''  <script type="text/javascript">
                var token = window.location.href.split("access_token=")[1]; 
                window.location = "/facebook-token/" + token;
            </script> '''


@app.route('/facebook-token/<token>/')
def facebook_token(token):
    access_token = token.split('&')[0]
    _update_json({
        'token-facebook': access_token,
        'use-facebook': False,
        'id-facebook': fbapi.get_u_id(access_token)})
    return redirect('/userdata')


@app.route('/auth-facebook')
def auth_facebook(name=None):
    return redirect(OAUTH_FB, code=302)


@app.route('/auth-reddit')
def auth_reddit(name=None):
    return redirect(OAUTH_REDDIT, code=302)


@app.route('/redirect-reddit')
def redirect_reddit(name=None):
    token_code = request.args.get('code')
    refresh_token = rs.gen_praw_object().auth.authorize(token_code)
    reddit_name = rs.get_u_id(refresh_token)
    _update_json({
        'token-reddit': refresh_token,
        'name-reddit': reddit_name,
        'use-reddit': False})
    return redirect('/load-user', code=302)  # skip /userdata route


@app.route('/load-user')
def load_user(name=None):
    with open(VAR_STORE, mode='r') as f:
        user_data = json.load(f)

    lu.load_user(
        user_data['name'],
        TWITTER_SCREEN_NAME=user_data['name-twitter'] if 'name-twitter' in user_data else None,
        FACEBOOK_U_ID=user_data['id-facebook'] if 'id-facebook' in user_data else None,
        REDDIT_USER_NAME=user_data['name-reddit'] if 'name-reddit' in user_data else None)
    #return redirect('/trigger-jobswindow.location.href = "you want to redirect";')
    return redirect('/trigger-jobs')


@app.route('/trigger-jobs')
def trigger_jobs(name=None):
    twitter_name = _read_json('name-twitter')
    fb_token = _read_json('token-facebook')
    reddit_token = _read_json('token-reddit')

    if twitter_name:
        job_param = 'twitter_user={}'.format(twitter_name)
        if cmd.run_job('LoadTwitterData', job_param) is False:
            abort(500)

    if fb_token:
        job_param = 'access_token={}'.format(fb_token)
        if cmd.run_job('facebookAPIexample', job_param) is False:
            abort(500)

    if reddit_token:
        rs.save_subs(reddit_token)
        if cmd.run_trafo('reddit_subscriptions') is False:
            abort(500)
    
    if twitter_name is None and fb_token is None:  # go to reddit recom.
        return redirect('/recommendations-subs', code=302)
         
    return redirect('/recommendations', code=302)


@app.route('/recommendations')
def recommendations(name=None):
    path_userwords = '/tmp/words_user.json'
    path_output = '/tmp/recommendations.txt'
    sub_recs = True if _read_json('name-reddit') else False

    gwl.start(_read_json('name'), path_userwords)  # creates words_user.json
    cmd.run_jar(
        'red_rec',
        path_userwords,
        SUBS_TXT,
        SUBS_SCREENNAME_TXT,
        path_output,
        str(REC_ABO_MIN),
        'true',  # use weight
        'false',  # false = std Jaccard
        '0')  # edit distance <= arg

    with open(path_output) as f:
        recs = json.load(f)[:REC_AMOUNT_SOCIAL]

    return render_template(
        'recommendations.html',
        rows=recs,
        cols=('subreddit', 'value'),
        sub_recs=sub_recs,
        first_results=True)


@app.route('/recommendations-subs')
def recommendations_subs(name=None):
    recs = iir.recommend(_read_json('name-reddit'))

    return render_template(
        'recommendations.html',
        rows=recs,
        cols=('subreddit', 'value'),
        sub_recs=False,
        first_results=False)


def _get_params(request_args):
    t = True if request_args.get('t') == 'y' else False
    f = True if request_args.get('f') == 'y' else False
    r = True if request_args.get('r') == 'y' else False
    name = request_args.get('name')
    return {'use-twitter': t, 'use-facebook': f, 'use-reddit': r, 'name': name}


def _update_json(new_data):
    # primitive key-value store - write
    old = None

    try:
        with open(VAR_STORE, mode='r') as f:
            try:
                old = json.load(f)
            except json.decoder.JSONDecodeError:
                pass  # ignore prev. empty file
    except FileNotFoundError:
        pass  # ignore non existing file

    with open(VAR_STORE, mode='w') as f:
        if old:
            json.dump({**old, **new_data}, f)
        else:
            json.dump(new_data, f)


def _read_json(key):
    # primitive key-value store - read
    with open(VAR_STORE, mode='r') as f:
        data = json.load(f)
        try:
            return data[key]
        except KeyError:
            return None
