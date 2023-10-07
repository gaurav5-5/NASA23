import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)


# Sqlite3 code
FEEDBACK = 'data/feedback.db'
REPORT = 'data/report.db'

def get_db(db_path):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(db_path,query, args=(), one=False, commit=False):
    cur = get_db(db_path).execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if commit:
        get_db(db_path).commit()
    return (rv[0] if rv else None) if one else rv



# app routes
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Fire Forecasters')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        if 'rprt-name' in request.form:
            na = request.form.get('rprt-name')
            em = request.form.get('rprt-email')
            msg = request.form.get('rprt-message')
            print(na,em,msg)

            # check if table exists
            query_db(REPORT,
                "CREATE TABLE IF NOT EXISTS feedback (name TEXT, email TEXT, feedback TEXT)")

            # Insert data into database
            query_db(REPORT,
                     "INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)",
                     (na, em, msg), commit=True)
            
            # flash('Reported Successfully!', category='success')

            # return render_template('feedback_success.html', title='Contact Us!')
        
        else:
            na = request.form.get('fd-name')
            em = request.form.get('fd-email')
            msg = request.form.get('fd-message')
            print(na,em,msg)

            # check if table exists
            query_db(FEEDBACK,
                "CREATE TABLE IF NOT EXISTS feedback (name TEXT, email TEXT, feedback TEXT)")

            # Insert data into database
            query_db(FEEDBACK,
                    "INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)",
                    (na, em, msg), commit=True)
            
            # flash('Thank you for your feedback!', category='success')
            

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
