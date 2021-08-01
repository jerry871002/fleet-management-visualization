"""
F04-3-small: Ship Speed Impact Factor(Small)

Parameters:
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
    dcc.Graph(id='ship_speed_impact_analysis_small_graph',
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
    Output('ship_speed_impact_analysis_small_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['voyage_route', # querry
            'waveh', 'bf', 'tw_head_beam_tail',
            'tw_direction_index', 'tc_head_beam_tail', 'tc_direction_index',
            'twspeed', 'tcspeed', 'slip',
            'stw', 'sog', 'poweravgkw',
            'me_foc_hfo', 'rpm']

    # Load data from DB when first load the page
    if df.empty:
        # df = data.get_corr_data(cols)

        df = data.read_csv('fig_data/F04_3.csv')

        df['tc_direction_index'] = df['tc_direction_index'].map(data.directions_dict.get)
        df['tw_direction_index'] = df['tw_direction_index'].map(data.directions_dict.get)
        df['tc_head_beam_tail'] = df['tc_head_beam_tail'].map(data.hbt_dict.get)
        df['tw_head_beam_tail'] = df['tw_head_beam_tail'].map(data.hbt_dict.get)

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Get URL parameters
    search_dic = data.get_search_dic()
    voyage_route = search_dic.get('voyage_route')

    # Prevent modify original data
    df_draw = df.copy()

    # voyage_route
    if voyage_route != None:
        df_draw = df_draw[df_draw['voyage_route'].astype('int64') == int(voyage_route)]
    else:
        # default value for voyage_route is 0
        df_draw = df_draw[df_draw['voyage_route'] == 0]

    # Make the correlation matrix with lower triangular mask
    df_draw.drop('voyage_route', axis=1, inplace=True)
    df_draw.rename(columns=data.F04_3_cols_name, inplace=True)
    df_corr = df_draw.corr()
    df_draw = data.correlation_matrix(df_corr)

    # Prevent elements not in the main diagonal has the value 1
    for n in range(len(df_draw.index)):
        for m in range(len(df_draw.columns)):
            if not data.isnan(df_draw.iloc[n, m]) and m + n != 13:
                df_draw.iloc[n, m] *= 0.999

    return {
        'data': [
            go.Heatmap(
                z=df_draw.apply(abs),
                x=df_draw.columns,
                y=df_draw.index,
                colorscale=color.corr_colorscale,
                showscale=False
            )
        ],
        'layout': go.Layout(
            xaxis={'showgrid': False},
            yaxis={'showgrid': False},
            margin={'t': 0, 'b': 0, 'l': 0, 'r': 0}
        )
    }
