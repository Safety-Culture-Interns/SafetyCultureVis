import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import datetime
import plotly.graph_objects as go

from flask import session

from . import aggregate_pipelines

current_date = datetime.datetime.now()
previous_date = current_date + datetime.timedelta(-29)
# header bar
header = html.Div([
    html.Div([
        html.Img(src='/dashboard/assets/iauditor-badge.png',
                 style={'height': '60px', 'width': 'auto', 'margin-bottom': '25px'})
    ], className='one-third column'),
    html.Div([
        html.H3('Safety Culture Dashboard'),
        html.H5('Your overview')
    ], className='one-half column', id='title'),
    html.Div([
        html.A('Logout', href='/auth/logout', className='logout_button')
    ], className='one-third column', style={'text-align': 'right'}),
], className='flex-display', id='header', style={'margin-bottom': '25px'})
# location map and drop downs
location_map = html.Div([
    html.Div([
        html.Div(children=[
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=previous_date.date(),
                end_date=current_date.date(),
                max_date_allowed=current_date.date() + datetime.timedelta(1),
                updatemode='bothdates'
            )], className='pretty_container',
            style={'width': '50%', 'text-align': 'center'}),
        html.Div(children=[],
                 className='pretty_container',
                 style={'width': '50%'}),
    ], style={'display': 'flex'}),
    html.Div([
        dcc.Graph(
            id='map',
            style={'width': '100%'},
            config={
                'displayModeBar': False,
                'autosizable': True,
                'fillframe': True,
                'colorBarPosition': True,
                'titleText': False
            }
        ),
    ], className='pretty_container'),

], id='right-column', className='eight columns')
# the score guage
score_gauge = html.Div([
    dcc.Input(
        id='fake-input',
        value="none",
        type='text',
        style={'display': 'None'}),
    daq.Gauge(
        id='my-gauge',
        value=0,
        showCurrentValue=True,
        units="%",
        color={"gradient": True, "ranges": {"red": [0, 60], "yellow": [60, 80], "green": [80, 100]}},
        label='Account Health',
        max=100,
        min=0,
        style={'color': 'black', 'font-size': '2rem'}
    ),
    html.Div([
        html.Img(src='/dashboard/assets/Feeling-barometer.png',
                 style={'height': '40px', 'width': 'auto', })
    ], className='happyness'),
    html.Div([
        html.H6("Incomplete Audits: 0%", id='total-failed', className='pretty_container five columns',
                style={'margin': '10px auto', 'padding': '15px 0'}
                ),
        html.H6('Complete Audits: 0%', id='total-passed', className='pretty_container five columns',
                style={'margin': '10px auto', 'padding': '15px 0'}),
        html.H6("Avg Audit Score: 0%", id='avg-score', className='pretty_container five columns',
                style={'margin': '10px auto', 'padding': '15px 0'},
                ),
        html.H6('Total Audits: 0', id='total-audits', className='pretty_container five columns',
                style={'margin': '10px auto', 'padding': '15px 0'})
    ], className='inside_pretty_container')
], id='score_guage', className='pretty_container four columns')

# combining into divs
score_graph = html.Div([
    dcc.Graph(id='score-graph',
              config={'displayModeBar': False})
], className='pretty_container six columns')

score_percent_graph = html.Div([
    dcc.Graph(id='score-percent-graph',
              config={'displayModeBar': False})
], className='pretty_container six columns')

duration_graph = html.Div([
    dcc.Graph(id='duration-graph',
              config={'displayModeBar': False})
], className='pretty_container six columns')

audits_graph = html.Div([
    dcc.Graph(id='audits-graph',
              config={'displayModeBar': False})
], className='pretty_container six columns')
# average audit duration and total vs failed audits
audit_duration_failed_audits = html.Div([
    duration_graph,
    audits_graph
], className='flex-display')
# average scores and score percentages
average_scores_percentages = html.Div([
    score_graph,
    score_percent_graph
], className='flex-display')
# map and health bar
map_health_bar = html.Div([
    score_gauge, location_map
], className='flex-display')

# main layout
layout = html.Div([

    header, map_health_bar, average_scores_percentages, audit_duration_failed_audits
], id='mainContainer', style={'display': 'flex', 'flex-wrap': 'wrap', 'width': '100%', 'height': '100%'})
