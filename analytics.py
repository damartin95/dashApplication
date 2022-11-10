

import pandas as pd
import datetime
from dataloader import *




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

    loadData_throughCSV([name1, name2])


def mostRecentSong(df):

    return_string = (str('Dis bisch listened to ' + df['Song'][0] + ' by ' + df['Artist'][0]))
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