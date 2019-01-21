import json
import os

import sqlalchemy
from flask import Flask, jsonify, redirect, render_template, request

from . import reddit_subscriptions as rs
from . import pdi
from ._facebook import api as fbapi

REDDIT_CLIENT_ID = ''
REDDIT_PERMISSIONS = 'mysubreddits+identity+history'
FACEBOOK_APP_ID = ''
FACEBOOK_PERMISSIONS = 'public_profile,email,user_likes,user_posts,user_gender,user_events'
OAUTH_REDDIT = 'https://www.reddit.com/api/v1/authorize?state=123456&duration=permanent&scope={}&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect-reddit&client_id={}&response_type=code'.format(REDDIT_PERMISSIONS, REDDIT_CLIENT_ID)
OAUTH_FB = 'https://www.facebook.com/v3.2/dialog/oauth?client_id={}&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect-facebook&state=6548211&scope={}&response_type=token'.format(FACEBOOK_APP_ID, FACEBOOK_PERMISSIONS)
DB_AUTH = 'mysql+pymysql://root:password@reddit-mysql/reddit_recommender'
VAR_STORE = '/tmp/usertemp.json'


app = Flask(__name__)
db = sqlalchemy.create_engine(DB_AUTH)


@app.route('/')
def start(name=None):
    return render_template('start.html', name=name)


@app.route('/store-initial')
def store_initial(name=None):
    params = _get_params(request.args)
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
    #rs.save_subs(refresh_token)
    #job_result = pdi.run_trafo('reddit_subscriptions.ktr')
    return redirect('/load-user', code=302)  # skip /userdata route


@app.route('/load-user')
def load_user(name=None):
    with open(VAR_STORE, mode='r') as f:
        user_data = json.load(f)

    # TODO: call loaduser    
    return redirect('/trigger-jobs')


@app.route('/trigger-jobs')
def trigger_jobs(name=None):
    # TODO: save personal data to DB
    return redirect('/recommendations', code=302)


@app.route('/recommendations')
def recommendations(name=None):
    # TODO: compute recs
    #os.remove(VAR_STORE)
    return render_template('recommendations.html', name=name)


@app.route('/db-test')
def db_test():
    with db.engine.connect() as con:
        result = con.execute('SELECT COUNT(*) AS count FROM subreddits;')
    return str(result.fetchone()['count'])


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
    with open(VAR_STORE, mode='r') as f:
        data = json.load(f)
        return data[key] 
