
import requests
import time
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
from datetime import date
from os.path import exists



TEST = False


def create_FILENAME(username):
    FILENAME = 'dataset_' + username + '.csv'
    return FILENAME


def loadData_throughAPI(user, page, b_exists): ## NEVER CALL IT DIRECTLY (as loadData_throughCSV will use this function if a file does not exist yet)
    #print('in API')
    df_all = pd.DataFrame()

    FILENAME = create_FILENAME(user[1])

    responses = []
    total_pages = 3  
    limit = 500

    if b_exists: total_pages = page
     
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
        
        #page = int(response.json()['recenttracks']['@attr']['page']) 
        
        
        if TEST: 
            total_pages = 3
        else:
            if not(b_exists):
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
        #print(r0_df)
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
         
      
    r0_df.columns=['mbid', 'Song', 'Artist', 'Album', 'Date', 'Year', 'Month']
                

    
    
    df_all = df_all.append(r0_df)


    '''IMPORTANT!'''
    #print('df_all.iloc[0]', '\n', df_all.iloc[:1]['Date']=='2022-11-13 20:49:00')


    return df_all



def loadData_throughCSV(users):
    
    user = users[0]
    
    
    FILENAME = create_FILENAME(user[1])
    page = 1

    df_tmp = pd.DataFrame()
    
    if exists(FILENAME): 
        #print('it exists')

        b_exists = True
        b_tmp = True
        

        df = pd.read_csv(FILENAME, sep=',', index_col=0) #, dtype='string')
        

        while b_tmp:
            #print('while b_tmp')
            df_API = loadData_throughAPI(user, page, b_exists)
            print('df.iloc[0][Date] >> ', df.iloc[0]['Date'])
            np_where = (np.where(df_API['Date'] == df.iloc[0]['Date']))

            #print('np_where ', np_where)


            if len(np.where(df_API['Date'] == df.iloc[0]['Date'])[0]) == 0:
                #print('if len')

                df_tmp = pd.concat([df_tmp, df_API], axis=0).reset_index(drop=True)
                


            else:  
                #print('else len')
                df_API_new = df_API[0:np_where[0][0]]

                df_tmp = pd.concat([df_tmp, df_API_new], axis=0).reset_index(drop=True)
            
                b_tmp = False

            #print('df_tmp.dtypes ', df_tmp.dtypes)

            #df_API_new = df_API[0:np_where]

            #df_API_new.to_csv('df_API_new.csv')
            #df.to_csv('df.csv')

            #df3_tmp = pd.concat([df_tmp, df_API_new], axis=0).reset_index()
            #df3_tmp.to_csv('df3_tmp.csv')

            page = page + 1


        #df_tmp.to_csv('df_tmp.csv')

        '''df_tmp = []
        i = 0

        #np_where_bool = (len(np.where(df_API['Date'] == df.iloc[0]['Date'])[0]) == 0)

        while len(np.where(df_API['Date'] == df.iloc[0]['Date'])[0]) == 0:
            print('i: ', i) 
            print('first row CSV == first row API???')
            print(df.iloc[0]['Date']==df_API.iloc[0]['Date'])

            print(df.iloc[0]['Date'])

            print(df_API.iloc[0]['Date'])


            np_where = (np.where(df_API['Date'] == df.iloc[0]['Date']))
            


            df_API_new = df_API[0:np_where]

            df_API_new.to_csv('df_API_new.csv')
            df.to_csv('df.csv')

            df3_tmp = pd.concat([df_tmp, df_API_new], axis=0).reset_index()
            df3_tmp.to_csv('df3_tmp.csv')

            i = i+1

            print('i-ende: ', i)
        #df3.to_csv('df3.csv')

        #print(df_API_new)
    '''
    else:
        #print('it doesnt exist')

        b_exists = False

        df = loadData_throughAPI(user, page, b_exists)
    
    

    #print('df_tmp[1][Date]', ' ', df_tmp[:1]['Date'])
    #print('df_tmp', '\n', df_tmp)
      
    
    df_all = pd.concat([df_tmp, df], axis=0).reset_index(drop=True)
                   
    df_all['User'] = user[1] 

    #df_all['Date'] = df_all['Date'].astype('O')

    #print('df_all.head(5)', '\n', df_all.head(5))
    #print('df_all[1][Date]', ' ', df_all[:1]['Date'])
    #print('df_all[5][Date]', ' ', df_all[4:5]['Date'])

    

    df_all.to_csv(FILENAME)
    
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




#mbid1 = '835defa77f6078c7a34c3c6ba04854c6'
#username1 = 'wuhuspringfield'

#mbid2 = 'ab8ab5b6deefd7b8afa5c1adab89fcb8'
#username2 = 'feybmertn'


#loadData_throughCSV([[mbid1, username1]])


#print(loadData_throughAPI([mbid1, username1], 1, True))


