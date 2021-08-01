"""
F03-3-small: Wind Speed and Direction Diagram(Small)
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data
import color

layout = html.Div([
    dcc.Graph(id='wind_direction_analysis_small_graph',
              style={'height': '95vh', 'width': '95vw'},
              config={'displayModeBar': False}),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()

@app.callback(
     Output('wind_direction_analysis_small_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df

    if df.empty:
        df = data.read_csv('fig_data/F03_3.csv')

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
            font_size=11,
            polar_radialaxis_tickformat=',.0%',
            showlegend=False,
            margin={'l': 30, 'b': 25, 't': 25, 'r': 30}
        )
    }
