

import requests
#import json
import numpy as np
import pandas as pd
import plotly.express as px
import datetime



USER_AGENT = 'Mozilla/5.0'




def lastfm_get(payload, user):
     
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'
    payload['api_key'] = user[0]
    payload['user'] = user[1]
    payload['format'] = 'json'
    
    response = requests.get(url, headers=headers, params=payload)
    
    return response


def callMeBaby(name1, name2):
    user = np.array(
             [name1, name2]
             #, ['ab8ab5b6deefd7b8afa5c1adab89fcb8', 'feybmertn']
             )
    page = 1
    limit = 500 #default: 500
    
    payload = {
                'method': 'user.getrecenttracks',
                'limit': limit,
                'page': page,
    }
    
    response = lastfm_get(payload, user)
    
    responses_df = []
    
        
    single_response_json = response.json()

    #print('single_response_json', '\n', single_response_json)

    single_response_track = single_response_json['recenttracks']['track']
        



    
    responses_df.append(single_response_track)
    
    
    r0_df = pd.concat([pd.DataFrame(i) for i in responses_df], ignore_index=True)
    

    
    
    
    if 1==1:
        r0_df = r0_df.drop('image', axis=1)
        r0_df = r0_df.drop('streamable', axis=1)
        r0_df = r0_df.drop('url', axis=1)
        #r0_df = r0_df.drop('mbid', axis=1) # musicbrainz id = unique identifier
        r0_df['artist'] = r0_df.artist.astype(str)
        r0_df['album'] = r0_df.album.astype(str)
        r0_df['date'] = r0_df.date.astype(str)
        
        r0_df[['mbid2','new_artist']]=r0_df['artist'].str.split("#text':", n = 1, expand = True)
        r0_df = r0_df.drop('mbid2', axis=1)
        r0_df = r0_df.drop('artist', axis=1)
        
        r0_df[['mbid3','new_album']]=r0_df['album'].str.split("#text':", n = 1, expand = True)
        r0_df = r0_df.drop('mbid3', axis=1)
        r0_df = r0_df.drop('album', axis=1)
        r0_df[['uts','new_date']]=r0_df['date'].str.split("#text':", n = 1, expand = True)
        r0_df = r0_df.drop('date', axis=1)
        
        r0_df = r0_df.drop('uts', axis=1) ## UTS
        
        
        if '@attr' in r0_df.columns: 
            r0_df = r0_df.drop('@attr', axis=1) # this fucker only shows up when a song is being played
            r0_df = r0_df.iloc[1:] # removed the top row as it contains None in its 'Date' column
            r0_df = r0_df.reset_index(drop=True)
    
        r0_df['new_artist'] = r0_df['new_artist'].str[2:-2]
        r0_df['new_album'] = r0_df['new_album'].str[2:-2]
        r0_df['new_date'] = r0_df['new_date'].str[2:-2]
    
    
        #r0_df = r0_df.fillna(value=np.nan)
        
        

    
       
    if 1==1: # PREPARE DATES
        r0_df['Date'] = pd.to_datetime(r0_df['new_date'])
        r0_df = r0_df.drop('new_date', axis=1)  
        
        #print(r0_df.head())
        
        r0_df['Year'] = pd.DatetimeIndex(r0_df['Date']).year
        r0_df['Month'] = pd.DatetimeIndex(r0_df['Date']).month

    r0_df['User'] = user[1]     
      
    r0_df.columns=['mbid', 'Song','Artist','Album','Date', 'Year', 'Month', 'User']
    
    
    return r0_df


def plot_timeline_MONTH(df, timefilter): ### works!
    
    print('timefilter ', timefilter)

    timefilterCapital = timefilter[0]

    df_single = df   
    df_single.loc[:, 'Date'] = pd.to_datetime(df_single.Date)
    df_single.loc[:, 'Date_month'] = df_single.Date.dt.to_period(timefilterCapital)
                
    ChbyYear = df_single.groupby(df_single.Date_month).Song.count()
    df_Year=ChbyYear.to_frame()    
    
    
    #print('df_single[User][1] ', )
    
    
    df_Year['User']= df_single['User'].iloc[0]
    
    
    df_Year['Year']= ChbyYear.index    
    df_Year['Year'] = df_Year['Year'].astype(str)
    df_Year.reset_index(drop=True, inplace=True)

    
    df_Year.to_csv('df_all.csv')
    

    return df_Year



