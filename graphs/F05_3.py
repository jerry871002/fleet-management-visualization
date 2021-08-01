import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

from app import app
import data

layout = html.Div([
    # html.H3('Fuel Consumption'),
    dcc.Graph(id='me_foc_history_graph',
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
    Output('me_foc_history_graph', 'figure'),
    [Input('interval_component', 'n_intervals')]
)
def update_figure(n_intervals):
    global df
    global df_draw

    # Load data from DB when first load the page
    if df.empty:
        df = data.get_fig_table(table_name='fm_fig_f05_3')

    data.debug_info(__name__, n_intervals, df.columns, df.empty)

    # Prevent modify original data
    df_draw = df.copy()

    return {
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
                # 'tickformat': ',.0%',
                'zeroline': False,
                'mirror': True,
                'ticks': 'outside',
                'showline': True
            },
            # margin={'l': 100, 'b': 200, 't': 10, 'r': 100},
            margin={'l': 100},
            legend={'x': 0, 'y': -0.1, 'bgcolor': 'rgba(255, 255, 255, 0.5)'},
            legend_orientation='h',
            hovermode='closest'
        )
    }
