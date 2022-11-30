

import pandas as pd
import datetime
from dataloader import *




def a_scrobblesOverTime(df, timefilter): ### works!
    

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



def a_mostRecentSong(df):
    return_string = (str('Dis bisch ' + df['User'][0] + ' listened to ' + df['Song'][0] + ' by ' + df['Artist'][0]) + '.')
    return return_string


def a_topSongsxDays(df, xdays): ### works for one and two users!
  
    #print('--- MOST LISTENED TO SONGS ON A SINGLE DAY ---' + '\n')
    
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
    
    #print(df3)
    
    
   
    df4 = pd.DataFrame({'Count' : df.groupby(['User', 'Date_day', 'Song', 'Artist']).size()}).reset_index()
    df4 = df4.sort_values(by='Count', ascending=False)
    df4=df4.reindex(columns=['Date_day', 'Song', 'Artist', 'Count', 'User']).reset_index(drop=True)
    
    
    df4 = df4.drop_duplicates(subset=['Date_day', 'User'], keep='first')
    df4 = df4.sort_values(by=['User', 'Date_day'], ascending=True)
    
    
    #print(df4.head(xdays), '\n')
    

    return df4.head(xdays)


def a_topSongs(df): 
        
    df.Date = pd.to_datetime(df.Date)
    grouped = df.groupby(['User', 'Artist', 'Song']).size() 
    grouped = grouped.to_frame()
    grouped.columns = ['Count']
    grouped = grouped.reset_index()
    grouped = grouped.groupby(['User']).apply(lambda x: x.nlargest(5,'Count')).reset_index(level=0, drop=True)
    


    return grouped


def a_topUnlistenedSongs(df): 
     


    df.Date = pd.to_datetime(df.Date)
    #df['Date_month'] = df.Date.dt.to_period("M")
    grouped = df.groupby(['User', 'Year', 'Month', 'Artist', 'Song']).size()    
    grouped = grouped.to_frame()
    grouped.columns = ['Count']

    grouped = grouped.reset_index()

    #print('grouped before', '\n', grouped)

    grouped = grouped.drop_duplicates(['Artist','Song'], keep=False)
    grouped = grouped.groupby(['User', 'Year', 'Month']).apply(lambda x: x.nlargest(5,'Count')).reset_index(level=0, drop=True)
    
    grouped.to_csv('grouped.csv')

    return grouped



def a_scrobbleSearch(df, artist, album, song):




    '''
    df_single.Date.dt.to_period(timefilterCapital)
                
    ChbyYear = df_single.groupby(df_single.Date_month).Song.count()
    df_Year=ChbyYear.to_frame()    
    
    
    #print('df_single[User][1] ', )
    
    
    df_Year['User']= df_single['User'].iloc[0]
    
    
    df_Year['Year']= ChbyYear.index    
    df_Year['Year'] = df_Year['Year'].astype(str)
    df_Year.reset_index(drop=True, inplace=True)
    '''




    

    df['Date_month'] = df.Date.dt.to_period('M')
    df['Date_month'] = df['Date_month'].astype(str)

    groupby_objects = ['Date_month', 'Artist']


    df_isin = df[df['Artist'].isin([artist])]
     
    if album != '/':
        groupby_objects.append('Album')
        df_isin = df[df['Album'].isin([album])]

    if song != '/':
        groupby_objects.append('Song')
        df_isin = df[df['Song'].isin([song])]

    #print('groupby_objects', '\n', groupby_objects)

    #print('df before', '\n', df)

    df = df_isin.groupby(groupby_objects).size()    
    df = df.to_frame()
    df.columns = ['Count']
    df = df.reset_index()

    #print('df after', '\n', df)





    return df


'''
mbid1='835defa77f6078c7a34c3c6ba04854c6' 
username1='wuhuspringfield'


df_user1 = loadData_throughCSV([[mbid1, username1]])
a_scrobbleSearch(df_user1)
'''