import pandas as pd
import plotly.graph_objects as go
import numpy as np


class PlotData():
    
    def plotWeeklyResults(self):

        df = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\WeeklyReportResults.csv')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df["CW"], y = df["OpenTicketsTotal"], name = "OpenTicketsTotal", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["InProgressTicketsTotal"], name = "InProgressTicketsTotal", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["ClosedTicketsTotal_perCW"], name = "ClosedTicketsTotal_perCW", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["ClosedTicketsTotal_perCW"], name = "ClosedTicketsTotal_perCW", mode = "lines"))

        fig.update_layout(title = "WeeklyReport", showlegend=True)
        fig.show()

    def plotIssueInGivenCW(self):

        df = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Issue.csv')

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df["CW"], y = df["OpenTicketsTotal"], name = "OpenTicketsTotal", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["InProgressTicketsTotal"], name = "InProgressTicketsTotal", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["ClosedTicketsTotal_perCW"], name = "ClosedTicketsTotal_perCW", mode = "lines"))
        fig.add_trace(go.Scatter(x = df["CW"], y = df["ClosedTicketsTotal_perCW"], name = "ClosedTicketsTotal_perCW", mode = "lines"))

        fig.update_layout(title = "WeeklyReport", showlegend=True)
        fig.show()

plot = PlotData()
plot.plotWeeklyResults
