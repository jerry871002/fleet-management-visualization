"""
F04-4: Current Direction & Speed
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data
import color

layout = html.Div([
    dcc.Graph(id='current_direction_analysis_graph',
              style={'height': '95vh', 'width': '95vw'}),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()

@app.callback(
     Output('current_direction_analysis_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df

    if df.empty:
        df = data.read_csv('fig_data/F04_4.csv')

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    theta = df.columns.drop('Level')

    return {
        'data': [
            go.Barpolar(
                r=df.loc[df['Level'] == '0-4', 'E': ].squeeze(),
                theta=theta,
                name='0-4 m/s',
                marker_color=color.wind_rose[0]
            ),
            go.Barpolar(
                r=df.loc[df['Level'] == '4-8', 'E': ].squeeze(),
                theta=theta,
                name='4-8 m/s',
                marker_color=color.wind_rose[1]
            ),
            go.Barpolar(
                r=df.loc[df['Level'] == '8-12', 'E': ].squeeze(),
                theta=theta,
                name='8-12 m/s',
                marker_color=color.wind_rose[2]
            ),
            go.Barpolar(
                r=df.loc[df['Level'] == '12-16', 'E': ].squeeze(),
                theta=theta,
                name='12-16 m/s',
                marker_color=color.wind_rose[3]
            ),
            go.Barpolar(
                r=df.loc[df['Level'] == '16-20', 'E': ].squeeze(),
                theta=theta,
                name='16-20 m/s',
                marker_color=color.wind_rose[4]
            ),
            go.Barpolar(
                r=df.loc[df['Level'] == '>20', 'E': ].squeeze(),
                theta=theta,
                name='>20 m/s',
                marker_color=color.wind_rose[5]
            )
        ],
        'layout': go.Layout(
            title='Current Direction & Speed',
            font_size=16,
            legend_font_size=16,
            polar_radialaxis_tickformat=',.0%',
            margin={'l': 30, 'b': 25, 't': 100, 'r': 30}
        )
    }
