#app layout
app=dash.Dash
server=app.server
app.layout=html.Div([
    html.H2('My Dash App'),
    dt.Datatable(
        id='WeeklyReportResults',
        rows=df_overall.to_dict('records'),
        editable=False,
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[]
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='datatable-subplots'
    )
    ], style={'width': '60%'})