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
                'Overview',
                style={'font-family': 'Helvetica',
                       "font-size": "300%",
                       "width": "100%",
                       "margin-top": "1%"
                       },
            ),
        ],
    ),
        
    #Tickets per Week Review sunplot
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
                style={'width': '80%', 'margin-left': '8%'}
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
                       "font-size": "300%",
                       "width": "100%",
                       "margin-top": "10%"
                       },
            ),
            html.Div(
                [
                    dcc.Graph(
                        id='datatable-subplots-Total'
                    )
                ],
            ),
            html.Div(
                [
                    dcc.RangeSlider(
                        id='CW-RangeSlider-OverallTotal',
                        min=df_overall['CW'].min(),
                        max=df_overall['CW'].max(),
                        value=[df_overall['CW'].min(), df_overall['CW'].max()],
                        marks={str(CW): str(CW) for CW in df_overall['CW'].unique()},
                        step=None
                    )
                ]
            )
        ]
    )
]) 



#-------------app callbacks-------------------------------------------
@app.callback(
    Output('datatable-subplots-OverallPerWeek', 'figure'), 
    [Input('CW-RangeSlider-OverallPerWeek', 'value')
    ])

def update_figure(value):
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
        title=dict(
            text='Number of opened DAI, JLR, MAP - tickets per week',
            font={'family': 'Helvetica', 'size': 25},
            x=0.5,
            y=1
        ),
        transition={'duration':1000},
        legend=dict(
            x=-0.1, 
            y=1,
        ),
    )   

    return fig

