"""
F02-1: Voyage Review

Parameters:
    new_v_datetime
    voyage_route
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data

layout = html.Div([
    dcc.Graph(id='voyage_review_graph',
              style={'height': '95vh', 'width': '95vw'},
              config={'scrollZoom': True}),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()
df_draw = data.create_dataframe()

@app.callback(
    Output('voyage_review_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'voyage_route', # querry
            'new_v_datetime', # x-axis
            'rpm', 'sog', 'stw', # y1-axis
            'slip'] # y2-axis

    # Load data from DB when first load the page
    if df.empty:
        # df = data.get_fig_dataframe(fig_no='F02-1',
        #                             fig_dataset=range(0, 10),
        #                             cols=cols)
                                    
        df = data.read_csv('fig_data/F02_1.csv')

        df['new_v_datetime'] = data.to_datetime(df['new_v_datetime'])
        df.sort_values(by='new_v_datetime', inplace=True)
        df.dropna(inplace=True)

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Get URL parameters
    search_dic = data.get_search_dic()
    new_v_datetime = search_dic.get('new_v_datetime')
    voyage_route = search_dic.get('voyage_route')

    # Prevent modify original data
    df_draw = df.copy()

    # new_v_datetime
    if new_v_datetime != None:
        df_draw = df_draw[df_draw['new_v_datetime'] < data.to_datetime(new_v_datetime)]
    # voyage_route
    if voyage_route != None:
        df_draw = df_draw[df_draw['voyage_route'].astype('int64') == int(voyage_route)]
    else:
        # default value for voyage_route is 0
        df_draw = df_draw[df_draw['voyage_route'] == 0]

    return {
        'data': [
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['rpm'],
                mode='lines',
                name='RPM'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['sog'],
                mode='lines',
                name='SOG'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['stw'],
                mode='lines',
                name='STW'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['slip'],
                mode='lines',
                name='Slip %',
                yaxis='y2'
            )
        ],
        'layout': go.Layout(
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'title': 'RPM / SOG / STW',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis2={
                'title': 'Slip %',
                'overlaying': 'y',
                'side': 'right',
                'tickformat': ',.0%',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            margin={'l': 100, 'r': 100},
            legend={'x': 0, 'y': -0.15, 'bgcolor': 'rgba(255, 255, 255, 0.5)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }
