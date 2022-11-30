
import pandas as pd
import plotly.graph_objects as go
from dash import callback, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
#from dash.exceptions import PreventUpdate
import plotly.express as px
import json


from analytics import *


TEST_scrobbles_over_time = True
TEST_most_recently_listened_to_songs = True
TEST_top_Songs = True
TEST_top_unlistened_Songs = True
TEST_topSongsxDays = True
TEST_scrobbleSearch = True



style_dcc_dropDown = {'width':'100px', 'border-width':'2px','border-color':'#a0a3a2'}
style_dcc_dropDown_wide = {'width':'300px', 'border-width':'2px','border-color':'#a0a3a2'}

style_dbc_Container = {'border-style': 'solid', 'border-width': '5px', 'border-color':'#a0a3a2'}#,'border-color':'#a0a3a2'}



layout = dbc.Container([
        
    dcc.Store(id='df_user1'),
    dcc.Store(id='df_user2'),

    html.Br(),

    #Most recently listened to songs
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Most recently listened to songs ...")),
        html.Br(),
        html.Div(id='div_most_recently_listened_to_songs', 
            style={"display": "flex", "justifyContent": "center"}),
        html.Br()
    ], style=style_dbc_Container),
    
    html.Br(),

    #Number of Scrobbles per ...
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Number of Scrobbles per ...")),
        html.Div(
            children=[
            dcc.Dropdown(
                ['Day', 'Week', 'Month', 'Year'],
                'Day',
                clearable=False,
                id = 'dropdown_timeperiod',
                searchable=False,
                style=style_dcc_dropDown
            ),], 
            style={"display": "flex", "justifyContent": "center"}
        ),
        html.Div(id='div_scrobbles_over_time'),  
        html.Br()      
    ], style=style_dbc_Container),

    html.Br(),

    #Top Songs per
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Top songs per ...")),
        
        html.Div(
            children=[
            dcc.Dropdown(
                id='dropdown_years1',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),

        html.Div(
            children=[
            dcc.Dropdown(
                id='dropdown_months1',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),



        html.Div(id='div_topSongs'),
        html.Br()  
    ], style=style_dbc_Container),

    html.Br(),

    #Top songs the other has missed per ...
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Top songs the other has missed per ...")),
        
        html.Div(
            children=[
            dcc.Dropdown(
                id='dropdown_years2',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),
        
        html.Div(
            children=[
            dcc.Dropdown(
                id='dropdown_months2',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),

        html.Div(
            children=[
                html.P('Once you have listened to that song on Spotify, it will disappear from this list forever - Make it count!'),
            ], style={"display": "flex", "justifyContent": "center"}
        ),

        html.Div(id='div_top_unlistened_songs_per_month'),
        html.Br()  
    ], style=style_dbc_Container),
            
    html.Br(),



    #Daily Top Songs of last x Days
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Top 20 songs per last days ...")),
        html.Div(
            children=[
            dcc.Dropdown(
                ['7', '30', '180', '360', '1000'],
                '7',
                clearable=False,
                id = 'dropdown_days',
                searchable=False,
                style=style_dcc_dropDown
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),
        html.Div(id='div_topSongsxDays'),
        html.Br()  
    ], style=style_dbc_Container),


    #Scrobble Search
    dbc.Container([   
        html.Br(),
        html.Center(html.H1("Search for your favorite scrobbles")),
        
        html.Div(
            children=[
            dcc.Dropdown(
                id='dropdown_search_artists',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown_wide
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),
        
        html.Div(
            children=[
                dcc.Dropdown(
                    id='dropdown_search_albums',
                    clearable=False,
                    searchable=False,
                    style=style_dcc_dropDown_wide
                ),],
            style={"display": "flex", "justifyContent": "center"}
        ),

        html.Div(
            children=[
                dcc.Dropdown(
                id='dropdown_search_songs',
                clearable=False,
                searchable=False,
                style=style_dcc_dropDown_wide
            ),],
            style={"display": "flex", "justifyContent": "center"}
        ),

        
        html.Div(id='div_scrobbleSearch'),
        html.Br()  
    ], style=style_dbc_Container),





])




@callback(
    Output('df_user1', 'data'),
    Output('df_user2', 'data'),
    Input('session_mbid1', 'data'),
    Input('session_username1', 'data'),
    Input('session_mbid2', 'data'),
    Input('session_username2', 'data')
)
def loadData(mbid1, username1, mbid2, username2):
    df_user1 = loadData_throughCSV([[mbid1, username1]])
    df_user1['Date'] = df_user1['Date'].astype('datetime64[ns]')
    
    df_user2 = loadData_throughCSV([[mbid2, username2]])
    df_user2['Date'] = df_user2['Date'].astype('datetime64[ns]')



    return json.dumps(df_user1.to_json()), json.dumps(df_user2.to_json())


   
@callback(
    Output('div_scrobbles_over_time', 'children'),
    Input('dropdown_timeperiod', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def scrobblesOverTime(timefilter, df1, df2):
    if TEST_scrobbles_over_time:

        df1 = pd.read_json(json.loads(df1))

        #print('df1.head(3)', '\n', df1.head(5))
        #print('df1-PAGE DATA.dtypes ', df1.dtypes)

        df2 = pd.read_json(json.loads(df2))
        username1 = df1['User'][0]
        username2 = df2['User'][0]

        df1 = a_scrobblesOverTime(df1, timefilter)
        df2 = a_scrobblesOverTime(df2, timefilter)

        fig = go.Figure()


        fig = fig.add_traces(go.Scatter(x = df1['Year'], y = df1['Song'], name=username1))
        fig = fig.add_traces(go.Scatter(x = df2['Year'], y = df2['Song'], name=username2))
        
        
        fig.update_traces(mode='markers+lines')
        fig.update_xaxes(categoryorder='category ascending') 
       
        
        graph_website = html.Div(children=[      
            dcc.Graph(
                        figure=fig
                    )
        ])

        return graph_website
    return ''
    


@callback(
    Output('div_most_recently_listened_to_songs', 'children'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def mostRecentSong(df1, df2):
    if TEST_most_recently_listened_to_songs:   
        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))

        output1 = a_mostRecentSong(df1)
        output2 = a_mostRecentSong(df2)
        graph_website = html.Div(children=[
            html.P(children=output1),
            html.P(children=output2)
        ])

        return graph_website
    return ''
    


@callback(
    Output('dropdown_years1', 'options'),
    Output('dropdown_years1', 'value'),
    Output('dropdown_years2', 'options'),
    Output('dropdown_years2', 'value'),
    Output('dropdown_months1', 'options'),
    Output('dropdown_months1', 'value'),
    Output('dropdown_months2', 'options'),
    Output('dropdown_months2', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def updateDropdownMonths(df1, df2):
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))

    df3 = pd.concat([df1, df2], axis=0)
    #df3.Date = pd.to_datetime(df3.Date)

    #print('df3.head(2)', '\n', df3.head(2))

    #df3_years = df3.Date.dt.to_period('Y')
    #print('df3_years', '\n', df3_years)

    #df3['Date_month'] = df3.Date.dt.to_period('M')

    df3_years = df3.loc[df3['Year'].notnull()]
    df3_years = df3_years['Year'].drop_duplicates().astype(str).tolist()
    df3_years.insert(0, '/')

    df3_months = df3.loc[df3['Month'].notnull()]
    df3_months = df3_months['Month'].drop_duplicates().astype(str).tolist()
    df3_months.insert(0, '/')

    
    return df3_years, df3_years[0], df3_years, df3_years[0], df3_months, df3_months[0], df3_months, df3_months[0]


@callback(
    Output('div_topSongs', 'children'),
    Input('dropdown_years1', 'value'),
    Input('dropdown_months1', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def topSongs(timeperiod_Y, timeperiod_M, df1, df2):
    if TEST_top_Songs:
        
        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))
        df3 = pd.concat([df1, df2], axis=0)


        if timeperiod_Y != '/':
            timeperiod_Y = int(timeperiod_Y)
            df3 = df3.loc[df3['Year'] == timeperiod_Y] 


        if timeperiod_M != '/':
            timeperiod_M = int(timeperiod_M)
            df3 = df3.loc[df3['Month'] == timeperiod_M]  

        df9999 = a_topSongs(df3)

        #print('df9999', '\n', df9999)

         

        #print('df9999', '\n', df9999)
        #print('df9999[Count]', '\n', df9999['Count'])
        #print('df9999[Song]', '\n', df9999['Song'])
        #print('type(df9999)', '\n', type(df9999))
    
        fig9999 = go.Figure()
        fig9999 = px.bar(df9999, x="Count", y="Song", color='User', orientation='h')   

        df9999_yaxes_ticktext = df9999['Artist'] + ' - ' + df9999['Song']
        fig9999.update_yaxes(ticktext=df9999_yaxes_ticktext, tickvals=df9999['Song'])
        fig9999.update_xaxes(categoryorder='category descending') 

        
        graph_website9999 = html.Div(children=[
            dcc.Graph(
                figure=fig9999
            )
        ])

        return graph_website9999
    return ''



@callback(
    Output('div_top_unlistened_songs_per_month', 'children'),
    Input('dropdown_years2', 'value'),
    Input('dropdown_months2', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def topUlistenedSongs(timeperiod_Y, timeperiod_M, df1, df2):
    if TEST_top_unlistened_Songs:
        
        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))
        df3 = pd.concat([df1, df2], axis=0)

          
        
        df = a_topUnlistenedSongs(df3)

        if timeperiod_Y != '/':
            timeperiod_Y = int(timeperiod_Y)
            df = df.loc[df['Year'] == timeperiod_Y] 

        if timeperiod_M != '/':
            timeperiod_M = int(timeperiod_M)
            df = df.loc[df['Month'] == timeperiod_M]
        else:
            #print('df before', '\n', df)
            df = df.groupby(['User']).apply(lambda x: x.nlargest(5,'Count')).reset_index(level=0, drop=True)
            #print('df after', '\n', df)
            


        #print('df', '\n', df)
        #print('type(df)', '\n', type(df))

        
        #print('df', '\n', df)

        fig666 = go.Figure()
        fig666 = px.bar(df, x="Count", y="Song", color='User', orientation='h') 

        df_yaxes_ticktext = df['Artist'] + ' - ' + df['Song']
        fig666.update_yaxes(ticktext=df_yaxes_ticktext, tickvals=df['Song'])
        fig666.update_xaxes(categoryorder='category ascending') 

        
        graph_website666 = html.Div(children=[          
            html.Br(),
            dcc.Graph(
                        figure=fig666
                    )
        ])

        return graph_website666
    return ''





#ONE USER ONLY!
@callback(
    Output('div_topSongsxDays', 'children'),
    Input('dropdown_days', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def topSongsxDays(days, df1, df2): 
    if TEST_topSongsxDays:

        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))

        days = int(days)

        df1 = a_topSongsxDays(df1, days)
        df1 = df1.groupby(['User']).apply(lambda x: x.nlargest(20,'Count')).reset_index(level=0, drop=True)
            
        
        fig2 = go.Figure()
        fig2 = px.bar(df1, x="Count", y="Song", color='User', orientation='h')  

        df1_yaxes_ticktext = df1['Artist'] + ' - ' + df1['Song']
        fig2.update_yaxes(ticktext=df1_yaxes_ticktext, tickvals=df1['Song'])
        #fig2.update_xaxes(categoryorder='category ascending') 
        
        graph_website2 = html.Div(children=[
                    
            html.Br(),
            dcc.Graph(
                        figure=fig2
                    )
        ])

        return graph_website2
    return ''




@callback(
    Output('dropdown_search_artists', 'options'),
    Output('dropdown_search_artists', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def updateDropdownSearchArtists(df1, df2):
    
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))

    df3 = pd.concat([df1, df2], axis=0)


    df3 = df3.groupby(['Artist']).size().nlargest(20)   

    #print('df3 - top 20 artists', '\n', df3)
    df3.to_csv('top20artists.csv')

    df3 = df3.to_frame()
    df3.columns = ['Count']

    df3 = df3.reset_index()

    df3 = df3.loc[df3['Artist'].notnull()]
    df3 = df3['Artist'].drop_duplicates().astype(str).tolist()
    #df3_months.insert(0, '/')
    
    return df3, df3[0]


@callback(
    Output('dropdown_search_albums', 'options'),
    Output('dropdown_search_albums', 'value'),
    Input('dropdown_search_artists', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def updateDropdownSearchArtists(artist, df1, df2):
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))

    df3 = pd.concat([df1, df2], axis=0)
    df3_isin = df3[df3['Artist'].isin([artist])]
    df3_albums = df3_isin.loc[df3_isin['Album'].notnull()]
    df3_albums = df3_albums['Album'].drop_duplicates().astype(str).tolist()
    df3_albums.insert(0, '/')
    
    
    return df3_albums, df3_albums[0] #, df3_songs, df3_songs[0]


@callback(
    Output('dropdown_search_songs', 'options'),
    Output('dropdown_search_songs', 'value'),
    Input('dropdown_search_artists', 'value'),
    Input('dropdown_search_albums', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def updateDropdownSearchArtists(artist, album, df1, df2):
    df1 = pd.read_json(json.loads(df1))
    df2 = pd.read_json(json.loads(df2))

    df3 = pd.concat([df1, df2], axis=0)
    df3_isin = df3[df3['Artist'].isin([artist])]

     
    if album != '/':
        df3_isin = df3[df3['Album'].isin([album])]

    
    df3_songs = df3_isin.loc[df3_isin['Song'].notnull()]
    df3_songs = df3_songs['Song'].drop_duplicates().astype(str).tolist()
    df3_songs.insert(0, '/')
    
    
    return df3_songs, df3_songs[0] #, df3_songs, df3_songs[0]



    #df3_songs = df3_isin.loc[df3_isin['Song'].notnull()]
    #df3_songs = df3_songs['Song'].drop_duplicates().astype(str).tolist()





@callback(
    Output('div_scrobbleSearch', 'children'),
    Input('dropdown_search_artists', 'value'),
    Input('dropdown_search_albums', 'value'),
    Input('dropdown_search_songs', 'value'),
    Input('df_user1', 'data'),
    Input('df_user2', 'data')
)
def scrobblesSearch(artist, album, song, df1, df2):
    if TEST_scrobbleSearch:

        df1 = pd.read_json(json.loads(df1))
        df2 = pd.read_json(json.loads(df2))
        username1 = df1['User'][0]
        username2 = df2['User'][0]

        

        df1 = a_scrobbleSearch(df1, artist, album, song)
        df2 = a_scrobbleSearch(df2, artist, album, song)

        #print('df1', '\n', df1)

        fig_ss = go.Figure()
        
    
        fig_ss = fig_ss.add_traces(go.Scatter(x = df1['Date_month'], y = df1['Count'], name=username1))
        fig_ss = fig_ss.add_traces(go.Scatter(x = df2['Date_month'], y = df2['Count'], name=username2))
        
        
        
        fig_ss.update_traces(mode='markers+lines')
        fig_ss.update_xaxes(categoryorder='category ascending') 
        #fig_ss.update_xaxes(dtick=1)
        
       
        
        graph_website = html.Div(children=[      
            dcc.Graph(
                        figure=fig_ss
                    )
        ])

        return graph_website

'''
mbid1='835defa77f6078c7a34c3c6ba04854c6' 
username1='wuhuspringfield'

mbid2='ab8ab5b6deefd7b8afa5c1adab89fcb8'
username2='feybmertn'


df1 = loadData_throughCSV([[mbid1, username1]])
df2 = loadData_throughCSV([[mbid2, username2]])

updateDropdownSearchArtists(df1, df2)'''