from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def start(name=None):
    return render_template('start.html', name=name)

#if __name__ == '__main__':
#	app.run(host='0.0.0.0')