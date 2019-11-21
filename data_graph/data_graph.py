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
    fig = make_subplots(rows=2, cols=3, subplot_titles=("Total close", "Number of Opened Tickets / Week", "Total in Progress", "Opened HAFMap-tickets and SP" "Opened DAI-tickets and SP""Opened JLR-tickets and SP"))

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["ClosedTicketsTotal_perCW"], name = "DAI", mode = "lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["ClosedTicketsTotal_perCW"], name = "JLR", mode = "lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["ClosedTicketsTotal_perCW"], name = "MAP", mode = "lines"), row=1, col=1)

    fig.update_layout(title_text="test")
    fig.show()

plotSlide6()
