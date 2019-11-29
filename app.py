from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, Response, url_for
import os
# import Constructor
import time

app = Flask(__name__)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"


@app.route('/login', methods=['POST'])
def do_admin_login():
    return redirect(url_for('loading'))


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@app.route('/progress')
def progress():
    def generate():
        x = 0

        while x <= 100:
            yield "data:" + str(round(x)) + "\n\n"
            x = x + 0.2
            time.sleep(0.5)

    return Response(generate(), mimetype='text/event-stream')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
