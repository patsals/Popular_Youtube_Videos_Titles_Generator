import json
from googleapiclient.discovery import build
import pandas as pd
import sqlite3 as db
from datetime import date

API_KEY = "AIzaSyDqitOoj1fCMdzUHapDY358e5Ys4_yN4Os"
PATH = '/mnt/c/users/prsal/desktop/popular_youtube_videos_titles_generator/'
json_file_name = PATH + "mostPopularVideosByCountry.json"
db_file_name = PATH + 'popular_youtube_videos.db'



def extract_json_data(country, country_code):
    youtube = build('youtube', 'v3', developerKey= API_KEY)
    countryDict = {}
    with open(json_file_name, "w") as outfile:
        request = youtube.videos().list(part='snippet,contentDetails,statistics',
                                        chart= 'mostPopular', regionCode = country_code,
                                        maxResults= 100)
        response = request.execute()
        countryDict[country] = response
        json.dump(countryDict, outfile, indent= 4)


def transform_json_to_df(country):
    with open(json_file_name) as infile:
        data = json.load(infile)
        df_records = []
        for video in data[country]['items']:
            try:
                temp_df = pd.DataFrame(
                    {"id": video["id"], 
                     "date_popular": [date.today()], 
                     "date_published": [video['snippet']['publishedAt'].split('T')[0]],
                     "title": [video["snippet"]["title"]],
                     'channel_name': [video['snippet']['title']],
                     "views": [video["statistics"]["viewCount"]],
                     "likes": [video["statistics"]["likeCount"]], 
                     "comments": [video["statistics"]["commentCount"]],
                     "description": [video['snippet']['description']]})
            except KeyError as e:
                if str(e) == "\'likeCount\'":
                    temp_df = pd.DataFrame(
                        {"id": video["id"], 
                         "date_popular": [date.today()], 
                        "date_published": [video['snippet']['publishedAt'].split('T')[0]],
                        "title": [video["snippet"]["title"]],
                         'channel_name': [video['snippet']['title']],
                         "views": [video["statistics"]["viewCount"]],
                         "likes": [video["statistics"]["favoriteCount"]], 
                         "comments": [video["statistics"]["commentCount"]],
                         "description": [video['snippet']['description']]})
                elif str(e) == "\'commentCount\'":
                    temp_df = pd.DataFrame(
                        {"id": video["id"], 
                         "date_popular": [date.today()], 
                         "date_published": [video['snippet']['publishedAt'].split('T')[0]],
                         "title": [video["snippet"]["title"]],
                         'channel_name': [video['snippet']['title']],
                         "views": [video["statistics"]["viewCount"]],
                         "likes": [video["statistics"]["likeCount"]], 
                         "comments": [0],
                         "description": [video['snippet']['description']]})
            df_records.append(temp_df)

        df = pd.concat(df_records)
    return df

def load_df_to_db(df):
    conn = db.connect(db_file_name)
    cur = conn.cursor()
    query = 'SELECT COUNT(*) FROM youtube_videos_us'
    cur.execute(query)
    print('\'youtube_videos_us\' table size before load:', cur.fetchone()[0])

    df.to_sql('youtube_videos_us', conn, if_exists='replace', index=False)

    query = 'SELECT COUNT(*) FROM youtube_videos_us'
    cur.execute(query)
    print('\'youtube_videos_us\' table size after load:', cur.fetchone()[0])

    conn.close()



if __name__ == '__main__':
    extract_json_data('United States', 'US')
    dataframe = transform_json_to_df('United States')
    load_df_to_db(dataframe)