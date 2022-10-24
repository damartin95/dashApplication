
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

from second import returnNameCombination, plot_timeline_MONTH, callMeBaby, last_x_days_most_listened_to_on_single_day

print('I am page1')

layout = dbc.Container([
    html.Div(id='my_div8'),
    html.Button('Click Me daddy', id='button3'),
    html.Div(id='my_div5'),
    html.Div(id='my_div6'),
    html.Div(id='my_div7')
])


@callback(Output('my_div8', 'children'),
        Input('session_mbid1', 'data'),
        Input('session_username1', 'data'))
def result(session_mbid1, session_username1):
    print('def result(session_mbid1)')
    return 'your answer is session_mbid1 is ' + session_mbid1 + ' and your session_username1 is ' + session_username1


### OBVIOUSLY kann hier kein State(...) stehen, weil der Button nichts übergibt!
# MOST RECENTLY LISTENED TO SONG
@callback(
    Output('my_div5', 'children'),
    Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(n_clicks, mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    
    output1 = returnNameCombination(mbid1, username1) 
    output2 = returnNameCombination(mbid2, username2) 
    graph_website = html.Div(children=[
                
        html.H2(children=output1),
        html.H2(children=output2)
    ])

    return graph_website
    



#GRAPHICS    
@callback(
    Output('my_div6', 'children'),
    Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(n_clicks, mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    

    df1 = plot_timeline_MONTH(callMeBaby(mbid1, username1))
    df2 = plot_timeline_MONTH(callMeBaby(mbid2, username2))

    fig = go.Figure()
    fig = fig.add_traces(go.Scatter(x = df1['Year'], y = df1['Song'], name=username1))
    fig = fig.add_traces(go.Scatter(x = df2['Year'], y = df2['Song'], name=username2))
    
    fig.update_layout(title='# Songs per Day')
    fig.update_traces(mode='markers+lines')
    
    
    
    graph_website = html.Div(children=[
                
        html.Br(),
        dcc.Graph(
                    id='example-graph3',
                    figure=fig
                )
    ])

    return graph_website
    
    




@callback(
    Output('my_div7', 'children'),
    Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(n_clicks, mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
   
    df1 = last_x_days_most_listened_to_on_single_day(callMeBaby(mbid1, username1),5)
    print('df1.head(3) ', df1.head(3))
    print('type(df1) ', type(df1))

    fig = go.Figure()
    
    fig = px.bar(df1, x="Count", y="Song", color='User', orientation='h')
    
    
    fig.update_layout(title='xxx')
    
    
    graph_website = html.Div(children=[
                
        html.Br(),
        dcc.Graph(
                    id='example-graph4',
                    figure=fig
                )
    ])

    return graph_website
