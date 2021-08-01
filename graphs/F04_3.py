"""
F04-3: Ship Speed Impact Factor

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
    dcc.Graph(id='ship_speed_impact_analysis_graph',
              style={'height': '95vh', 'width': '95vw'}),
    dcc.Interval(
        id='interval_component',
        interval=1*1000*60*5, # update every 5 minutes
        n_intervals=0
    )
])

df = data.create_dataframe()
df_draw = data.create_dataframe()

@app.callback(
    Output('ship_speed_impact_analysis_graph', 'figure'),
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
        df = data.get_corr_data(cols)
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

    annotations = go.Annotations()
    for n in range(len(df_draw.index)):
        for m in range(len(df_draw.columns)):
            if data.isnan(df_draw.iloc[n, m]):
                text = ''
            else:
                text = str(df_draw.iloc[n, m])
                # Prevent elements not in the main diagonal has the value 1
                if m + n != 13:
                    df_draw.iloc[n, m] *= 0.999

            if 0.4 < abs(df_draw.iloc[n, m]) < 0.7:
                font = '#11134e'
            else:
                font = 'white'

            annotations.append(go.Annotation(text=text,
                                             x=df_draw.columns[m],
                                             y=df_draw.index[n],
                                             showarrow=False,
                                             font={'color': font}))

    return {
        'data': [
            go.Heatmap(
                z=df_draw.apply(abs),
                x=df_draw.columns,
                y=df_draw.index,
                colorscale=color.corr_colorscale
            )
        ],
        'layout': go.Layout(
            annotations=annotations,
            xaxis={'showgrid': False},
            yaxis={'showgrid': False}
        )
    }
