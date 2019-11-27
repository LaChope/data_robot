import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import dash.dependencies
from dash.dependencies import Input, Output, State
import plotly
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

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

layout_OverallPerWeek = html.Div([
    html.H1('Test Center Weekly Status 2019 CW 47'),
    html.H2('Number of opened DAI, JLR, MAP -tickets per week'),
    #Database Subplot
    html.Div([
        dcc.Graph(id='datatable-subplots-OverallPerWeek')
    ]),

    #RangeSlider
    html.Div([
        dcc.RangeSlider(
            id='CW-RangeSlider',
            min=df_overall['CW'].min(),
            max=df_overall['CW'].max(),
            value=[df_overall['CW'].min(), df_overall['CW'].max()],
            marks={str(CW): str(CW) for CW in df_overall['CW'].unique()},
            step=None
        ),
        html.Div(id='output-RangeSlider')
    ], style={'width': '80%', 'padding-left':'10%', 'padding-right':'5%'}),

    html.Br(),
    html.Br(),
    #First dt
    html.Div([
            dt.DataTable(
            id='TableResultsIDC5',
            columns=[{"name": i, "id": i} for i in df_DAI.columns],
            data=df_DAI.to_dict('records'),
            editable=False,
            row_selectable='multi',
            filter_action='native',
            sort_action='native',
            selected_rows=[]
        ),
    ], style={'width': '50%', 'display': 'inline-block'}
    ),
        
    #Second dt
    html.Div([
        dt.DataTable(
            id='overall',
            columns=[{"name": i, "id": i} for i in df_overall.columns],
            data=df_overall.to_dict('records'),
            editable=False,
            row_selectable='multi',
            filter_action='native',
            sort_action='native',
            selected_rows=[]
            )
    ], style={'width': '50%', 'display': 'inline-block'}
    ),
    
    html.Div(id='OverallPerWeek'),
    html.Br()
])

app.layout = html.Div(children=[layout_OverallPerWeek])

#-------------app callbacks-------------------------------------------
@app.callback(Output('TableResultsIDC5', 'selected_rows'), 
            [Input('datatable-subplots-OverallPerWeek', 'clickData')], 
            [State('TableResultsIDC5', 'selected_rows')])

def updated_selected_row_indices(clickData, selected_rows):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_rows:
                selected_rows.remove(point['pointNumber'])
            else:
                selected_rows.append(point['pointNumber'])
    return selected_rows

@app.callback(
    Output('datatable-subplots-OverallPerWeek', 'figure'), 
    [Input('CW-RangeSlider', 'value'),
    Input('TableResultsIDC5', 'selected_rows')]
    )

def update_figure(value, selected_rows):
    filtered_df = df_overall[(df_overall['CW'] >= value[0]) & (df_overall['CW'] <= value[1])]
    fig = plotly.subplots.make_subplots(rows=2, cols=3, 
    subplot_titles=("Total close", "Number of Opened Tickets / Week", "Total in Progress", "Opened HAFMap-tickets and SP","Opened DAI-tickets and SP","Opened JLR-tickets and SP"),
    shared_xaxes=True)

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
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_MAP["OpenTickets_perCW_SPsum"], name = "MAP", line={'color': 'grey'}, showlegend=False), row=2, col=1)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_MAP["OpenTicketsTotal"], name = "Tickets", marker=dict(color='skyblue')), row=2, col=1)

    #Add traces for Opened DAI-tickets and SP
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_DAI["OpenTickets_perCW_SPsum"], name = "DAI", showlegend=False), row=2, col=2)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_DAI["OpenTicketsTotal"], name = "DAI", marker=dict(color='skyblue'), showlegend=False), row=2, col=2)

    #Add traces for Opened JLR-tickets and SP
    fig.add_trace(go.Scatter(x = filtered_df["CW"], y = df_JLR["OpenTickets_perCW_SPsum"], name = "JLR", line={'color': 'purple'}, showlegend=False), row=2, col=3)
    fig.add_trace(go.Bar(x = filtered_df["CW"], y = df_JLR["OpenTicketsTotal"], name = "JLR", marker=dict(color='skyblue'), showlegend=False), row=2, col=3)

    fig.update_layout(height=700, width=1900)

    return fig

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=False)