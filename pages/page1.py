
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

from second import returnNameCombination, plot_timeline_MONTH, callMeBaby, last_x_days_most_listened_to_on_single_day, most_listened_to_on_single_day_top_10_days

print('I am page1')

layout = dbc.Container([
    #html.Div(id='my_div9'),
    #html.Button('Click Me', id='button3'), #when button is added -> n_click as an argument needed 
    
    html.Center(html.H1("GEDULD IST (vorerst) EINE TUGEND")),
    
    html.Div(id='my_div5'),
    html.Div(id='my_div6'),
    html.Div(id='my_div7'),
    html.Div(id='my_div8')
])


@callback(Output('my_div9', 'children'),
        Input('session_mbid1', 'data'),
        Input('session_username1', 'data'))
def result(session_mbid1, session_username1):
    print('def result(session_mbid1)')
    return 'your answer is session_mbid1 is ' + session_mbid1 + ' and your session_username1 is ' + session_username1


### OBVIOUSLY kann hier kein State(...) stehen, weil der Button nichts übergibt!
# MOST RECENTLY LISTENED TO SONG
@callback(
    Output('my_div5', 'children'),
    #Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    
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
    #Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    

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
    #Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
   
    df1 = most_listened_to_on_single_day_top_10_days(callMeBaby(mbid1, username1))
    

    fig = go.Figure()
    fig = px.bar(df1, x="Count", y="Song", color='User', orientation='h')
    
    
    fig.update_layout(title='Top Songs of last 10 Days')

    
    graph_website = html.Div(children=[
                
        html.Br(),
        dcc.Graph(
                    id='example-graph4',
                    figure=fig
                )
    ])

    

    return graph_website





@callback(
    Output('my_div8', 'children'),
    #Input('button3', 'n_clicks'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    if False:
        df2 = last_x_days_most_listened_to_on_single_day(callMeBaby(mbid1, username1),5)
        print('df1.head(3) ', df2.head(3))
        print('type(df1) ', type(df2))

        fig2 = go.Figure()

        print('2')
        

        fig2 = px.bar(df2, x="Count", y="Song", color='User', orientation='h')  
        print('3')  
        fig2.update_layout(title='Daily Top Songs of last 5 Days')
        print('4')
        
        graph_website2 = html.Div(children=[
                    
            html.Br(),
            dcc.Graph(
                        id='example-graph5',
                        figure=fig2
                    )
        ])

        print('5')
        return graph_website2
    return ''
