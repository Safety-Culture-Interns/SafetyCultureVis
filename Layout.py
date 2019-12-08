# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime as dt
import string

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('data.csv')

# df = pd.read_csv('https://raw.githubusercontent.com/matthew-lewandowski/SafetyCultureVis/audit/data.csv')

values = list(df.columns.values)

scl = [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
      [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
      [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colours = {
    'background': '#8D8C8B',
    'text': '#fff'
}


def update_string(attribute):
    """Splits strings by underscores and capitalises each word"""
    return string.capwords(' '.join(attribute.split('_')), ' ')


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='map-tab', children=[
        dcc.Tab(label='Map Tab', value='map-tab', children=[
            html.H3('Map'),
            html.Div(children=[
                dcc.DatePickerRange(
                    id='date-picker-range',
                    # start_date_placeholder_text='Select Start date',
                    # end_date_placeholder_text='Select End date'
                    start_date=dt(2017, 12, 25),
                    end_date=dt(2018, 2, 1)
                )], style={'width': '25%', 'display': 'inline-block'}),
            html.Div(children=[
                dcc.Dropdown(options=[
                    {'label': 'Audit Created', 'value': 'audit_created_at_date'},
                    {'label': 'Audit Modified', 'value': 'audit_modified_at_date'},
                    {'label': 'Date Completed', 'value': 'date_completed_date'}
                ], value='audit_created_at_date',
                    id='date-sort')], style={'width': '25%', 'display': 'inline-block'}),
            dcc.Graph(
                id='map'
            )]),
        dcc.Tab(label='Graph Tab', value='graph-tab', children=[
            html.H3('Graph'),
            html.Div(children=[
                html.Label('Graph Type'),
                dcc.Dropdown(
                    options=[
                        {'label': 'Bar Graph', 'value': 'bar'},
                        {'label': 'Line Graph', 'value': 'line'},
                        {'label': 'Scatter Plot', 'value': 'scatter'}
                    ],
                    value='scatter',
                    id='graph-type'
                )], style={'width': '25%', 'display': 'inline-block'}),
            html.Div(children=[
                html.Label('X Axis'),
                dcc.Dropdown(
                    options=[
                        {'label': update_string(i), 'value': i} for i in values
                    ],
                    value='score',
                    id='xaxis'
                )], style={'width': '25%', 'display': 'inline-block'}),
            html.Div(children=[
                html.Label('Y Axis'),
                dcc.Dropdown(
                    options=[
                        {'label': update_string(i), 'value': i} for i in values
                    ],
                    value='score_percentage',
                    id='yaxis'
                )], style={'width': '25%', 'display': 'inline-block'}),
            html.Div(children=[
                dcc.Graph(
                    id='chart'
                )
            ])
        ]),
        html.Div(id='tabs-content')
    ])
])


@app.callback(Output('map', 'figure'),
              [Input('date-picker-range', 'start_date'),
               Input('date-picker-range', 'end_date'),
               Input('date-sort', 'value')])
def select_date(start_date, end_date, sorting_method):
    """Displays map points alongside score percentage based on dates selected and sorting method"""
    df[sorting_method] = pd.to_datetime(df[sorting_method])
    mask = df[sorting_method].between(start_date, end_date)
    print(mask)
    trace = go.Scattergeo(
        lat=df['latitude'].get(mask),
        lon=df['longitude'].get(mask),
        text=df['score_percentage'].astype(str) + ' percent',
        marker=dict(
            color=df['score_percentage'],
            colorscale=scl,
            reversescale=True,
            opacity=0.7,
            size=7,
            colorbar=dict(
                lenmode='fraction', len=0.47, thickness=40,
                titleside="right",
                outlinecolor="rgba(68, 68, 68, 0)",
                ticks="outside",
                showticksuffix="last",
                dtick=1
            )
        ))
    return {'data': [trace], 'layout': go.Layout(geo=dict(
        scope='world',
        showland=True,
        landcolor="rgb(212, 212, 212)",
        subunitcolor="rgb(255, 255, 255)",
        countrycolor="rgb(255, 255, 255)",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
        showsubunits=True,
        showcountries=True,
        resolution=50,
        projection=dict(
            type='equirectangular',
        ),
        lonaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            range=[-180.0, 180.0],
            dtick=5
        ),
        lataxis=dict(
            showgrid=True,
            gridwidth=0.5,
            range=[-180.0, 180.0],
            dtick=5
        )
    ), width=1000, height=1000, title='map', margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=50))}


@app.callback(
    Output('chart', 'figure'),
    [Input('graph-type', 'value'),
     Input('xaxis', 'value'),
     Input('yaxis', 'value')]
)
def update_figure(graph_type, x_value, y_value):
    """Updates the graph based on what graph type is selected and parameters selected"""
    if graph_type == 'scatter':
        traces = [dict(
            x=df[x_value],
            y=df[y_value],
            # text=['score_percentage'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )]
        return {
            'data': traces,
            'layout': dict(
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
            )
        }
    elif graph_type == 'line':
        trace = [go.Scatter(x=df[x_value], y=df[y_value], mode='lines',
                            marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, )]
        return {"data": trace,
                "layout": go.Layout(title="Line Graph",
                                    colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
                                    yaxis={"title": ""}, xaxis={"title": ""})}
    elif graph_type == 'bar':
        trace = go.Bar(x=df[x_value], y=df[y_value], name='')
        return {
            'data': [trace],
            'layout': go.Layout(title='Bar Graph',
                                colorway=["#EF963B", "#EF533B"], hovermode="closest",
                                xaxis={'title': "", 'titlefont': {'color': 'black', 'size': 14},
                                       'tickfont': {'size': 9, 'color': 'black'}},
                                yaxis={'title': "",
                                       'titlefont': {'color': 'black', 'size': 14, },
                                       'tickfont': {'color': 'black'}})}


if __name__ == '__main__':
    app.run_server(debug=True)
