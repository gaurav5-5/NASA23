import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)


# Sqlite3 code
FEEDBACK = 'data/feedback.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(FEEDBACK)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False, commit=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if commit:
        get_db().commit()
    return (rv[0] if rv else None) if one else rv



# app routes
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Fire Forecasters')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        na = request.form
        # em = request.form['feedback']['email']
        # fd = request.form['feedback']['message']
        print(na)
        # check if table exists
        # query_db(
        #     "CREATE TABLE IF NOT EXISTS feedback (name TEXT, email TEXT, feedback TEXT)")

        # # Insert data into database
        # query_db("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)",
        #          (na, em, fd), commit=True)

        return render_template('feedback_success.html', title='Contact Us!')
    return render_template('feedback.html', title='Feedback')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@app.route('/protocol', methods=['GET', 'POST'])
def protocol():
    return render_template('protocol.html', title='Protocol')


if __name__ == '__main__':
    app.run(debug=True)
