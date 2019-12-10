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
import dash_core_components as dcc

application = flask.Flask(__name__)
application.config['SESSION_TYPE'] = 'memcached'
application.config['SECRET_KEY'] = 'super secret key boy'
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


@application.route('/api_sync')
def api_sync():
    worked = APISync.sync_with_api()
    if worked:
        return redirect(url_for('/dashboard/'), Response=None)


@application.route('/login', methods=['POST'])
def do_login():
    error = None
    if request.method == 'POST':
        if not UserService().correct_user(request.form['username']):
            error = 'Invalid Username'
        elif not UserService().correct_log_in(request.form['username'], request.form['password']):
            error = "Invalid Password"
        elif UserService().correct_log_in(request.form['username'], request.form['password']):
            session['logged_in'] = True
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


#
# This separates the flask from the dash.
#

df = pd.read_csv('data.csv')
mean_score_percentage = df['score_percentage'].mean()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

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
], style={'border-width': '5px', 'border-style': 'solid', 'width': '50%', 'margin-left': '30%',
          'margin-top': '10%'})

# title of the sidebar
sidebar_header = html.Div([
    dbc.Row(html.Div('Dashboard', className="active", style={'padding': '15%', 'width': '100%'}),
            className="active")
])

# sidebar of the homepage
sidebar = html.Div([
    sidebar_header,
    dbc.Row(dcc.Link('Go to Page 1', href='/page-1', style={'padding': '15%', 'display': 'block', 'width': '100%',
                                                            'color': 'black', 'text-decoration': 'none'})),
    dbc.Row(dcc.Link('Go to Page 2', href='/page-2', style={'padding': '15%', 'display': 'block', 'width': '100%',
                                                            'color': 'black', 'text-decoration': 'none'})),
    dbc.Row(dcc.Link('Go to Page 3', href='/page-3', style={'padding': '15%', 'display': 'block', 'width': '100%',
                                                            'color': 'black', 'text-decoration': 'none'}))
], className="sidebar")

index_page = html.Div([
    sidebar,
    score_gauge,
], style={'display': 'flex', 'width': '100%', 'height': '100%'})

page_1_layout = html.Div([
    dcc.Link('Go back to home', href='/'),
])

page_2_layout = html.Div([
    dcc.Link('Go back to home', href='/')
])

page_3_layout = html.Div([
    dcc.Link('Go back to home', href='/')
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page


if __name__ == "__main__":
    application.secret_key = os.urandom(12)
    application.run(debug=True)
