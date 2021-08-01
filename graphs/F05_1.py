import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data

layout = html.Div([
    # html.H3('SOG-T / Current Speed / BF / RPM %'),
    dcc.Graph(id='sog_curent_bf_rpm_history_graph',
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
    Output('sog_curent_bf_rpm_history_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'voyage_route', # querry
            'new_v_datetime', # x-axis
            'sog', 'tcspeed', 'bf', # y1-axis
            'rpm_percentage'] # y2-axis

    # Load data from DB when first load the page
    if df.empty:
        df = data.get_fig_dataframe(fig_no='F05-1',
                                    fig_dataset=range(0, 9),
                                    cols=cols)
        df['new_v_datetime'] = data.to_datetime(df['new_v_datetime'])
        df.sort_values(by='new_v_datetime', inplace=True)
        df.dropna(inplace=True)

    # TODO: remove this when deploying!!!
    # !!! Only for debug !!!
    print('F05-1#####################')
    print(n_intervals)
    print(df.columns)
    print(df.empty)
    print('##########################')

    # Get URL parameters
    search_dic = data.get_search_dic()
    new_v_datetime = search_dic.get('new_v_datetime')
    voyage_route = search_dic.get('voyage_route')

    # Prevent modify original data
    df_draw = df.copy()

    # new_v_datetime
    if new_v_datetime != None:
        # TODO: remove print statement before deploying
        print('F05-1 Get dic value: ' + new_v_datetime)
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
                y=df_draw['sog'],
                mode='lines',
                name='SOG'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['tcspeed'],
                mode='lines',
                name='TC Speed'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['bf'],
                mode='lines',
                name='BF'
            ),
            go.Scatter(
                x=df_draw['new_v_datetime'],
                y=df_draw['rpm_percentage'],
                mode='lines',
                name='RPM %',
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
                'title': 'SOG<br>TC Speed<br>BF',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis2={
                'title': 'RPM %',
                'overlaying': 'y',
                'side': 'right',
                'tickformat': ',.0%',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            # margin={'l': 100, 'b': 200, 't': 10, 'r': 100},
            margin={'l': 100, 'r': 100},
            legend={'x': 0, 'y': -0.1, 'bgcolor': 'rgba(255, 255, 255, 0.5)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }
