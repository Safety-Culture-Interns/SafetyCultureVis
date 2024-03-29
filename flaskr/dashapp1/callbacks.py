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


def fill_data(df, start_date, end_date, y):
    """Creates a new dataframe in a specified daterange, filling any dates that have no value with 0"""
    series = pd.Series(dict(zip(df['date'], df[y])))
    series.index = pd.DatetimeIndex(series.index)
    series = series.reindex(pd.date_range(pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()),
                            fill_value=0)

    filled_dataframe = pd.DataFrame({update_string(y): series})
    return filled_dataframe.reset_index(inplace=False)


def create_line(df):
    """creates a line in a line graph based on the parameters entered"""
    columns = list(df.columns.values)
    return go.Scatter(x=df[columns[0]], y=df[columns[1]], mode='lines+markers', name=columns[1],
                      line=dict(width=4), showlegend=True,
                      marker={'size': 7, "opacity": 0.6})


def register_callbacks(app):
    @app.callback(
        Output('map', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')])
    def select_date(start_date, end_date):
        """Displays map points alongside score percentage based on dates selected and sorting method"""
        df = aggregate_pipelines.get_map_dataframe(session['user_id'], start_date, end_date)
        g = geocoder.ip('me')

        trace = go.Scattermapbox(
            lat=df['Y'],
            lon=df['X'],
            text=df['Score'].astype(str) + ' percent',
            hoverinfo='text',
            marker=dict(
                color=df['Score'].append(pd.Series(100)),
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
        Output('health_score', 'children'),
        Output('health_score', 'style'),
        Output('my-gauge', 'value'),
        Output('total-failed', 'children'),
        Output('total-passed', 'children'),
        Output('avg-score', 'children'),
        Output('total-audits', 'children'),
        Output('total-failed', 'style'),
        Output('total-passed', 'style'),
        Output('avg-score', 'style'),
        Output('total-audits', 'style')],
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')])
    def update_output(start_date, end_date):
        data = aggregate_pipelines.get_completed_report_dataframe(session['user_id'], start_date, end_date)
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

        if failed and passed is not None:
            percentage_failed = round((failed / total) * 100)
            percentage_passed = round((passed / total) * 100)
        else:
            percentage_failed = 0
            percentage_passed = 0
        account_health = (score_percentage / 2.5) + (percentage_passed / 1.5)
        total_style = {'margin': '10px auto', 'padding': '15px 0', }
        failed_style = {'margin': '10px auto', 'padding': '15px 0', }
        health_style = {'color': 'rgba(255, 0, 0, 0.18)'}
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
        if account_health <= 50:
            health_style = {'color': 'rgba(255, 0, 0, 1)'}
        elif account_health <= 70:
            health_style = {'color': 'rgba(255, 153, 0, 1)'}
        elif account_health <= 80:
            health_style = {'color': 'rgba(255, 247, 0, 1)'}
        else:
            health_style = {'color': 'rgba(133, 255, 0, 1)'}

        return "{}%".format(round(account_health)), health_style, account_health, 'Incomplete Audits: {}%'.format(
            percentage_failed), 'Complete Audits: {}%'.format(
            percentage_passed), 'Avg Audit Score: {}%'.format(score_percentage), 'Total Audits: {}'.format(
            total), failed_style, failed_style, avg_style, total_style

    @app.callback(
        Output('score-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_date(session['user_id'], start_date, end_date)
        return {"data": [create_line(fill_data(df, start_date, end_date, 'avg_score')),
                         create_line(fill_data(df, start_date, end_date, 'avg_total_score'))],
                "layout": go.Layout(title="Average Scores",
                                    hovermode='closest'
                                    )}

    @app.callback(
        Output('score-percent-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_date(session['user_id'], start_date, end_date)
        return {"data": [create_line(fill_data(df, start_date, end_date, 'avg_score_percentage'))],
                "layout": go.Layout(title="Average Score Percentage",
                                    hovermode='closest',
                                    )}

    @app.callback(
        Output('duration-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_date(session['user_id'], start_date, end_date)
        return {"data": [create_line(fill_data(df, start_date, end_date, 'avg_duration'))],
                "layout": go.Layout(title="Average Audit Duration (Seconds)",
                                    hovermode='closest'
                                    )}

    @app.callback(
        Output('audits-graph', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = aggregate_pipelines.get_stats_by_date(session['user_id'], start_date, end_date)
        return {"data": [create_line(fill_data(df, start_date, end_date, 'audits')),
                         create_line(fill_data(df, start_date, end_date, 'incomplete_audits'))],
                "layout": go.Layout(title="Total vs Incomplete Audits",
                                    hovermode='closest'
                                    )}
