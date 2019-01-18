import sqlalchemy
from flask import Flask, render_template

DB_PATH = 'mysql+pymysql://root:password@reddit-mysql/reddit_recommender'

app = Flask(__name__)
db = sqlalchemy.create_engine(DB_PATH)


@app.route('/')
def start(name=None):
    return render_template('start.html', name=name)

@app.route('/db-test')
def db_test():
	with db.engine.connect() as con:
		result = con.execute('SELECT COUNT(*) AS count FROM subreddits;')
	return str(result.fetchone()['count'])
