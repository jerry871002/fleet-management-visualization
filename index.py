import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from graphs import *
from data import set_search_dic

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
               Input('url', 'search')])
def display_page(pathname, search):
    set_search_dic(search)

    if pathname == '/graphs/F01-1':
        return F01_1.layout
    elif pathname == '/graphs/F02-1':
        return F02_1.layout
    elif pathname == '/graphs/F03-1':
        return F03_1.layout
    elif pathname == '/graphs/F03-1-small':
        return F03_1_small.layout
    elif pathname == '/graphs/F03-1-2':
        return F03_1_2.layout
    elif pathname == '/graphs/F03-1-2-small':
        return F03_1_2_small.layout
    elif pathname == '/graphs/F03-3':
        return F03_3.layout
    elif pathname == '/graphs/F03-3-small':
        return F03_3_small.layout
    elif pathname == '/graphs/F04-1':
        return F04_1.layout
    elif pathname == '/graphs/F04-1-2':
        return F04_1_2.layout
    elif pathname == '/graphs/F04-1-small':
        return F04_1_small.layout
    elif pathname == '/graphs/F04-1-2-small':
        return F04_1_2_small.layout
    elif pathname == '/graphs/F04-2':
        return F04_2.layout
    elif pathname == '/graphs/F04-2-small':
        return F04_2_small.layout
    elif pathname == '/graphs/F04-3':
        return F04_3.layout
    elif pathname == '/graphs/F04-3-small':
        return F04_3_small.layout
    elif pathname == '/graphs/F04-4':
        return F04_4.layout
    elif pathname == '/graphs/F04-4-small':
        return F04_4_small.layout
    elif pathname == '/graphs/F05-1-all':
        return F05_1_all.layout
    elif pathname == '/graphs/F05-1-all-small':
        return F05_1_all_small.layout
    elif pathname == '/graphs/F05-2-all':
        return F05_2_all.layout
    elif pathname == '/graphs/F05-2-all-small':
        return F05_2_all_small.layout
    elif pathname == '/graphs/F05-3-all':
        return F05_3_all.layout
    elif pathname == '/graphs/F05-3-all-small':
        return F05_3_all_small.layout
    else:
        return 'Sorry we don\'t have this page.'

if __name__ == '__main__':
    app.run_server(debug=True)
