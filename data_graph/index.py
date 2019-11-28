import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from layouts import OverallPerWeek, OverallTotal, DAI, HAFMAP, JLR, home

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Navigate to "/home"', href='/home'),
    html.Br(),
    dcc.Link('Navigate to "/OverallPerWeek"', href='/OverallPerWeek'),
    html.Br(),
    dcc.Link('Navigate to "/OverallTotal"', href='/OverallTotal'),
    html.Br(),
    dcc.Link('Navigate to "/DAI"', href='/DAI'),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    if pathname == '/OverallPerWeek':
        return OverallPerWeek.layout_OverallPerWeek
    elif pathname == '/OverallTotal':
        return OverallTotal.layout_OverallTotal
    elif pathname == '/DAI':
        return DAI.layout_DAI
    elif pathname == '/HAFMAP':
        return HAFMAP.layout_HAFMAP
    elif pathname == '/JLR':
        return JLR.layout_JLR
    else:
        return 'Error 404'

if __name__ == '__main__':
    app.run_server(debug=False)