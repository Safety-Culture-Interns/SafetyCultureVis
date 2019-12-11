import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import pandas as pd

df = pd.read_csv('api_sync/data.csv')
mean_score_percentage = df['score_percentage'].mean()

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
layout = html.Div([
    sidebar,
    score_gauge
], style={'display': 'flex', 'width': '100%', 'height': '100%'})
