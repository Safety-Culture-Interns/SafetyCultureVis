import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import datetime

current_date = datetime.datetime.now()
previous_date = current_date + datetime.timedelta(-29)

location_map = html.Div([
    html.Div(children=[
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=previous_date.date(),
            end_date=current_date.date()
        )], style={'width': '35%', 'display': 'inline-block', 'text-align': 'center', 'margin': '0 auto'}),
    html.Div(children=[
        dcc.Dropdown(options=[
            {'label': 'Audit Created', 'value': 'Created_at'},
            {'label': 'Audit Modified', 'value': 'Modified_at'},
            {'label': 'Date Completed', 'value': 'completed_at'}
        ], value='Created_at',
            id='date-sort')], style={'width': '100%', 'display': 'inline-block', 'text-align': 'center', 'margin': '0 auto'}),
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
], style={'width': '100%', 'display': 'flex', 'flex-wrap': 'wrap', 'margin-top': '10px'})

score_gauge = html.Div([
    daq.Gauge(
        id='my-gauge',
        showCurrentValue=True,
        units="%",
        color={"gradient": True, "ranges": {"red": [0, 10], "yellow": [10, 20], "green": [20, 100]}},
        label='Default',
        max=100,
        min=0,
    ),
], style={'border-width': '5px', 'border-style': 'solid', 'width': '85%', 'position': 'relative'})

# title of the sidebar
sidebar_header = html.Div([
    dbc.Row(html.Div('Dashboard', className="active", style={'padding': '12%'}), className="active")
])

# sidebar of the homepage
sidebar = html.Div([
    sidebar_header,
    dbc.Row(html.A('haha1', style={'padding': '15%'})),
    dbc.Row(html.A('haha2', style={'padding': '15%'})),
    dbc.Row(html.A('haha3', style={'padding': '15%'}))
], className="sidebar", style={'position': 'relative', 'height': 'auto', 'display': 'block'})

# main layout
layout = html.Div([
    sidebar,
    score_gauge, location_map
], style={'display': 'flex', 'flex-wrap': 'wrap', 'width': '100%', 'height': '100%'})
