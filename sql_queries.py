# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay ; "
user_table_drop = "DROP TABLE IF EXISTS songuser ; "
song_table_drop = "DROP TABLE IF EXISTS song ; "
artist_table_drop = "DROP TABLE IF EXISTS songartist ; "
time_table_drop = "DROP TABLE IF EXISTS songtime ;"

# CREATE TABLES



user_table_create = ("""
CREATE TABLE IF NOT EXISTS songuser 
(
user_id int primary key, 
first_name varchar, 
last_name varchar, 
gender char(1), 
level varchar
) ;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS song 
(
song_id varchar not null primary key, 
title varchar not null, 
artist_id varchar not null, 
year int, 
duration numeric not null
) ;
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS songartist 
(
artist_id varchar not null primary key, 
name varchar not null, 
location varchar, 
latitude numeric, 
longitude numeric
) ;
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS songtime 
(
start_time TIMESTAMP primary key, 
hour int, 
day int, 
week int, 
month int, 
year int, 
weekday int
);
""")
                     
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplay 
(
songplay_id SERIAL not null primary key, 
start_time TIMESTAMP not null REFERENCES songtime (start_time), 
user_id int not null REFERENCES songuser (user_id),
level varchar, 
song_id varchar REFERENCES song (song_id), 
artist_id varchar REFERENCES songartist (artist_id), 
session_id int ,
location varchar, 
user_agent varchar
) ;
""")

# INSERT RECORDS

songplay_table_insert = (""" 
insert into songplay 
(start_time,  user_id , level , song_id , artist_id , session_id  ,location , user_agent ) 
VALUES (%s, %s, %s,%s, %s, %s,%s, %s) 
ON CONFLICT(songplay_id) 
DO NOTHING ;
""")

user_table_insert = (""" 
insert into songuser (user_id, first_name , last_name , gender , level )
VALUES (%s, %s, %s,%s, %s) 
ON CONFLICT (user_id) 
DO UPDATE SET level = excluded.level ; 
""")

song_table_insert = (""" 
insert into song (song_id , title , artist_id , year , duration ) 
VALUES (%s, %s, %s,%s, %s) 
ON CONFLICT(song_id) 
DO NOTHING ;
""")

artist_table_insert = (""" 
insert into songartist (artist_id , name , location , latitude , longitude )
VALUES (%s, %s, %s,%s, %s) 
ON CONFLICT(artist_id) 
DO NOTHING;
""")


time_table_insert = (""" 
insert into songtime (start_time , hour , day , week , month , year , weekday )
VALUES (%s, %s, %s,%s, %s,%s, %s) 
ON CONFLICT(start_time) 
DO NOTHING;
""")

# FIND SONGS

song_select = (""" 
select 
    song.song_id,
    songartist.artist_id
    
from 
song join songartist 
    on song.artist_id=songartist.artist_id  
where 
    song.title=%s 
    and 
    songartist.name=%s 
    and 
    song.duration=%s
""")

# QUERY LISTS

create_table_queries = [ user_table_create, song_table_create, artist_table_create, time_table_create,songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]