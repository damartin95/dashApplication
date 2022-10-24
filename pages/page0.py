
import pandas as pd
import plotly.express as px
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from second import returnNameCombination, plot_timeline_MONTH, callMeBaby


print('I am page0')


layout = dbc.Container([
    html.Br(),
    html.Br(),
    dbc.Input(id='mbid1', value='835defa77f6078c7a34c3c6ba04854c6', type="text"),
    html.Br(),
    dbc.Input(id='username1', value='wuhuspringfield', type='text'),
    html.Br(),
    html.Button('Click Me', id='button1', n_clicks=0), #remove n_clicks=0!
    html.Div(id='my-div2'),
    html.Div(id='my-div3'),
    html.Br(),
    html.P('Add additional user'),
    html.Br(),
    dbc.Input(id='mbid2', value='ab8ab5b6deefd7b8afa5c1adab89fcb8', type="text"),
    html.Br(),
    dbc.Input(id='username2', value='feybmertn', type='text'),
    html.Br(),
    html.Button('Click Me', id='button2', n_clicks=0), #remove n_clicks=0!
    html.Br()
])


@callback( 
    Output('session_mbid1', 'data'),
    [Input('button1', 'n_clicks')],
    [State('mbid1', 'value'),
    State('username1', 'value')],
    #, prevent_initial_call=True
)
def write_session_mbid1(n_clicks, mbid1, username1): ### FIX - no need for three arguments
    print('write_session_mbid2')
    if n_clicks==None: ### When switching between page0 and page1, session_mbid and session_username are not saved because n_clicks==None and therewith will be made ''
        return ''
    else:
        print('wrote session_mbid1')
        return mbid1

@callback(
    Output('session_username1', 'data'),
    [Input('button1', 'n_clicks')],
    [State('mbid1', 'value'),
    State('username1', 'value')],
    prevent_initial_call=True
)
def write_session_username1(n_clicks, mbid1, username1):  ### FIX - no need for three arguments
    if n_clicks==None:
        return ''
    else:
        print('wrote session_username1')
        return username1

@callback(
    Output('my-div3', 'children'),
    [Input('button1', 'n_clicks')],
    [State('mbid2', 'value'),
        State('username2', 'value')],
    prevent_initial_call=True
)
def update_output_div(n_clicks, mbid, username):
    return '!You have entered "{}" and "{}" and clicked {} times. Please provide valid information'.format(mbid, username, n_clicks)




@callback( 
    Output('session_mbid2', 'data'),
    [Input('button2', 'n_clicks')],
    [State('mbid2', 'value'),
    State('username2', 'value')],
    #, prevent_initial_call=True
)
def write_session_mbid1(n_clicks, mbid2, username2): ### FIX - no need for three arguments
    print('write_session_mbid2')
    if n_clicks==None: ### When switching between page0 and page1, session_mbid and session_username are not saved because n_clicks==None and therewith will be made ''
        return ''
    else:
        print('wrote session_mbid2')
        return mbid2

@callback(
    Output('session_username2', 'data'),
    [Input('button2', 'n_clicks')],
    [State('mbid2', 'value'),
    State('username2', 'value')],
    prevent_initial_call=True
)
def write_session_username1(n_clicks, mbid2, username2):  ### FIX - no need for three arguments
    if n_clicks==None:
        return ''
    else:
        print('wrote session_username2')
        return username2
