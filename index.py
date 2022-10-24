
import dash
from dash import dcc, html
from app import app, server

from pages import page0, page1, page2
from components import navbar

from dash.dependencies import Input, Output, State
import git


server = app.server
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
        return page0.layout
    elif pathname == '/page1':
         return page1.layout
    elif pathname == '/page2':
         return page2.layout
    else:
        return "Error 404!"

if __name__ == '__main__':
    app.run_server()
