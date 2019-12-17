import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from flask import session
import string
from . import aggregate_pipelines
import geocoder

scl = [0, "rgb(242, 51, 242)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
      [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
      [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]

mapbox_access_token = 'pk.eyJ1IjoibmF0aGFubWFyc29uIiwiYSI6ImNrNDdwcnFnaDB4bmEzZG1reDZ0ZGU4NTkifQ.AN6b7zESbtQ8vJy8AovR0Q'


def update_string(attribute):
    """Splits strings by underscores and capitalises each word"""
    return string.capwords(' '.join(attribute.split('_')), ' ')


def create_line(df, values, x, y):
    """creates a line in a line graph based on the parameters entered"""
    return go.Scatter(x=df[values[x]], y=df[values[y]], mode='lines+markers', name=update_string(values[y]),
                      line=dict(width=4), showlegend=True,
                      marker={'size': 7, "opacity": 0.6})


def register_callbacks(app):
    @app.callback(
        Output('map', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')])
    def select_date(start_date, end_date):
        """Displays map points alongside score percentage based on dates selected and sorting method"""
        df = aggregate_pipelines.get_map_dataframe(session['user_id'])
        values = list(df.columns.values)
        mask = df['Created_at'].between(start_date, end_date)
        g = geocoder.ip('me')

        trace = go.Scattermapbox(
            lat=df['Y'].get(mask),
            lon=df['X'].get(mask),
            text=df['Score'].astype(str) + ' percent',
            hoverinfo='text',
            marker=dict(
                color=df['Score'],
                colorscale=scl,
                reversescale=True,
                opacity=0.7,
                size=15,
                colorbar=dict(
                    lenmode='fraction', len=1, thickness=30,
                    titleside="right",
                    outlinecolor="rgba(68, 68, 68, 0)",
                    ticks="outside",
                    showticksuffix="last",
                    dtick=10
                )
            )
        )
        return {'data': [trace], 'layout': go.Layout(margin=dict(l=0, r=0, b=0, t=0),
                                                     mapbox={'accesstoken': mapbox_access_token, 'bearing': 0,
                                                             'center': {'lat': g.latlng[0], 'lon': g.latlng[1]},
                                                             'pitch': 0, 'zoom': 2,
                                                             "style": 'mapbox://styles/mapbox/light-v9'}
                                                     )}

    # callback from the Guage
    @app.callback([
        Output('my-gauge', 'value'),
        Output('total-failed', 'children'),
        Output('total-passed', 'children'),
        Output('avg-score', 'children'),
        Output('total-audits', 'children')],
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')])
    def update_output(start_date, end_date):
        data = aggregate_pipelines.get_failed_report_dataframe(session['user_id'], start_date, end_date)
        score_percentage = round(
            aggregate_pipelines.get_average_score_percentage(session['user_id'], start_date, end_date))
        try:
            failed = data['count'][0]
        except KeyError:
            failed = 0
        try:
            passed = data['count'][1]
        except KeyError:
            passed = 0
        total = failed + passed
        percentage_failed = round((failed / total) * 100)
        percentage_passed = round((passed / total) * 100)
        account_health = (score_percentage / 2.5) + (percentage_passed / 1.5)
        return account_health, 'Incomplete Audits: {}%'.format(percentage_failed), 'Complete Audits: {}%'.format(
            percentage_passed), 'Avg Audit Score: {}%'.format(score_percentage), 'Total Audits: {}'.format(total)

    @app.callback([
        Output('total-failed', 'style'),
        Output('total-passed', 'style'),
        Output('avg-score', 'style'),
        Output('total-audits', 'style')],
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')])
    def update_output(start_date, end_date):
        data = aggregate_pipelines.get_failed_report_dataframe(session['user_id'], start_date, end_date)
        score_percentage = round(
            aggregate_pipelines.get_average_score_percentage(session['user_id'], start_date, end_date))
        try:
            failed = data['count'][0]
        except KeyError:
            failed = 0
        try:
            passed = data['count'][1]
        except KeyError:
            passed = 0
        total = failed + passed
        percentage_failed = round((failed / total) * 100)
        percentage_passed = round((passed / total) * 100)
        total_style = {'margin': '10px auto', 'padding': '15px 0', }
        failed_style = {'margin': '10px auto', 'padding': '15px 0', }
        avg_style = {'margin': '10px auto', 'padding': '15px 0', }
        if percentage_failed >= 50:
            failed_style['background-color'] = 'rgba(255, 0, 0, 0.18)'  # red
        elif percentage_failed >= 30:
            failed_style['background-color'] = 'rgba(255, 153, 0, 0.42)'  # orange
        elif percentage_failed >= 20:
            failed_style['background-color'] = 'rgba(255, 247, 0, 0.36)'  # yellow
        else:
            failed_style['background-color'] = 'rgba(133, 255, 0, 0.25)'  # green
        if score_percentage <= 50:
            avg_style['background-color'] = 'rgba(255, 0, 0, 0.18)'  # red
        elif score_percentage <= 70:
            avg_style['background-color'] = 'rgba(255, 153, 0, 0.42)'  # orange
        elif score_percentage <= 80:
            avg_style['background-color'] = 'rgba(255, 247, 0, 0.36)'  # yellow
        else:
            avg_style['background-color'] = 'rgba(133, 255, 0, 0.25)'  # green
        if total < 1:
            total_style['background-color'] = 'rgba(255, 0, 0, 0.18)'  # red
        else:
            total_style['background-color'] = 'rgba(133, 255, 0, 0.25)'  # green

        return failed_style, failed_style, avg_style, total_style

    @app.callback(
        Output('score-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], start_date, end_date)
        values = list(df.columns.values)
        return {"data": [create_line(df, values, 6, 2), create_line(df, values, 6, 4)],
                "layout": go.Layout(title="Average Scores",
                                    hovermode='closest'
                                    )}

    @app.callback(
        Output('score-percent-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], start_date, end_date)
        values = list(df.columns.values)
        return {"data": [create_line(df, values, 6, 3)],
                "layout": go.Layout(title="Average Score Percentage",
                                    hovermode='closest'
                                    )}

    @app.callback(
        Output('duration-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], start_date, end_date)
        values = list(df.columns.values)
        return {"data": [create_line(df, values, 6, 1)],
                "layout": go.Layout(title="Average Audit Duration",
                                    hovermode='closest'
                                    )}

    @app.callback(
        Output('audits-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], start_date, end_date)
        values = list(df.columns.values)
        return {"data": [create_line(df, values, 6, 0), create_line(df, values, 6, 7)],
                "layout": go.Layout(title="Total vs Failed Audits",
                                    hovermode='closest'
                                    )}
