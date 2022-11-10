
import requests
import time
import numpy as np
import pandas as pd
from datetime import date
from os.path import exists



TEST = True


def create_FILENAME(username):
    FILENAME = 'dataset_' + username + '_' + date.today().strftime("%d-%m-%Y") + '.csv'
    return FILENAME


def loadData_throughAPI(user): ## NEVER CALL IT DIRECTLY (as loadData_throughCSV will use this function if a file does not exist yet)

    df_all = pd.DataFrame()

    
    
    
    FILENAME = create_FILENAME(user[1])

    responses = []
    page = 1
    total_pages = 3  
    limit = 500
     
    while page <= total_pages:
        
        payload = {
            'method': 'user.getrecenttracks',
            'limit': limit,
            'page': page,
        }
        print('user[1]', user[1])
        print("Requesting page {}/{} for {}".format(page, total_pages, user[1]))
        #clear_output(wait = True) ## This function apparently only works in Jupyter Notebooks
        
        response = lastfm_get(payload, user)
        responses.append(response)
        
        if response.status_code != 200:
            print('response.status_code != 200')
            print(response.text)
            break
        
        page = int(response.json()['recenttracks']['@attr']['page']) 
        
        
        if TEST: 
            total_pages = 3
        else:
            total_pages = int(response.json()['recenttracks']['@attr']['totalPages']) ## Only used for full runs
        
        
        if not getattr(response, 'from_cache', False):
            time.sleep(0.1)
        
        page += 1
    
    
    
    responses_df = []
    
    for single_response in responses:
        
        single_response_json = single_response.json()
        single_response_track = single_response_json['recenttracks']['track']
        
        
        responses_df.append(single_response_track)
    
    
    r0_df = pd.concat([pd.DataFrame(i) for i in responses_df], ignore_index=True)
    

    
    
    
    if 1==1:
        r0_df = r0_df.drop('image', axis=1)
        r0_df = r0_df.drop('streamable', axis=1)
        r0_df = r0_df.drop('url', axis=1)
        print(r0_df)
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
         
      
    r0_df.columns=['mbid', 'Song','Artist','Album','Date', 'Year', 'Month']
                

    r0_df.to_csv(FILENAME)
    
    df_all = df_all.append(r0_df)

    return df_all


def loadData_throughCSV(users):
    
    df_all = pd.DataFrame()
    
    
    
    for user in users:
        
        
        FILENAME = create_FILENAME(user[1])
        
        if exists(FILENAME): 
            df = pd.read_csv(FILENAME, sep=',', index_col=0) #, dtype='string')
            
        else:
            
            df = loadData_throughAPI(user)
        
        df['User'] = user[1] 
        df_all = df_all.append(df)
      
    
    
    return df_all


def lastfm_get(payload, user):
    USER_AGENT = 'Mozilla/5.0'
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

