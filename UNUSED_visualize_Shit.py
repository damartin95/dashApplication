'''
Created on 21 Apr 2022

@author: danielmartin
'''


from lastfmAPI import loadData_throughCSV
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#pd.set_option('display.max_rows', None)


import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime





def loadData(users):
    df = pd.DataFrame(loadData_throughCSV(users))
    
    return df



#listened to the first time!
#


def top_listened_to_artists(df): ### ONLY APPLICABLE FOR ONE USER
    
    top_x = 20
    
    top_artists = df.groupby(df.Artist).Song.count()
    
    df_top_artists = top_artists.to_frame()
    
    df_top_artists.columns=['Count']
    
    df_top_artists = df_top_artists.sort_values(by='Count', ascending=False)
    
    print(df_top_artists.iloc[:top_x])
    
    return


def top_listened_to_songs(df): ### ONLY APPLICABLE FOR ONE USER
    
       
    top_x = 20
    
    top_artists = df.groupby(df.Song).Song.count()
    
    df_top_artists = top_artists.to_frame()
    
    df_top_artists.columns=['Count']
    
    df_top_artists = df_top_artists.sort_values(by='Count', ascending=False)
    
    print(df_top_artists.iloc[:top_x])
    
    return   


def top_songs_MONTH(df): ### ONLY APPLICABLE FOR ONE USER
    
    print('--- TOP SONGS PER MONTH ---' + '\n')
    
    
    df.Date = pd.to_datetime(df.Date)
    df['Date_month'] = df.Date.dt.to_period("M")
    
    grouped = df.groupby(['Date_month', 'Song']).size()    
    grouped = grouped.to_frame()
    grouped.columns = ['Count']
    
    grouped = grouped.groupby(['Date_month'])['Count'].nlargest(5)
    
    print(grouped, '\n')
    
    return


def most_listened_to_on_single_day_top_10_days(df): ### works for one and two users!
  
    print('--- MOST LISTENED TO SONGS ON A SINGLE DAY ---' + '\n')
    
    df.Date = pd.to_datetime(df.Date)
    df['Date_day'] = df.Date.dt.to_period("D")
    df2 = df.groupby(['User', 'Date_day', 'Song']).size()  
        
    df3 = df2.to_frame()
    df3.columns = ['Count']

    df4 = pd.DataFrame({'Count' : df.groupby(['User', 'Date_day', 'Song', 'Artist']).size()}).reset_index()
    df4 = df4.sort_values(by='Count', ascending=False)
    df4=df4.reindex(columns=['Date_day', 'Song', 'Artist', 'Count', 'User']).reset_index(drop=True)
    
    
    print(df4.head(10), '\n')
    

    return



def last_x_days_most_listened_to_on_single_day(df, xdays): ### works for one and two users!
  
    print('--- MOST LISTENED TO SONGS ON A SINGLE DAY ---' + '\n')
    
    ### YOU CAN COMPARE
    #2022-10-11 22:13:00 (<class 'pandas._libs.tslibs.timestamps.Timestamp'>)
    #2022-10-01 22:42:44.152733 (<class 'datetime.datetime'>)
    
    df.Date = pd.to_datetime(df.Date)  
    xDaysAgoDate = datetime.datetime.now() - datetime.timedelta(days = 9)
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
    
    
    print(df4.head(10), '\n')
    

    return


def plot_timeline_MONTH(df): ### works!
    
    print('--- xxx ---')
    
    
    
    df_single = df

    
    
    df_single.loc[:, 'Date'] = pd.to_datetime(df_single.Date)
    df_single.loc[:, 'Date_month'] = df_single.Date.dt.to_period("D")
                
            
    ChbyYear = df_single.groupby(df_single.Date_month).Song.count()
    df_Year=ChbyYear.to_frame()    
    
    
    print(type(df_single))
    print(df_single.head(3))
    
    
    #print('df_single[User][1] ', )
    
    
    df_Year['User']= df_single['User'].iloc[0]
    
    
    
    df_Year['Year']= ChbyYear.index    
    df_Year['Year'] = df_Year['Year'].astype(str)
    df_Year.reset_index(drop=True, inplace=True)

    
    
    
        
   
    fig = px.line(df_Year, x = 'Year', y = 'Song', color = 'User')
    fig.update_traces(mode='markers+lines')
    
    
    df_Year.to_csv('df_all.csv')
    


    return fig


def plot_timeline_YEAR(df): ### does not work (8 Oct 22) ### USE plot_timeline_MONTH as this function is currently not able to process data for two users
    
    ChbyYear=df.groupby(df.Year).Song.count()
    df_Year=ChbyYear.to_frame()
    df_Year['User']= 'wuhuspringfield'
    df_Year['Year']= ChbyYear.index
    df_Year.reset_index(drop=True, inplace=True)

    print(df_Year.head())
    
    plt.subplots(figsize=(20,7))
    plt.title('Scrobbling trend throughout the years', fontsize = 20) 
    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Scrobbling', fontsize=16)
    sns.set_style("darkgrid")
    sns.despine()
    sns.lineplot(data=df_Year,
                x="Year", 
                y="Song",
                hue="User",
                style="User",
                markers=True, dashes=False)

    plt.show()


def plot_timeline_SONG(dfs): ### works
    
    ## TO-DO - fill in entries with zeros for days with no plays
    
    df_filtered = list()
    
    for df in dfs:
        #print('\n\n\n------ NEW df -----\n')
        
        df_new = df.loc[df['Song'] == 'DITTO'].copy()
        
        
        df_filtered.append(df_new)
        
    
    plot_timeline_MONTH(df_filtered)
    
    return

    



users = [
         ['835defa77f6078c7a34c3c6ba04854c6', 'wuhuspringfield']
         , ['ab8ab5b6deefd7b8afa5c1adab89fcb8', 'feybmertn']
         ]




#last_x_days_most_listened_to_on_single_day(loadData(users), 10)

most_listened_to_on_single_day_top_10_days(loadData(users))




