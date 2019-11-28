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
df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')
df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')
df_MAP = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsMAP.csv')
df_JLR = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsJLR.csv')

layout = html.Div([
    #Title
    html.Div(
        [
            html.H1(
                'Test Center Weekly Status 2019 CW 47',
                style={'font-family': 'Helvetica',
                       "margin-top": "25",
                       "margin-bottom": "0",
                       'display': 'inline-block'
                       },
            ),
            html.Img(
                src='http://www.dwglogo.com/wp-content/uploads/2017/01/Alten-Logo.png',
                style={
                    'height': '15%',
                    'width': '15%',
                    'float': 'right',
                    'position': 'relative',
                    'display': 'inline-block'
                },
            ),
            html.P(
                'Overview',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%"},
            ),
        ],
    ),
        
    #Database Subplot
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-OverallPerWeek',
                    )
                ],
            ),
            html.Div(
                    [
                        dcc.RangeSlider(
                            id='CW-RangeSlider-OverallPerWeek',
                            min=df_overall['CW'].min(),
                            max=df_overall['CW'].max(),
                            value=[df_overall['CW'].min(), df_overall['CW'].max()],
                            marks={str(CW): str(CW) for CW in df_overall['CW'].unique()},
                            step=None
                        )
                    ],
                    style={'width': '80%', 'display': 'inline-block'}
                ),
        ],
        style={'width': '49%', 'display': 'inline-block'}
    ),
]) 



#-------------app callbacks-------------------------------------------
@app.callback(
    Output('datatable-subplots-OverallPerWeek', 'figure'), 
    [Input('CW-RangeSlider-OverallPerWeek', 'value')
    ])

def update_figure(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = filtered_df["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000}
    )
            
    return fig