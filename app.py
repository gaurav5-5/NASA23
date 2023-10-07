from flask import Flask, render_template, request

app = Flask(__name__)





@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('nav'):
            return render_template('feedback.html', title='Contact Us!')
    else:
        return render_template('index.html', title='Fire Forecasters')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
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
