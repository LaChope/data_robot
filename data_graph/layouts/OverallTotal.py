import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

#Import module from parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from app import app

pio.templates.default = "plotly_white"

#-----------------Get the .csv files-----------------------------------------------
df = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')

layout_OverallTotal = html.Div([
    html.H1('Test Center Weekly Status 2019 CW 47'),
    html.H2('Test Requirements progress - total'),
    #Database Subplot
    html.Div([
        dcc.Graph(id='datatable-subplots')
    ]),

    #RangeSlider
    html.Div([
        dcc.RangeSlider(
            id='CW-RangeSlider',
            min=df['CW'].min(),
            max=df['CW'].max(),
            value=[df['CW'].min(), df['CW'].max()],
            marks={str(CW): str(CW) for CW in df['CW'].unique()},
            step=None
        ),
        html.Div(id='output-RangeSlider')
    ], style={'width': '80%', 'padding-left':'5%', 'padding-right':'5%'}),

    html.Br(),
    html.Br(),
    #Weekly Report DataTable
    html.Div([
            dt.DataTable(
            id='WeeklyReportResults',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
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
    [Input('CW-RangeSlider', 'value'),
    Input('WeeklyReportResults', 'selected_rows')]
    )

def update_figure(value, selected_rows):
    filtered_df = df[(df['CW'] >= value[0]) & (df['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = filtered_df["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualBlockedReq_SPsum"], name = "Actual tested", marker=dict(color='grey')))

    fig.update_layout(height=700, width=1900)
            
    return fig

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=False)