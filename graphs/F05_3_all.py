"""
F05-3-all: Fuel Consumption Combined
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data
import color

layout = html.Div([
    html.Div([
        dcc.Graph(id='me_foc_history_graph_all',
                  className="nine columns",
                  style={'height': '95vh'})
    ]),
    html.Div([
        dcc.Graph(id='me_foc_sum_graph_all',
                  className="three columns",
                  style={'height': '95vh'})
    ]),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()
df_draw = data.create_dataframe()

@app.callback(
    [Output('me_foc_history_graph_all', 'figure'),
     Output('me_foc_sum_graph_all', 'figure')],
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    # Load data from DB when first load the page
    if df.empty:
        # df = data.get_fig_table(table_name='fm_fig_f05_3')
        df = data.read_csv('fig_data/F05_3.csv')

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Prevent modify original data
    df_draw = df.copy()

    # Get URL parameters
    search_dic = data.get_search_dic()
    voyage_route = search_dic.get('voyage_route')

    # voyage_route
    if voyage_route != None:
        df_draw = df_draw[df_draw['voyage_route'].astype('int64') == int(voyage_route)]
    else:
        # default value for voyage_route is 0
        df_draw = df_draw[df_draw['voyage_route'] == 0]

    items = ['me_foc_hfo', 'ae_foc_hfo']
    y = [df_draw[item].sum() for item in items]

    graph_1 = {
        'data': [
            go.Bar(
                x=df_draw['date'],
                y=df_draw['ae_foc_hfo'],
                name='AE FOC HFO'
            ),
            go.Bar(
                x=df_draw['date'],
                y=df_draw['me_foc_hfo'],
                name='ME FOC HFO'
            )
        ],
        'layout': go.Layout(
            barmode='stack',
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'title': 'MT / Day',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            margin={'b': 40, 't': 40, 'l': 60, 'r': 50},
            legend={'x': 0, 'y': -0.1, 'bgcolor': 'rgba(255, 255, 255, 0)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }

    graph_2 = {
        'data': [
            go.Bar(
                x=['ME FOC HFO', 'AE FOC HFO'],
                y=y,
                marker_color=[color.orange, color.blue]
            )
        ],
        'layout': go.Layout(
            barmode='stack',
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            margin={'b': 40, 't': 40, 'l': 40, 'r': 10}
        )
    }

    return graph_1, graph_2
