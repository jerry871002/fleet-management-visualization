"""
F05-2-all: RPM/SLIP/ME LOAD% Combined

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
import color

layout = html.Div([
    html.Div([
        dcc.Graph(id='eng_rpm_slip_history_graph_all',
                  className="nine columns",
                  style={'height': '95vh'})
    ]),
    html.Div([
        dcc.Graph(id='eng_rpm_slip_avg_graph_all',
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
    [Output('eng_rpm_slip_history_graph_all', 'figure'),
     Output('eng_rpm_slip_avg_graph_all', 'figure')],
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'voyage_route', # querry
            'new_v_datetime', # x-axis
            'slip', 'rpm_percentage', 'engine_load_percentage'] # y-axis

    # Load data from DB when first load the page
    if df.empty:
        # df = data.get_fig_dataframe(fig_no='F05-1',
        #                             fig_dataset=range(0, 11),
        #                             cols=cols)

        df = data.read_csv('fig_data/F05_2_all.csv')

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

    items = ['slip', 'rpm_percentage', 'engine_load_percentage']
    y = [df_draw[item].mean() for item in items]

    graph_1 = {
        'data': [
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['slip'],
                mode='lines',
                name='SLIP %'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['rpm_percentage'],
                mode='lines',
                name='RPM %'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['engine_load_percentage'],
                mode='lines',
                name='ME LOAD %'
            )
        ],
        'layout': go.Layout(
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'title': 'SLIP / RPM / ME LOAD %',
                'tickformat': ',.0%',
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
                x=['Slip', 'RPM %', 'Engine Load %'],
                y=y,
                marker_color=[color.blue,
                              color.orange,
                              color.green]
            )
        ],
        'layout': go.Layout(
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'tickformat': ',.0%',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            margin={'b': 40, 't': 40, 'l': 40, 'r': 10}
        )
    }

    return graph_1, graph_2
