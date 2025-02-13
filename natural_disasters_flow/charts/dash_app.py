import pymysql
import os
import dash
from dash import dcc
from dotenv import load_dotenv
from charts_functions import *

load_dotenv()
# get db connection info from .env
db = os.getenv('DB_BASE')
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
app = dash.Dash(__name__)

# set up the main structure of the page with charts and a map
with pymysql.connect(host=host, user=user, password=password, database=db) as conn:
    with conn.cursor() as cursor:
        map = create_map(conn.cursor())
    app.layout = html.Div([
        html.H1('Disasters Trends:', style={'textAlign': 'center'}),
        dcc.Graph(id='bar-chart', figure=create_bar_diagram(conn)),
        html.H1('Percentage By Regions:', style={'textAlign': 'center'}),
        dcc.Graph(id='regions-chart', figure=create_regions_chart(conn)),
        html.H1('Percentage By Seasons:', style={'textAlign': 'center'}),
        dcc.Graph(id='seasons-chart', figure=create_seasons_chart(conn)),
        html.H1('Events Map(last 90 days):', style={'textAlign': 'center'}),
        html.Div(id='map', children=map),

        # update charts every six hours
        dcc.Interval(id='interval-update', interval=1000 * 60 * 60 * 6, n_intervals=0)
    ])


# update charts and map when the interval triggers by making a new query to the db
@app.callback([dash.dependencies.Output('bar-chart', 'figure'),
               dash.dependencies.Output('regions-chart', 'figure'),
               dash.dependencies.Output('seasons-chart', 'figure'),
               dash.dependencies.Output('map', 'children')],
              [dash.dependencies.Input('interval-update', 'n_intervals')])
def update_graphs(n):
    with pymysql.connect(host=host, user=user, password=password, database=db) as conn:
        bar_fig = create_bar_diagram(conn)
        regions_fig = create_regions_chart(conn)
        seasons_fig = create_seasons_chart(conn)
        with conn.cursor() as cursor:
            map_html = create_map(cursor)
        return bar_fig, regions_fig, seasons_fig, map_html


if __name__ == "__main__":
    app.run_server(debug=True)
