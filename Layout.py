# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# df = pd.read_csv('test.csv')

df = pd.read_csv('https://raw.githubusercontent.com/matthew-lewandowski/SafetyCultureVis/audit/data.csv')

scl = [0, "rgb(150,0,90)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
      [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
      [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colours = {
    'background': '#8D8C8B',
    'text': '#fff'
}


app.layout = html.Div([
    html.Label('Comparison'),
    dcc.Dropdown(
        options=[
            {'label': 'Compare Audits', 'value': 'audit'},
            {'label': 'Compare Templates', 'value': 'template'}
        ],
        value='audit',
    ),
    html.Label('Graph Type'),
    dcc.Dropdown(
        options=[
            {'label': 'Bar Graph', 'value': 'bar'},
            {'label': 'Line Graph', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'}
        ],
        value='bar',
    ),
    html.Label('X Axis'),
    dcc.Dropdown(
        options=[
            {'label': 'Score', 'value': 'score'},
            {'label': '', 'value': ''}
        ],
        value='score',
        id='xaxis'
    ),
    html.Label('Y Axis'),
    dcc.Dropdown(
        options=[
            {'label': 'Score Percentage', 'value': 'percent'},
            {'label': '', 'value': ''}
        ],
        value='percent',
        id='yaxis'
    ),
    dcc.Graph(
        id='map'
    )
])


@app.callback(
    dash.dependencies.Output("map", "figure"),
    [dash.dependencies.Input("xaxis", "value")]
)
def update_figure(selected):
    trace = go.Scattergeo(
    lat=df['longitude'],
    lon=df['latitude'], #change later, wrong way around in csv right now
    text=df['score_percentage'].astype(str) + ' percent',
    marker=dict(
        color=df['score_percentage'],
        colorscale=scl,
        reversescale=True,
        opacity=0.4,
        size=5,
        colorbar=dict(
            titleside="right",
            outlinecolor="rgba(68, 68, 68, 0)",
            ticks="outside",
            showticksuffix="last",
            dtick=0.1
        )
    ))
    return {'data': [trace], 'layout': go.Layout(geo=dict(
        # height=500,
        # width=1000,
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
    ), width=1000, height=1000, title='map', margin=go.layout.Margin(l=5, r=5, b=5, t=5, pad=0))}


if __name__ == '__main__':
    app.run_server(debug=True)
