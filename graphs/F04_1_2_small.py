"""
F04-1-2-small: Propeller Performance Combined(Small)

Parameters:
    oldstartdatetime
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data
import color

layout = html.Div([
    dcc.Graph(id='propeller_performance_forecast_small_graph_all',
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
    Output('propeller_performance_forecast_small_graph_all', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'oldstartdatetime', # x-axis
            'propeller_quotient'] # y-axis

    # Load data from DB when first load the page
    if df.empty:
        # df = data.get_fig_dataframe(fig_no='F04-1',
        #                             fig_dataset=[1, 2],
        #                             cols=cols)

        df = data.read_csv('fig_data/F04_1.csv')

        df['oldstartdatetime'] = data.to_datetime(df['oldstartdatetime'])
        df.sort_values(by='oldstartdatetime', inplace=True)
        df.dropna(inplace=True)

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Get URL parameters
    search_dic = data.get_search_dic()
    oldstartdatetime = search_dic.get('oldstartdatetime')

    # Prevent modify original data
    df_draw = df.copy()

    # oldstartdatetime
    if oldstartdatetime != None:
        df_draw = df_draw[df_draw['oldstartdatetime'] < data.to_datetime(oldstartdatetime)]

    df_draw['propeller_quotient'] = 0.1 / df_draw['propeller_quotient']
    df_draw = df_draw[df_draw['propeller_quotient'] > 0.3]

    x, y = data.linear_reg_date(df_draw['oldstartdatetime'], df_draw['propeller_quotient'])

    return {
        'data': [
            go.Scatter(
                x=df_draw['oldstartdatetime'],
                y=df_draw['propeller_quotient'],
                mode='markers',
                name='PQ',
                showlegend=False
            ),
            go.Scatter(
                x=x,
                y=y,
                mode='lines',
                name='PQ 1 Line',
                line={
                    'dash': 'dash',
                    'color': color.blue
                },
                showlegend=False
            ),
        ],
        'layout': go.Layout(
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True,
                'range': [0, 0.8]
            },
            margin={'l': 50, 'r': 10, 't': 10, 'b': 30},
            legend={'x': 0, 'y': -0.15, 'bgcolor': 'rgba(255, 255, 255, 0)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }
