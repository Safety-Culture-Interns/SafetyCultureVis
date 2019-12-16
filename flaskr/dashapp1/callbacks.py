import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from flask import session
import string

from . import aggregate_pipelines

scl = [0, "rgb(242, 51, 242)"], [0.125, "rgb(0, 0, 200)"], [0.25, "rgb(0, 25, 255)"], \
      [0.375, "rgb(0, 152, 255)"], [0.5, "rgb(44, 255, 150)"], [0.625, "rgb(151, 255, 0)"], \
      [0.75, "rgb(255, 234, 0)"], [0.875, "rgb(255, 111, 0)"], [1, "rgb(255, 0, 0)"]

mapbox_access_token = 'pk.eyJ1IjoibmF0aGFubWFyc29uIiwiYSI6ImNrNDdwcnFnaDB4bmEzZG1reDZ0ZGU4NTkifQ.AN6b7zESbtQ8vJy8AovR0Q'


def update_string(attribute):
    """Splits strings by underscores and capitalises each word"""
    return string.capwords(' '.join(attribute.split('_')), ' ')


def register_callbacks(app):
    @app.callback(
        Output('map', 'figure'),
        [Input('date-picker-range', 'start_date'),
         Input('date-picker-range', 'end_date'),
         Input('date-sort', 'value')])
    def select_date(start_date, end_date, sorting_method):
        """Displays map points alongside score percentage based on dates selected and sorting method"""
        df = aggregate_pipelines.get_map_dataframe(session['user_id'])
        values = list(df.columns.values)
        df[sorting_method] = pd.to_datetime(df[sorting_method or 'Created_at'])
        mask = df[sorting_method].between(start_date, end_date)

        trace = go.Scattermapbox(
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
            )
        )
        return {'data': [trace], 'layout': go.Layout(
            mapbox={'accesstoken': mapbox_access_token, 'bearing': 0,
                    'center': {'lat': 38, 'lon': -94}, 'pitch': 0, 'zoom': 3,
                    "style": 'mapbox://styles/mapbox/light-v9'}
        )}

    # callback from the Guage
    @app.callback([
        Output('my-gauge', 'value'),
        Output('total-failed', 'children'),
        Output('total-passed', 'children')],
        [Input('fake-input', 'value')])
    def update_output(value):
        data = aggregate_pipelines.get_failed_report_dataframe(session['user_id'])
        failed = data['count'][0]
        passed = data['count'][1]  # will make smaller once we have all the information we need.
        total = failed + passed
        percentage_failed = round((failed / total) * 100)
        percentage_passed = round((passed / total) * 100)
        style = {'background-color': 'red'}
        return percentage_passed, 'Failed: {}%'.format(percentage_failed), 'Passed: {}%'.format(
            percentage_passed)

    @app.callback([
        Output('total-failed', 'style'),
        Output('total-passed', 'style')],
        [Input('fake-input', 'value')])
    def update_output(value):
        data = aggregate_pipelines.get_failed_report_dataframe(session['user_id'])
        failed = data['count'][0]
        passed = data['count'][1]
        total = failed + passed
        percentage_failed = round((failed / total) * 100)
        percentage_passed = round((passed / total) * 100)
        failed_style = {'margin': '10px auto', 'padding': '15px 0', }
        if percentage_failed >= 50:
            failed_style['background-color'] = 'rgba(255, 0, 0, 0.18)'
        elif percentage_failed >= 30:
            failed_style['background-color'] = 'rgba(255, 153, 0, 0.42)'
        elif percentage_failed >= 20:
            failed_style['background-color'] = 'rgba(255, 247, 0, 0.36)'
        else:
            failed_style['background-color'] = 'rgba(133, 255, 0, 0.25)'

        return failed_style, failed_style

    @app.callback(
        Output(component_id='score-graph', component_property='figure'),
        [Input(component_id='fake-input', component_property='value')]
    )
    def update_graph(value):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], 30)
        values = list(df.columns.values)
        return {"data": [
            go.Scatter(x=df[values[6]], y=df[values[2]], mode='lines+markers', name=update_string(values[2]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, ),
            go.Scatter(x=df[values[6]], y=df[values[4]], mode='lines+markers', name=update_string(values[4]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, )],
            "layout": go.Layout(title="Average Scores",
                                hovermode='closest'
                                )}

    @app.callback(
        Output(component_id='score-percent-graph', component_property='figure'),
        [Input(component_id='fake-input', component_property='value')]
    )
    def update_graph(value):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], 30)
        values = list(df.columns.values)
        return {"data": [
            go.Scatter(x=df[values[6]], y=df[values[3]], mode='lines+markers', name=update_string(values[3]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, )],
            "layout": go.Layout(title="Average Score Percentage",
                                hovermode='closest'
                                )}

    @app.callback(
        Output(component_id='duration-graph', component_property='figure'),
        [Input(component_id='fake-input', component_property='value')]
    )
    def update_graph(value):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], 30)
        values = list(df.columns.values)
        return {"data": [
            go.Scatter(x=df[values[6]], y=df[values[1]], mode='lines+markers', name=update_string(values[1]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, )],
            "layout": go.Layout(title="Average Audit Duration",
                                hovermode='closest'
                                )}

    @app.callback(
        Output(component_id='audits-graph', component_property='figure'),
        [Input(component_id='fake-input', component_property='value')]
    )
    def update_graph(value):
        df = aggregate_pipelines.get_stats_by_x_days(session['user_id'], 30)
        values = list(df.columns.values)
        return {"data": [
            go.Scatter(x=df[values[6]], y=df[values[0]], mode='lines+markers', name=update_string(values[0]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, ),
            go.Scatter(x=df[values[6]], y=df[values[7]], mode='lines+markers', name=update_string(values[7]),
                       marker={'size': 5, "opacity": 0.6,
                               "line": {'width': 0.5}}, )],
            "layout": go.Layout(title="Total vs Failed Audits",
                                hovermode='closest'
                                )}
