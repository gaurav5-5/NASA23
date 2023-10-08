import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)


# Sqlite3 code
DATABASE = 'data/userip.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
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


def update_db(req, table=None):
    if table is not None:
        if table == 'report':
            query_db(
                f"CREATE TABLE IF NOT EXISTS {table} (message TEXT)")
        else:
            query_db(
                f"CREATE TABLE IF NOT EXISTS {table} (name TEXT, email TEXT, feedback TEXT)")

        # Insert data into database
        if table == 'feedback':
            query_db(
                    f"INSERT INTO {table} (name, email, feedback) VALUES (?, ?, ?)",
                    (req.form.get('fd-name'), req.form.get('fd-email'), req.form.get('fd-message')), commit=True)
        elif table == 'report':
            query_db(
                    f"INSERT INTO {table} (message) VALUES (?)",
                    (req.form.get('rprt-message')), commit=True)





# app routes
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Fire Forecasters')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        if 'fd-message' in request.form:
            update_db(request, table='feedback')
            return render_template('feedback.html', title='Feedback')
        elif 'rprt-message' in request.form:
            update_db(request, table='report')
            return render_template('index.html', title='Fire Forecasters')
        
    return render_template('feedback.html', title='Feedback')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About')


@app.route('/protocol', methods=['GET', 'POST'])
def protocol():
    return render_template('protocol.html', title='Protocol')


if __name__ == '__main__':
    app.run(debug=True)
