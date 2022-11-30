
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask import Flask

from pages import page_login, page_data, page_aboutme
from components import navbar

import git




server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

nav = navbar.navbar()


@server.route('/git_update', methods=['POST'])
def git_update():
  repo = git.Repo('./dashApplication')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()                                
  origin.pull()
  return '', 200


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session_mbid1'),
    dcc.Store(id='session_username1'),
    dcc.Store(id='session_mbid2'),
    dcc.Store(id='session_username2'),
    nav, 
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_login.layout
    elif pathname == '/data':
         return page_data.layout
    elif pathname == '/aboutme':
         return page_aboutme.layout
    else:
        return "Error 404!"

if __name__ == '__main__':
    app.run_server()
