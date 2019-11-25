import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from app import app


#-----------------Get the .csv files-----------------------------------------------
df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')

layout_OverallTotal = html.Div([
    html.H1('Test Center Weekly Status 2019 CW 47'),
    html.H2('Test Requirements progress - total'),
    #Database Subplot
    html.Div([
        dcc.Graph(id='datatable-subplots')
    ]),
    
    #Weekly Report DataTable
    html.Div([
            dt.DataTable(
            id='WeeklyReportResults',
            columns=[{"name": i, "id": i} for i in df_overall.columns],
            data=df_overall.to_dict('records'),
            editable=False,
            row_selectable='multi',
            filter_action='native',
            sort_action='native',
            selected_rows=[]
        ),
    ]
    ),
    html.Div(
        id='OverallTotal'),
        dcc.Link('Go to App 1', href='/layouts/OverallPerWeek')
])

app.layout = html.Div(children=[layout_OverallTotal])


#-------------app callbacks-------------------------------------------
@app.callback(Output('WeeklyReportResults', 'selected_rows'), 
            [Input('datatable-subplots', 'clickData')], 
            [State('WeeklyReportResults', 'selected_rows')])

def updated_selected_row_indices(clickData, selected_rows):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_rows:
                selected_rows.remove(point['pointNumber'])
            else:
                selected_rows.append(point['pointNumber'])
    return selected_rows

@app.callback(
    Output('datatable-subplots', 'figure'), 
    [Input('WeeklyReportResults', 'data'),
    Input('WeeklyReportResults', 'selected_rows')]
    )

def update_figure(data, selected_rows):
    dff = pd.DataFrame(data)
    fig = go.Figure()

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = dff["CW"], y = dff["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = dff["CW"], y = dff["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = dff["CW"], y = dff["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = dff["CW"], y = dff["ActualBlockedReq_SPsum"], name = "Actual tested", marker=dict(color='grey')))

    fig.update_layout(height=900, width=1900)
        
    return fig


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)