import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from layouts import  home, DAI, HAFMAP, JLR


#Import module from parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from app import app
from navbar import Navbar
from layouts.home import Homepage

nav = Navbar()

app.layout = html.Div(
    [
        dcc.Location(id = 'url', refresh = False),
        html.Div(id = 'page-content')
    ]
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return Homepage()
    elif pathname == '/DAI':
        return DAI.layout
    elif pathname == '/HAFMAP':
        return HAFMAP.layout
    elif pathname == '/JLR':
        return JLR.layout
    else:
        return Homepage()

if __name__ == '__main__':
    app.run_server(debug=False)