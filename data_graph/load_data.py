import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Get the .csv files
df_overall = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\WeeklyReportResults.csv')
df_DAI = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsIDC5.csv')
df_MAP = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsMAP.csv')
df_JLR = pd.read_csv('C:\\Alten\\Internal_Project\\Data_repository\\Results_DB\\CSV\\ResultsJLR.csv')
print(df_overall.head())

#app layout
app=dash.Dash(__name__)
server=app.server
app.layout=html.Div([
    html.H2('My Dash App'),
    dt.DataTable(
        id='ResultsIDC5',
        columns=[{"name": i, "id": i} for i in df_DAI.columns],
        data=df_DAI.to_dict('records')
    ),
    html.Div(id='datatable'),
    dcc.Graph(
        id='datatable-subplots'
    )
    ], style={'width': '60%'})

@app.callback(Output('datatable-subplots', 'figure'), [Input('ResultsIDC5', 'data'), Input('ResultsIDC5', 'columns')])

def update_figure(data, selected_row_indices):
    dff = pd.Dataframe(data)
    fig = plotly.tools.make_subplots(rows=2, cols=3, 
    subplot_titles=("Total close", "Number of Opened Tickets / Week", "Total in Progress", "Opened HAFMap-tickets and SP","Opened DAI-tickets and SP","Opened JLR-tickets and SP"))

    #Add traces for Total Close
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["ClosedTicketsTotal_perCW"], name = "DAI", line={'color': 'green'}), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["ClosedTicketsTotal_perCW"], name = "JLR", line={'color': 'purple'}), row=1, col=1)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["ClosedTicketsTotal_perCW"], name = "MAP", line={'color': 'grey'}), row=1, col=1)

    #Add traces for Number of Opened Tickets / Week
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["OpenTickets_perCW_Count"], name = "DAI", line={'color': 'green'}, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["OpenTickets_perCW_Count"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["OpenTickets_perCW_Count"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=1, col=2)

    #Add traces for Total in Progress
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["InProgressTicketsTotal"], name = "DAI", line={'color': 'green'}, showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["InProgressTicketsTotal"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=1, col=3)
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["InProgressTicketsTotal"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=1, col=3)

    #Add traces for Opened HAFMap-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_MAP["OpenTickets_perCW_SPsum"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=2, col=1)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_MAP["OpenTicketsTotal"], name = "MAP", marker=dict(color='blue')), row=2, col=1)

    #Add traces for Opened DAI-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_DAI["OpenTickets_perCW_SPsum"], name = "DAI", showlegend=False), row=2, col=2)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_DAI["OpenTicketsTotal"], name = "DAI", marker=dict(color='blue'), showlegend=False), row=2, col=2)

    #Add traces for Opened JLR-tickets and SP
    fig.add_trace(go.Scatter(x = df_overall["CW"], y = df_JLR["OpenTickets_perCW_SPsum"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=2, col=3)
    fig.add_trace(go.Bar(x = df_overall["CW"], y = df_JLR["OpenTicketsTotal"], name = "JLR", marker=dict(color='blue'), showlegend=False), row=2, col=3)
    

    fig.update_layout(title_text="Test Center Weekly Status 2019 CW 46 Number of opened DAI, JLR, MAP -tickets per week")
    fig.show()
    print(dff)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=False)
    

