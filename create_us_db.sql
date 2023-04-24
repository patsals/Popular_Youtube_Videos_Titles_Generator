--DROP TABLE IF EXISTS youtube_videos_us;

CREATE TABLE IF NOT EXISTS youtube_videos_us(
    id VARCHAR(20) PRIMARY KEY,
    date_popular DATE,
    date_published DATE,
    title VARCHAR(250),
    channel_name VARCHAR(20),
    views INTEGER,
    likes INTEGER,
    comments INTEGER,
    description VARCHAR(1000)
);