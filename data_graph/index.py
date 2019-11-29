import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from layouts import  home, DAI, HAFMAP, JLR

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link(
        'Navigate to "/Home"', href='/home'),
    dcc.Link('Navigate to "/DAI"', href='/DAI'),
    dcc.Link('Navigate to "/HAFMap"', href='/HAFMap'),
    dcc.Link('Navigate to "/JLR"', href='/JLR'),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/DAI':
        return DAI.layout_DAI
    elif pathname == '/HAFMAP':
        return HAFMAP.layout_HAFMAP
    elif pathname == '/JLR':
        return JLR.layout_JLR

if __name__ == '__main__':
    app.run_server(debug=False)