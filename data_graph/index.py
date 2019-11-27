import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from app import server
from layouts import OverallPerWeek, OverallTotal, DAI, HAFMAP, JLR

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Navigate to "/OverallPerWeek"', href='/OverallPerWeek'),

    html.Br(),
    dcc.Link('Navigate to "/OverallTotal"', href='/OverallTotal'),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/OverallPerWeek':
        return OverallPerWeek
    elif pathname == '/OverallTotal':
        return OverallTotal
    elif pathname == 'C:\\Alten\\Internal_Project\\Scripts\\data_robot\\data_graph\\DAI.py':
        return DAI
    elif pathname == 'C:\\Alten\\Internal_Project\\Scripts\\data_robot\\data_graph\\HAFMAP.py':
        return HAFMAP
    elif pathname == 'C:\\Alten\\Internal_Project\\Scripts\\data_robot\\data_graph\\JLR.py':
        return JLR
    else:
        return 'Error 404'

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=False)