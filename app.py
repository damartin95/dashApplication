
import dash
from flask import Flask
import dash_bootstrap_components as dbc


server = Flask(__name__)

app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])



