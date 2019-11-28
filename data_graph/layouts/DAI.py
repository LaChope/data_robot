import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
from dash.dependencies import Input, Output, State
import dash_table as dt
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
df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')

layout_DAI = html.Div([
    html.H1('Test Center Weekly Status 2019 CW 47'),

    #Database Subplot
    html.Div([
        dcc.Graph(
            id='datatable-subplots-DAI',
            style={'width': '100%', 'margin-left':'auto', 'margin-right':'auto'}
            )
    ]),

    #RangeSlider
    html.Div([
        dcc.RangeSlider(
            id='CW-RangeSlider-DAI',
            min=df['CW'].min(),
            max=df['CW'].max(),
            value=[df['CW'].min(), df['CW'].max()],
            marks={str(CW): str(CW) for CW in df['CW'].unique()},
            step=None
        ),
        html.Div(id='output-RangeSlider-DAI')
    ], style={'width': '80%', 'margin-left':'auto', 'margin-right':'auto'}),

    html.Br(),
    html.Br(),

    #DAI DataTable
    html.Div([
            dt.DataTable(
            id='ResultsIDC5',
            columns=[{"name": i, "id": i} for i in df_DAI.columns],
            data=df_DAI.to_dict('records'),
            editable=False,
            row_selectable='multi',
            filter_action='native',
            sort_action='native',
            selected_rows=[],
        ),
    ], style={'width': '50%', 'margin-left':'5%', 'margin-right':'5%', 'margin-left':'5%'}
    ),
])


#-------------app callbacks-------------------------------------------
@app.callback(
    Output('datatable-subplots-DAI', 'figure'), 
    [Input('CW-RangeSlider-DAI', 'value')
    ])

def update_figure(value):
    filtered_df = df[(df['CW'] >= value[0]) & (df['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = filtered_df["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(title={
        'text': 'Test Requirements progress - total',
        'x':0.5,
        'y':0.95,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    height=700, width=1900, transition={'duration':1000})
            
    return fig