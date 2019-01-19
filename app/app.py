import sqlalchemy
from flask import Flask, redirect, render_template, request

from . import reddit_subscriptions as rs
from . import pdi

REDDIT_CLIENT_ID = 'hn7qi5bxIVgXBg'
REDDIT_PERMISSIONS = 'mysubreddits+identity+history'
DB_PATH = 'mysql+pymysql://root:password@reddit-mysql/reddit_recommender'
OAUTH_REDDIT = 'https://www.reddit.com/api/v1/authorize?state=123456&duration=permanent&scope={}&redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fredirect-reddit&client_id={}&response_type=code'.format(REDDIT_PERMISSIONS, REDDIT_CLIENT_ID)

app = Flask(__name__)
db = sqlalchemy.create_engine(DB_PATH)


@app.route('/')
def start(name=None):
    return render_template('start.html', name=name)


@app.route('/auth-reddit')
def auth_reddit(name=None):
    return redirect(OAUTH_REDDIT, code=302)


@app.route('/redirect-reddit')
def redirect_reddit(name=None):
    token_code = request.args.get('code')
    refresh_token = rs.gen_praw_object().auth.authorize(token_code)
    rs.save_subs(refresh_token)
    job_result = pdi.run_trafo('reddit_subscriptions.ktr')
    return job_result  # 0 = success


@app.route('/db-test')
def db_test():
    with db.engine.connect() as con:
        result = con.execute('SELECT COUNT(*) AS count FROM subreddits;')
    return str(result.fetchone()['count'])
