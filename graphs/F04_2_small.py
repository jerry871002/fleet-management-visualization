"""
F04-2-small: SOG Power BF Head(Small)
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data
import color

layout = html.Div([
    dcc.Graph(id='sog_power_bf_head_small_graph',
              style={'height': '95vh', 'width': '95vw'},
              config={'displayModeBar': False}),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()
df_draw = data.create_dataframe()

@app.callback(
    Output('sog_power_bf_head_small_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'rpm', # x-axis
            'thrust'] # y-axis

    # Load data from DB when first load the page
    if df.empty:
        df = data.get_fig_dataframe(fig_no='F04-2',
                                    fig_dataset=[1, 2],
                                    cols=cols)
        df.dropna(inplace=True)

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Prevent modify original data
    df_draw = df.copy()

    df_draw = df_draw[df_draw['rpm'] >= 35]
    df_draw_1 = df_draw[df_draw['fig_dataset'] == 1]
    df_draw_2 = df_draw[df_draw['fig_dataset'] == 2]

    x1, y1 = data.linear_reg(df_draw_1['rpm'], df_draw_1['thrust'])
    x2, y2 = data.linear_reg(df_draw_2['rpm'], df_draw_2['thrust'])

    return {
        'data': [
            go.Scatter(
                x=df_draw_1['rpm'],
                y=df_draw_1['thrust'],
                mode='markers',
                name='July-Sep',
                showlegend=False
            ),
            go.Scatter(
                x=df_draw_2['rpm'],
                y=df_draw_2['thrust'],
                mode='markers',
                name='Oct-Dec',
                showlegend=False
            ),
            go.Scatter(
                x=x1,
                y=y1,
                mode='lines',
                name='July-Sep Line',
                line={
                    'dash': 'dash',
                    'color': color.blue
                },
                showlegend=False
            ),
            go.Scatter(
                x=x2,
                y=y2,
                mode='lines',
                name='Oct-Dec Line',
                line={
                    'dash': 'dash',
                    'color': color.orange
                },
                showlegend=False
            )
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'RPM',
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'title': 'Thrust(kn)',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            margin={'l': 70, 'r': 30, 't': 30, 'b': 70},
            legend={'x': 0, 'y': -0.2, 'bgcolor': 'rgba(255, 255, 255, 0.5)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }
