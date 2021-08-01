import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data

layout = html.Div([
    # html.H3('RPM / SLIP / ME LOAD Avg'),
    dcc.Graph(id='eng_rpm_slip_avg_graph',
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
    Output('eng_rpm_slip_avg_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    cols = ['timeid', # id
            'voyage_route', 'new_v_datetime', # querry
            'slip','rpm_percentage','engine_load_percentage'] # bar

    # Load data from DB when first load the page
    if df.empty:
        df = data.get_fig_dataframe(fig_no='F05-2',
                                    fig_dataset=range(0, 9),
                                    cols=cols)
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
        # TODO: remove print statement before deploying
        print('F05-2-1 Get dic value: ' + new_v_datetime)
        df_draw = df_draw[df_draw['new_v_datetime'] < data.to_datetime(new_v_datetime)]
    # voyage_route
    if voyage_route != None:
        df_draw = df_draw[df_draw['voyage_route'].astype('int64') == int(voyage_route)]
    else:
        # default value for voyage_route is 0
        df_draw = df_draw[df_draw['voyage_route'] == 0]

    items = ['slip', 'rpm_percentage', 'engine_load_percentage']
    y = [df_draw[item].mean() for item in items]

    return {
        'data': [
            go.Bar(
                x=['Slip', 'RPM %', 'Engine Load %'],
                y=y,
                marker_color=['rgb(36, 117, 180)',
                              'rgb(253, 125, 18)',
                              'rgb(52, 164, 44)']
            )
        ],
        'layout': go.Layout(
            xaxis={
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            yaxis={
                'tickformat': ',.1%',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            }
            # margin={'l': 100, 'b': 200, 't': 10, 'r': 100},
            # legend={'x': 0, 'y': -0.1, 'bgcolor': 'rgba(255, 255, 255, 0.5)'},
            # legend_orientation='h',
            # hovermode='closest'
        )
    }