def returnNameCombination(name1, name2):

    r0_df = callMeBaby(name1, name2)
    return_string = (str('Dis bisch listened to ' + r0_df['Song'][0] + ' by ' + r0_df['Artist'][0]))

    return return_string



def most_listened_to_on_single_day_top_10_days(df): ### works for one and two users!
  
    #print('--- MOST LISTENED TO SONGS ON A SINGLE DAY ---' + '\n')
    
    df.Date = pd.to_datetime(df.Date)
    df['Date_day'] = df.Date.dt.to_period("D")
    df2 = df.groupby(['User', 'Date_day', 'Song']).size()  
        
    df3 = df2.to_frame()
    df3.columns = ['Count']

    df4 = pd.DataFrame({'Count' : df.groupby(['User', 'Date_day', 'Song', 'Artist']).size()}).reset_index()
    df4 = df4.sort_values(by='Count', ascending=False)
    df4=df4.reindex(columns=['Date_day', 'Song', 'Artist', 'Count', 'User']).reset_index(drop=True)
    
    
    #print(df4.head(10), '\n')
    return df4.head(10)


def last_x_days_most_listened_to_on_single_day(df, xdays): ### works for one and two users!
  
    print('--- MOST LISTENED TO SONGS ON A SINGLE DAY ---' + '\n')
    
    ### YOU CAN COMPARE
    #2022-10-11 22:13:00 (<class 'pandas._libs.tslibs.timestamps.Timestamp'>)
    #2022-10-01 22:42:44.152733 (<class 'datetime.datetime'>)
    
    df.Date = pd.to_datetime(df.Date)  
    xDaysAgoDate = datetime.datetime.now() - datetime.timedelta(days = xdays)
    df = df[df.Date > xDaysAgoDate]
    
    
    df['Date_day'] = df.Date.dt.to_period("D")
    

    df2 = df.groupby(['User', 'Date_day', 'Song']).size()  
    
    
        
    df3 = df2.to_frame()
    df3.columns = ['Count']
    
    print(df3)
    
    
   
    df4 = pd.DataFrame({'Count' : df.groupby(['User', 'Date_day', 'Song', 'Artist']).size()}).reset_index()
    df4 = df4.sort_values(by='Count', ascending=False)
    df4=df4.reindex(columns=['Date_day', 'Song', 'Artist', 'Count', 'User']).reset_index(drop=True)
    
    
    df4 = df4.drop_duplicates(subset=['Date_day', 'User'], keep='first')
    df4 = df4.sort_values(by=['User', 'Date_day'], ascending=True)
    
    
    print(df4.head(xdays), '\n')
    

    return df4.head(xdays)



def top_songs_per_MONTH(df): ### ONLY APPLICABLE FOR ONE USER
    
    #print('--- TOP SONGS PER MONTH ---' + '\n')
    
    df.Date = pd.to_datetime(df.Date)
    df['Date_month'] = df.Date.dt.to_period("M")
    grouped = df.groupby(['Date_month', 'Song']).size()    
    grouped = grouped.to_frame()
    grouped.columns = ['Count']
    grouped = grouped.groupby(['Date_month']).apply(lambda x: x.nlargest(5,'Count')).reset_index(level=0, drop=True)
    grouped.reset_index(inplace=True)
    
    #print('grouped in function', '\n', grouped)

    return grouped



def top_unlistened_to_songs(df): ### ONLY APPLICABLE FOR ONE USER
    
    #print('--- SONGS THAT SKIPPED ON US ---' + '\n')
    
    df.Date = pd.to_datetime(df.Date)
    df['Date_month'] = df.Date.dt.to_period("M")
    grouped = df.groupby(['User', 'Date_month', 'Artist', 'Song']).size()    
    grouped = grouped.to_frame()
    grouped.columns = ['Count']

    grouped = grouped.reset_index()

    #print('grouped before', '\n', grouped)

    grouped = grouped.drop_duplicates(['Artist','Song'], keep=False)

    grouped = grouped.groupby(['User', 'Date_month']).apply(lambda x: x.nlargest(5,'Count')).reset_index(level=0, drop=True)
    
    
    #grouped.reset_index(inplace=True) ### might be not needed!
    #grouped.to_csv('grouped_keep_false_groupby_user.csv')

    #print('grouped', '\n', grouped)

    return grouped