#! /bin/bash

#log our ETL processes
printf "ETL job executed at: %s\n" "$(date)">> /mnt/c/users/prsal/desktop/popular_youtube_videos_titles_generator/log.txt

#run our etl process
python3 /mnt/c/users/prsal/desktop/popular_youtube_videos_titles_generator/etl.py >> /mnt/c/users/prsal/desktop/popular_youtube_videos_titles_generator/log.txt

