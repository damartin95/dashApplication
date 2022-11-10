
import pandas as pd
import plotly.express as px
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from analytics import *


print('I am page0')

style_dbc_Input = {'width':'450px','height':'45px','padding':'10px','margin-top':'10px', 
            'border-width':'2px','border-color':'#a0a3a2'}

style_html_Button = {'width':'100px','height':'45px','padding':'10px','margin-top':'10px', 
            'border-width':'2px','border-color':'#a0a3a2'}


layout = dbc.Container([

    html.Br(),
    html.Center(html.H1("Login")),
    html.Br(),
    html.Br(),
    html.Div(
        children=[
            dbc.Input(id='mbid1', value='835defa77f6078c7a34c3c6ba04854c6', type="text", 
            style=style_dbc_Input),
            ],
        style={"display": "flex", "justifyContent": "center"}),
    html.Div(
        children=[
            dbc.Input(id='username1', value='wuhuspringfield', type='text',
            style=style_dbc_Input),
            ],
        style={"display": "flex", "justifyContent": "center"}),
    html.Br(),
    html.Div(
        children=[
            dbc.Button('Submit', id='button1', n_clicks=0,  #remove n_clicks=0!
            color='secondary'),
            ],
        style={"display": "flex", "justifyContent": "center"}),

    html.Br(),

    html.Div(
        children=[
        dbc.Checklist(
            options=[
                {"label": "You want to add a friend?", "value": 1}, #default value = 0
            ],
            value=[1], # default value = []
            id="switches_input",
            switch=True
        ),], 
        style={"display": "flex", "justifyContent": "center"}
    
    ),
    html.Br(),
    html.Div(id='add_friend_form')
    
    
])


@callback( 
    Output('session_mbid1', 'data'),
    [Input('button1', 'n_clicks')],
    [State('mbid1', 'value'),
    State('username1', 'value')],
    #, prevent_initial_call=True
)
def write_session_mbid1(n_clicks, mbid1, username1): ### FIX - no need for three arguments
    #print('write_session_mbid2')
    if n_clicks==None: ### When switching between page0 and page1, session_mbid and session_username are not saved because n_clicks==None and therewith will be made ''
        return ''
    else:
        #print('wrote session_mbid1')
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
        #print('wrote session_username1')
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
    #print('write_session_mbid2')
    if n_clicks==None: ### When switching between page0 and page1, session_mbid and session_username are not saved because n_clicks==None and therewith will be made ''
        return ''
    else:
        #print('wrote session_mbid2')
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



@callback(
    Output("add_friend_form", "children"), 
    Input("switches_input", "value"),
)
def add_friend(switches_input):

    print('Y u no call me?')
    print('switches_input ', switches_input)

    if len(switches_input) > 0:

        add_friend_form = html.Div(children=[
            html.Div(
            children=[
                dbc.Input(id='mbid2', value='ab8ab5b6deefd7b8afa5c1adab89fcb8', type="text", 
                style=style_dbc_Input),
                ],
            style={"display": "flex", "justifyContent": "center"}),
            html.Div(
                children=[
                    dbc.Input(id='username2', value='feybmertn', type='text',
                    style=style_dbc_Input),
                    ],
                style={"display": "flex", "justifyContent": "center"}),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button('Submit', id='button2', n_clicks=0,  #remove n_clicks=0!
                    color='secondary'),
                    ],
                style={"display": "flex", "justifyContent": "center"}),

        ])
        return add_friend_form
    else:
        return ''