
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px

from second import *

print('I am page1')


TEST = False


style_html_dropDown = {'width':'100px', 'border-width':'2px','border-color':'#a0a3a2'}



layout = dbc.Container([
    #html.Div(id='my_div9'),
    #html.Button('Click Me', id='button3'), #when button is added -> n_click as an argument needed 
    
    html.Center(html.H1("GEDULD IST (vorerst) EINE TUGEND")),
    

    html.Div(id='my_div5'),

    
    html.Div(
        children=[
        dcc.Dropdown(
            ['Day', 'Month', 'Year'],
            'Day',
            clearable=False,
            id = 'song_per_day_dd',
            searchable=False,
            style=style_html_dropDown
        ),], 
        style={"display": "flex", "justifyContent": "center"}
    ),
    

    html.Div(
        children=[
        dcc.Dropdown(
            id='opt_dropdown',
            clearable=False,
            searchable=False,
            style=style_html_dropDown
        ),],
        style={"display": "flex", "justifyContent": "center"}
    ),


    html.Div(id='my_div6'),
    html.Div(id='my_div666'),

    html.Div(
        children=[
        dcc.Dropdown(
            ['2022-10', '2022-11'],
            '2022-10',
            clearable=False,
            id = 'top_songs_per_month',
            searchable=False,
            style=style_html_dropDown
        ),], 
        style={"display": "flex", "justifyContent": "center"}
    ),

    html.Div(id='my_div9999'),
    html.Div(id='my_div7'),
    html.Div(id='my_div8')
])



@callback(
    Output('opt_dropdown', 'options'),
    Output('opt_dropdown', 'value'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data')
)
def update_date_dropdown(mbid1, username1):
    df = callMeBaby(mbid1, username1)
    df.Date = pd.to_datetime(df.Date)
    df['Date_month'] = df.Date.dt.to_period("M")
    df = df.loc[df['Date_month'].notnull()]
    dflist = df['Date_month'].drop_duplicates().astype(str).tolist()
    
    return dflist, dflist[0]




@callback(
        Output('my_div9', 'children'),
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
    if TEST:
        output1 = returnNameCombination(mbid1, username1) 
        output2 = returnNameCombination(mbid2, username2) 
        graph_website = html.Div(children=[
                    
            html.H2(children=output1),
            html.H2(children=output2)
        ])

        return graph_website
    return ''
    



#GRAPHICS    
@callback(
    Output('my_div6', 'children'),
    #Input('button3', 'n_clicks'),
    Input('song_per_day_dd', 'value'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(timefilter, mbid1, username1, mbid2, username2): #n_clicks wird bei page-reload auf None gesetzt
    if TEST:

        print('timefilter ', timefilter)
        print('mbid1 ', mbid1)

        df1 = plot_timeline_MONTH(callMeBaby(mbid1, username1), timefilter)
        df2 = plot_timeline_MONTH(callMeBaby(mbid2, username2), timefilter)

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
    return ''
    



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
   

    if TEST:

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
    return ''




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
    if TEST:
        df2 = last_x_days_most_listened_to_on_single_day(callMeBaby(mbid1, username1),5)
        
        fig2 = go.Figure()


        fig2 = px.bar(df2, x="Count", y="Song", color='User', orientation='h')  
        fig2.update_layout(title='Daily Top Songs of last 5 Days')
        
        graph_website2 = html.Div(children=[
                    
            html.Br(),
            dcc.Graph(
                        id='example-graph5',
                        figure=fig2
                    )
        ])

        return graph_website2
    return ''



#### USE top_songs_MONTH(loadData(users)) FROM VisualizeShit
@callback(
    Output('my_div9999', 'children'),
    #Input('button3', 'n_clicks'),
    Input('opt_dropdown', 'value'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(month, mbid1, username1, mbid2, username2):
    if TEST:

        df9999 = top_songs_per_MONTH(callMeBaby(mbid1, username1))
        df9999 = df9999.loc[df9999['Date_month'] == month]    
        fig9999 = go.Figure()
        fig9999 = px.bar(df9999, x="Count", y="Song", orientation='h')   
        fig9999.update_layout(title='Top Songs per MONTH')

        graph_website9999 = html.Div(children=[
                        
                html.Br(),
                dcc.Graph(
                            id='example-graph9999',
                            figure=fig9999
                        )
            ])


        return graph_website9999
    return ''



#### 
@callback(
    Output('my_div666', 'children'),
    #Input('button3', 'n_clicks'),
    Input('opt_dropdown', 'value'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data'),
    #, prevent_initial_call=True
)
def update_output_div(month, mbid1, username1, mbid2, username2):

    print('mbid1, username1', mbid1, username1, '\n') 
    print('mbid2, username2', mbid2, username2)

    #top_unlistened_to_songs(loadData(users))


    #print('callMeBaby(mbid1, username1)', '\n', callMeBaby(mbid1, username1))
    #print('callMeBaby(mbid2, username2)', '\n', callMeBaby(mbid2, username2))


    df1 = callMeBaby(mbid1, username1)
    df2 = callMeBaby(mbid2, username2)

    df3 = pd.concat([df1, df2], axis=0)
       

    df = top_unlistened_to_songs(df3)

    #print('df3', '\n', df3)
    
    df = df.loc[df['Date_month'] == month] 

    fig666 = go.Figure()


    fig666 = px.bar(df, x="Count", y="Song", color='User', orientation='h')  
    fig666.update_layout(title='xxx')
    
    graph_website666 = html.Div(children=[
                
        html.Br(),
        dcc.Graph(
                    id='example-graph666',
                    figure=fig666
                )
    ])

    return graph_website666
