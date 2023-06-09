import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """_summary_
    this method read song file and add song and artist data to
    postgres database using cusror

    Args:
        cur (cursor): postgres cursor using for insert song and artist data 
        filepath (string): destination of json song file to process
    """
    # open song file
    df = pd.read_json(filepath,lines=True)
   
    # insert song record
    song_data = df[["song_id","title","artist_id","year","duration"]].values.flatten().tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[["artist_id","artist_name","artist_location","artist_latitude","artist_longitude"]].values.flatten().tolist()
    cur.execute(artist_table_insert, artist_data)
    


def process_log_file(cur, filepath):
    """_summary_
    this method read log file and add time,users data to dimensions tables ,
    also add songplay data to Fact table using cusror

    Args:
        cur (cursor): postgres cursor using for insert time,users dimensions tables and songplays fact table
        filepath (string): destination of json log file to process
    """
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']
    # convert timestamp column to datetime
    time_df=pd.DataFrame(columns=['start_time','hour','day','week','month','year','weekday'])
    time_df['start_time']=pd.to_datetime(df['ts'],unit='ms')
    time_df['hour']=time_df['start_time'].dt.hour
    time_df['day']=time_df['start_time'].dt.day
    time_df['week']=time_df['start_time'].dt.isocalendar().week
    time_df['month']=time_df['start_time'].dt.month
    time_df['year']=time_df['start_time'].dt.year
    time_df['weekday']=time_df['start_time'].dt.weekday
    
    # insert time data records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId","firstName","lastName","gender","level"]]
    
    
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    df['ts']=pd.to_datetime(df['ts'],unit='ms')
    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """_summary_
    This is general method using to process file by file for song_file and log_file and apply method accordingly process_song_file for song_file and process_log_file for log_file 
, extracting the intrested data and save to database using cursor and connection

    Args:
        cur (cursor): postgres cursor
        conn (connectionstring): connectionstring for postgrers database
        filepath (string): destination of json file to process
        func (method): method to apply (process_song_file or process_log_file)
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """_summary_
    main entry point for varaible initialization , open connection , get cursor and calling process_data method for song and log folders
    """
    #connectionstring"host=127.0.0.1 dbname=sparkifydb user=student password=student"
    connectionstring="host=song-abdsaf.postgres.database.azure.com port=5432 dbname=sparkifydb user=abdsaf password=fasdba123! sslmode=require"

    conn = psycopg2.connect(connectionstring)
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()