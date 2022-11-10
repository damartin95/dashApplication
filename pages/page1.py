
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import json

from analytics import *
from pages import page0

print('I am page1')


TEST = False

style_html_dropDown = {'width':'100px', 'border-width':'2px','border-color':'#a0a3a2'}





layout = dbc.Container([
    
    
    html.Center(html.H1("GEDULD IST (vorerst) EINE TUGEND")),
    

    #html.Div(id='dummy'),

    dcc.Store(id='df1'),
    dcc.Store(id='df2'),

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


    html.Div(id='my_div9999'),
    html.Div(id='my_div7'),
    html.Div(id='my_div8')
])







### LOAD DATA ONCE HERE!




@callback(
    Output('df1', 'data'),
    Output('df2', 'data'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data')
)
def loadData(mbid1, username1, mbid2, username2):
    print('AM I EVEN HERE?', '\n')


    df1 = callMeBaby(mbid1, username1).to_json()
    df2 = callMeBaby(mbid2, username2).to_json()

    return json.dumps(df1), json.dumps(df2)



@callback(
    Output('opt_dropdown', 'options'),
    Output('opt_dropdown', 'value'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def update_date_dropdown(df1, df2):
    print('What about here?', '\n')
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))

    df3 = pd.concat([df1, df2], axis=0)
    df3.Date = pd.to_datetime(df3.Date)
    df3['Date_month'] = df3.Date.dt.to_period("M")
    df3 = df3.loc[df3['Date_month'].notnull()]
    df3 = df3['Date_month'].drop_duplicates().astype(str).tolist()
    
    return df3, df3[0]



### OBVIOUSLY kann hier kein State(...) stehen, weil der Button nichts übergibt!
# MOST RECENTLY LISTENED TO SONG
@callback(
    Output('my_div5', 'children'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def most_recently_listened_to_songs(df1, df2): #n_clicks wird bei page-reload auf None gesetzt

    if TEST:   
    
        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))

        output1 = mostRecentSong(df1)
        output2 = mostRecentSong(df2)
        graph_website = html.Div(children=[
                    
            html.H2(children=output1),
            html.H2(children=output2)
        ])

        return graph_website
    return ''
    



#GRAPHICS    
@callback(
    Output('my_div6', 'children'),
    Input('song_per_day_dd', 'value'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def update_output_div(timefilter, df1, df2): #n_clicks wird bei page-reload auf None gesetzt
    if True:

        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))
        username1 = df1['User'][0]
        username2 = df2['User'][0]

        df1 = plot_timeline_MONTH(df1, timefilter)
        df2 = plot_timeline_MONTH(df2, timefilter)

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
    


'''ONLY ONE USER!!!!!!!!! '''
''' REDUNDANT?'''
@callback(
    Output('my_div7', 'children'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def top_songs_last_10_days(df1, df2): #n_clicks wird bei page-reload auf None gesetzt
   
    if TEST:

        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))

        df1 = most_listened_to_on_single_day_top_10_days(df1)
        

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



'''ONLY ONE USER'''
@callback(
    Output('my_div8', 'children'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def top_songs_last_x_days(df1, df2): #n_clicks wird bei page-reload auf None gesetzt
    if TEST:

        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))


        df1 = last_x_days_most_listened_to_on_single_day(df1,5)
        
        fig2 = go.Figure()


        fig2 = px.bar(df1, x="Count", y="Song", color='User', orientation='h')  
        fig2.update_layout(title='Daily Top Songs of last x Days')
        
        graph_website2 = html.Div(children=[
                    
            html.Br(),
            dcc.Graph(
                        id='example-graph5',
                        figure=fig2
                    )
        ])

        return graph_website2
    return ''



'''ONLY ONE USER'''
@callback(
    Output('my_div9999', 'children'),
    Input('opt_dropdown', 'value'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def top_songs_per_timeperiod(timeperiod_M, df1, df2):
    if True:
        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))

        df9999 = top_songs_per_MONTH(df1)
        df9999 = df9999.loc[df9999['Date_month'] == timeperiod_M]    
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
    Input('opt_dropdown', 'value'),
    Input('df1', 'data'),
    Input('df2', 'data')
)
def top_unlistened_songs(month, df1, df2):
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))
    df3 = pd.concat([df1, df2], axis=0)
       
    df = top_unlistened_to_songs(df3)
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




