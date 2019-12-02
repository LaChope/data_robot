import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.UNITED]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

#Login
#import dash_auth
#VALID_USERNAME_PASSWORD_PAIRS = [
#    ['username', 'password']
#]
#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)
