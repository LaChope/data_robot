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
from app import app, GetWeekNumber
from navbar import Navbar

pio.templates.default = "plotly_white"

#-----------------Get the .csv files-----------------------------------------------
df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')
df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')

#-----------------Layout----------------------------------------------------------
layout = html.Div([
    Navbar(),
    #Title
    html.Div(
        [
            html.H1(
                'Test Center Weekly Status 2019 CW ' + GetWeekNumber(),
                style={'font-family': 'Helvetica',
                       "margin-top": "0",
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
                    'display': 'inline-block',
                },
            ),
            #Overview
            html.P(
                'Requirements progress - DAI',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "1%"
                       },
            ),
        ],
    ),
        
    #Tickets per Week Review subplot
    html.Div(
        [
            #Plot
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-DAI',
                    )
                ],
            ),
            #RangeSlider
            html.Div(
                [
                    dcc.RangeSlider(
                        id='CW-RangeSlider-DAI',
                        min=df_overall['CW'].min(),
                        max=df_overall['CW'].max(),
                        value=[df_overall['CW'].min(), df_overall['CW'].max()],
                        marks={str(CW): str(CW) for CW in df_overall['CW'].unique()},
                        step=None
                    )
                ],
                style={'width': '80%', 'margin-left': '8%', 'margin-top': '2%', 'margin-bottom': '5%'}
            )
        ],
        style={'width': '100%', 'margin-top': '5%'}
    ),

    html.Div(
        [
            dt.DataTable(
                id='Table-DAI',
                columns=[{"name": i, "id": i} for i in df_DAI.columns],
                data=df_DAI.to_dict('records'),
                sort_action='native',
                column_selectable='multi',
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold',
                    'width': 'auto'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_table={'overflowX': 'scroll'},
                style_cell={
                    'minWidth': '0px', 'maxWidth': '200px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis'
                },
            )
        ],
        style={'width': '85%', 'margin-left': '5%', 'margin-top': '5%', 'margin-bottom': '5%'}
    )
])

@app.callback(
    Output('datatable-subplots-DAI', 'figure'), 
    [Input('CW-RangeSlider-DAI', 'value')
    ])

def update_figure_(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = df_DAI["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000},
        legend_orientation='h'
    )     
            
    return fig