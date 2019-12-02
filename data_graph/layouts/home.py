import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import configparser


#Import module from parent folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from app import app
from navbar import Navbar

pio.templates.default = "plotly_white"


def GetWeekNumber():
    init=configparser.ConfigParser()
    configFilePath='C:\Alten\Internal_Project\Scripts\data_robot\data_graph\data_graph_service.ini'
    init.read(configFilePath)
    Week_number = init.get('generic', 'week_number')

    return Week_number

#-----------------Get the .csv files-----------------------------------------------
df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')
df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')
df_MAP = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsMAP.csv')
df_JLR = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsJLR.csv')

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
                'Number of opened DAI, JLR, MAP - tickets per week',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "1%"
                       },
            ),
            html.Div(
                [
                    dcc.RangeSlider(
                        id='CW-RangeSlider',
                        min=df_overall['CW'].min(),
                        max=df_overall['CW'].max(),
                        value=[df_overall['CW'].min(), df_overall['CW'].max()],
                        marks={str(CW): str(CW) for CW in df_overall['CW'].unique()},
                        step=None
                    )
                ],
                style={'width': '80%', 'margin-left': '8%', 'margin-top': '8%'}
            )
        ],
    ),
        
    #Tickets per Week Review subplot
    html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-OverallPerWeek-dashboard',
                    )
                ],
            ),
        ],
        style={'width': '100%', 'margin-top': '5%'}
    ),
    
    #Test Requirements progress - total subplot
    html.Div(
        [
            html.P(
                'Test Requirements progress - total',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "10%"
                       },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-OverallTotal-dashboard'
                    )
                ],
            ),
        ]
    ),

    #Test Requirements progress - DAI
    html.Div(
        [
            html.P(
                'Test Requirements progress - DAI',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "10%"
                       },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-DAI-dashboard'
                    )
                ],
            ),
        ]
    ),

    #Test Requirements progress - HAFMap
    html.Div(
        [
            html.P(
                'Test Requirements progress - HAFMap',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "10%"
                       },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-MAP-dashboard'
                    )
                ],
            ),
        ]
    ),

    #Test Requirements progress - JLR
    html.Div(
        [
            html.P(
                'Test Requirements progress - JLR',
                style={'font-family': 'Helvetica',
                       "font-size": "200%",
                       "width": "100%",
                       "margin-top": "10%"
                       },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-JLR-dashboard'
                    )
                ],
            ),
        ]
    )
]) 



#-------------app callbacks-------------------------------------------
@app.callback(
    Output('datatable-subplots-OverallPerWeek-dashboard', 'figure'), 
    [Input('CW-RangeSlider', 'value')
    ])

def update_figure_OverallPerWeek(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = plotly.subplots.make_subplots(
        rows=2, cols=3,
        specs=[[{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}],
                [{"secondary_y": True}, {"secondary_y": True}, {"secondary_y": True}]],
        subplot_titles=("Total close", "Number of Opened Tickets / Week", "Total in Progress", "Opened HAFMap-tickets and SP","Opened DAI-tickets and SP","Opened JLR-tickets and SP"
        )
    )

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_DAI["ClosedTicketsTotal_perCW"], name = "DAI", line={'color': 'green'}), row=1, col=1)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_JLR["ClosedTicketsTotal_perCW"], name = "JLR", line={'color': 'purple'}), row=1, col=1)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_MAP["ClosedTicketsTotal_perCW"], name = "MAP", line={'color': 'grey'}), row=1, col=1)

    #Add traces for Number of Opened Tickets / Week
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_DAI["OpenTickets_perCW_Count"], name = "DAI", line={'color': 'green'}, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_JLR["OpenTickets_perCW_Count"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_MAP["OpenTickets_perCW_Count"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=1, col=2)

    #Add traces for Total in Progress
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_DAI["InProgressTicketsTotal"], name = "DAI", line={'color': 'green'}, showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_JLR["InProgressTicketsTotal"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_MAP["InProgressTicketsTotal"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=1, col=3)

    #Add traces for Opened HAFMap-tickets and SP
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_MAP["OpenTickets_perCW_SPsum"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=2, col=1, secondary_y=False)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_MAP["OpenTicketsTotal"], name = "Tickets", marker=dict(color='skyblue')), row=2, col=1, secondary_y=True)

    #Add traces for Opened DAI-tickets and SP
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_DAI["OpenTickets_perCW_SPsum"], name = "DAI", showlegend=False), row=2, col=2, secondary_y=False)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_DAI["OpenTicketsTotal"], name = "DAI", marker=dict(color='skyblue'), showlegend=False), row=2, col=2, secondary_y=True)

    #Add traces for Opened JLR-tickets and SP
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_JLR["OpenTickets_perCW_SPsum"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=2, col=3, secondary_y=False)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_JLR["OpenTicketsTotal"], name = "JLR", marker=dict(color='skyblue'), showlegend=False), row=2, col=3, secondary_y=True)

    fig.update_layout(
        transition={'duration':1000},
        legend=dict(
            x=-0.1, 
            y=1,
        ),
    )   

    return fig

@app.callback(
    Output('datatable-subplots-OverallTotal-dashboard', 'figure'), 
    [Input('CW-RangeSlider', 'value'),
    ])

def update_figure_OverallTotal(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for OverallTotal
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = filtered_df["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = filtered_df["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000},
        legend=dict(
            x=1, 
            y=1,
        ),
    )

    return fig

@app.callback(
    Output('datatable-subplots-DAI-dashboard', 'figure'), 
    [Input('CW-RangeSlider', 'value')
    ])

def update_figure_DAI(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for DAI
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = df_DAI["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_DAI["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000},
        legend=dict(
            x=1, 
            y=1,
        ),
    )     
            
    return fig

@app.callback(
    Output('datatable-subplots-MAP-dashboard', 'figure'), 
    [Input('CW-RangeSlider', 'value')
    ])

def update_figure_MAP(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for MAP
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = df_MAP["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_MAP["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_MAP["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_MAP["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000},
        legend=dict(
            x=1, 
            y=1,
        ),
    )     
            
    return fig


@app.callback(
    Output('datatable-subplots-JLR-dashboard', 'figure'), 
    [Input('CW-RangeSlider', 'value')
    ])

def update_figure_JLR(value):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = go.Figure()

    #Add traces for JLR
    fig.add_trace(go.Scatter(x = filtered_df['CW'], y = df_JLR["ActualSummaryReq_SPsum"], name = "Actual Summary", line={'color': 'orangered'}))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_JLR["ActualTestedReq_SPsum"], name = "Actual tested", marker=dict(color='skyblue')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_JLR["ActualInProgress_SPsum"], name = "Actual in progress", marker=dict(color='orange')))
    fig.add_trace(go.Bar(x = filtered_df['CW'], y = df_JLR["ActualBlockedReq_SPsum"], name = "Actual blocked", marker=dict(color='grey')))

    fig.update_layout(
        transition={'duration':1000},
        legend=dict(
            x=1, 
            y=1,
        ),
    )     
            
    return fig