from flask import Flask, redirect, render_template, request, session, Response, url_for
import flask
import os
import APISync
from service import *
import dash
import pandas as pd
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq

df = pd.read_csv('data.csv')
mean_score_percentage = df['score_percentage'].mean()
application = flask.Flask(__name__)
application.config['SESSION_TYPE'] = 'memcached'
application.config['SECRET_KEY'] = 'super secret key boy'
user_service = UserService()
username = ""
app = dash.Dash(
    __name__,
    server=application,
    routes_pathname_prefix='/dashboard/'
)


@application.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('progress.html')


def get_username():
    return username


@application.route('/api_sync')
def api_sync():
    def eventStream():
        if APISync.sync_with_api():
            yield "data:{}\n\n".format("done")

    return Response(eventStream(), mimetype='text/event-stream')


@application.route('/login', methods=['POST'])
def do_login():
    error = None
    if request.method == 'POST':
        if not user_service.correct_user(request.form['username']):
            error = 'Invalid Username'
        elif not user_service.correct_log_in(request.form['username'], request.form['password']):
            error = "Invalid Password"
        elif user_service.correct_log_in(request.form['username'], request.form['password']):
            session['logged_in'] = True
            global username
            username = request.form['username']
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
            user_service.create(request.form['username'], request.form['password'], request.form['api'])
            print(len(request.form['username']))
            return render_template('login.html')
        else:
            error = "All fields must be filled out"
    return render_template("signup.html", error=error)


@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


#
# This separates the flask from the dash.
#

# dash gauge showing the average score percentage
score_gauge = html.Div([
    daq.Gauge(
        id='my-gauge',
        showCurrentValue=True,
        units="%",
        color={"gradient": True, "ranges": {"red": [0, 10], "yellow": [10, 20], "green": [20, 100]}},
        value=mean_score_percentage,
        label='Default',
        max=100,
        min=0,
    ),
], style={'border-width': '5px', 'border-style': 'solid', 'width': '50%', 'margin-left': '30%', 'margin-top': '10%'})

# title of the sidebar
sidebar_header = html.Div([
    dbc.Row(html.Div('Dashboard', className="active", style={'padding': '15%'}), className="active")
])

# sidebar of the homepage
sidebar = html.Div([
    sidebar_header,
    dbc.Row(html.A('haha1', style={'padding': '15%'})),
    dbc.Row(html.A('haha2', style={'padding': '15%'})),
    dbc.Row(html.A('haha3', style={'padding': '15%'}))
], className="sidebar")

# main layout
app.layout = html.Div([
    sidebar,
    score_gauge
], style={'display': 'flex', 'width': '100%', 'height': '100%'})

if __name__ == "__main__":
    application.secret_key = os.urandom(12)
    application.run(debug=True)
