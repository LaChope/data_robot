import dash, configparser
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.UNITED]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

def GetWeekNumber():
    init=configparser.ConfigParser()
    configFilePath='C:\Alten\Internal_Project\Scripts\data_robot\data_graph\data_graph_service.ini'
    init.read(configFilePath)
    Week_number = init.get('generic', 'week_number')

    return Week_number

#Login
#import dash_auth
#VALID_USERNAME_PASSWORD_PAIRS = [
#    ['mchopart2@de.alten.com', 'Spqbt2227958'],
#    ['test', 'test2']
#]
#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)
