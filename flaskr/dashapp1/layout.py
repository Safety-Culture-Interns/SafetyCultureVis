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

location_map = html.Div([
    html.Div([
        html.Div(children=[
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=previous_date.date(),
                end_date=current_date.date(),
            )], className='pretty_container',
            style={'width': '50%', 'text-align': 'center'}),
        html.Div(children=[
            dcc.Dropdown(options=[
                {'label': 'Audit Created', 'value': 'Created_at'},
                {'label': 'Audit Modified', 'value': 'Modified_at'},
                {'label': 'Date Completed', 'value': 'completed_at'}
            ], value='Created_at',
                id='date-sort')],
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
        color={"gradient": True, "ranges": {"red": [0, 10], "yellow": [10, 20], "green": [20, 100]}},
        label='Default',
        max=100,
        min=0,
    ),

], id='score_guage', className='pretty_container four columns', style={'border-width': '5px', 'border-style': 'solid', 'width': '85%', 'position': 'relative'})

score_graph = html.Div([
    dcc.Graph(id='score-graph')
])

score_percent_graph = html.Div([
    dcc.Graph(id='score-percent-graph')
])

duration_graph = html.Div([
    dcc.Graph(id='duration-graph')
])

audits_graph = html.Div([
    dcc.Graph(id='audits-graph')
])

# title of the sidebar
sidebar_header = html.Div([
    dbc.Row(html.Div('Dashboard', className="active", style={'padding': '12%'}), className="active")
])
# map and health bar
map_health_bar = html.Div([
    score_gauge, location_map
], className='flex-display')

# header bar
header = html.Div([
    html.Div([
        html.Img(src='iauditor-badge.png')
    ], className='one-third column'),
    html.Div([
        html.H1('Safety Culture Dashboard')
    ], className='one-half column', id='title'),
    html.Div([
    ], className='one-third column'),
], className='row flex-display', id='header', style={'margin-bottom': '25px'})

# main layout
layout = html.Div([

    header, map_health_bar, score_graph, score_percent_graph, duration_graph, audits_graph
], id='mainContainer', style={'display': 'flex', 'flex-wrap': 'wrap', 'width': '100%', 'height': '100%'})

