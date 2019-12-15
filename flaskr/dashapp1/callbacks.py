import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from flask import session

from . import aggregate_pipelines

scl = [0, "rgb(242, 51, 242)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
      [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
      [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]


def register_callbacks(app):
    @app.callback(Output('map', 'figure'),
                  [Input('date-picker-range', 'start_date'),
                   Input('date-picker-range', 'end_date'),
                   Input('date-sort', 'value')])
    def select_date(start_date, end_date, sorting_method):
        """Displays map points alongside score percentage based on dates selected and sorting method"""
        df = aggregate_pipelines.get_map_dataframe(session['user_id'])
        values = list(df.columns.values)
        df[sorting_method] = pd.to_datetime(df[sorting_method or 'Created_at'])
        mask = df[sorting_method].between(start_date, end_date)
        trace = go.Scattergeo(
            lat=df['Y'].get(mask),
            lon=df['X'].get(mask),
            text=df['Score'].astype(str) + ' percent',
            marker=dict(
                color=df['Score'],
                colorscale=scl,
                reversescale=True,
                opacity=0.7,
                size=15,
                colorbar=dict(
                    lenmode='fraction', len=0.94, thickness=40,
                    titleside="right",
                    outlinecolor="rgba(68, 68, 68, 0)",
                    ticks="outside",
                    showticksuffix="last",
                    dtick=10
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
            resolution=110,
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
                range=[-90.0, 90.0],
                dtick=5
            )
        ), margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=50))}

    @app.callback(
        Output(component_id='my-gauge', component_property='value'),
        [Input(component_id='fake-input', component_property='value')])
    def update_output(value):
        data = aggregate_pipelines.get_failed_report_dataframe(session['user_id'])
        failed = data['count'][0]
        passed = data['count'][1]  # will make smaller once we have all the information we need.
        total = failed + passed
        score = (passed / total) * 100
        return score
