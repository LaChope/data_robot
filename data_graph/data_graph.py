import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def plotSlide6():

    #Get the .csv files
    df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')
    df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')
    df_MAP = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsMAP.csv')
    df_JLR = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsJLR.csv')

    #Initialize figure with subplots
    fig = make_subplots(rows=2, cols=3, subplot_titles=("Total close", "Number of Opened Tickets / Week", "Total in Progress", "Opened HAFMap-tickets and SP","Opened DAI-tickets and SP","Opened JLR-tickets and SP"))

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["ClosedTicketsTotal_perCW"], name = "DAI", mode = "lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["ClosedTicketsTotal_perCW"], name = "JLR", mode = "lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["ClosedTicketsTotal_perCW"], name = "MAP", mode = "lines"), row=1, col=1)

    #Add traces for Number of Opened Tickets / Week
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["OpenTickets_perCW_Count"], name = "DAI", mode = "lines", showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["OpenTickets_perCW_Count"], name = "JLR", mode = "lines", showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["OpenTickets_perCW_Count"], name = "MAP", mode = "lines", showlegend=False), row=1, col=2)

    #Add traces for Total in Progress
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["InProgressTicketsTotal"], name = "DAI", mode = "lines", showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["InProgressTicketsTotal"], name = "JLR", mode = "lines", showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["InProgressTicketsTotal"], name = "MAP", mode = "lines", showlegend=False), row=1, col=3)

     #Add traces for Opened HAFMap-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["OpenTickets_perCW_SPsum"], name = "MAP", mode = "lines", showlegend=False), row=2, col=1)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_MAP["OpenTicketsTotal"], name = "MAP", showlegend=False), row=2, col=1)

    #Add traces for Opened DAI-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["OpenTickets_perCW_SPsum"], name = "DAI", mode = "lines", showlegend=False), row=2, col=2)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_DAI["OpenTicketsTotal"], name = "DAI", showlegend=False), row=2, col=2)

    #Add traces for Opened JLR-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["OpenTickets_perCW_SPsum"], name = "JLR", mode = "lines", showlegend=False), row=2, col=3)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_JLR["OpenTicketsTotal"], name = "JLR", showlegend=False), row=2, col=3)
 

    fig.update_layout(title_text="Test Center Weekly Status 2019 CW 46 Number of opened DAI, JLR, MAP -tickets per week")
    fig.show()

plotSlide6()
