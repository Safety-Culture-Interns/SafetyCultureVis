from flask import Flask, flash, redirect, render_template, request, session, abort, Response, url_for
import os
import time
from service import *

application = Flask(__name__)


@application.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@application.route('/login', methods=['POST'])
def do_login():
    error = None
    if request.method == 'POST':
        if not UserService().correct_user(request.form['username']):
            error = 'Invalid Username'
        elif not UserService().correct_log_in(request.form['username'], request.form['password']):
            error = "Invalid Password"
        elif UserService().correct_log_in(request.form['username'], request.form['password']):
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@application.route('/go_to_signup', methods=['POST'])
def direct_to_signup():
    return render_template('signup.html')


@application.route('/signup', methods=['POST'])
def signup():
    error = None
    if request.method == 'POST':
        if len(request.form['username']) > 0 and len(request.form['password']) > 0 and len(request.form['api']) > 0:
            UserService().create(request.form['username'], request.form['password'], request.form['api'])
            print(len(request.form['username']))
            return render_template('login.html')
        else:
            error = "All fields must be filled out"
    return render_template("signup.html", error=error)


@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@application.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(round(x)) + "\n\n"
            x = x + 0.2
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    application.secret_key = os.urandom(12)
    application.run(debug=True)
