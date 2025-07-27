from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from db_connection import insert_sentiment_data
import pandas as pd
from dotenv import load_dotenv
# load_dotenv()

# Initialize YouTube API
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def get_trending_videos(region_code="IN", max_results=10):
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": item["statistics"].get("viewCount"),
            "likes": item["statistics"].get("likeCount"),
            "published": item["snippet"]["publishedAt"]
        })
    return videos

data=[]

# Fetch top-level comments for a video
def get_video_comments(video_id, video_title, max_results=50):
    video_title_sentiment = analyzer.polarity_scores(video_title)
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    )
    response = request.execute()

    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        sentiment = analyzer.polarity_scores(comment)
        data.append({
            "post_title":video_title,
            "post_pos_sentiment": video_title_sentiment["pos"],
            "post_neg_sentiment": video_title_sentiment["neg"],
            "post_neu_sentiment": video_title_sentiment["neu"],
            "post_compound": video_title_sentiment["compound"],
            "comment":comment[:100],
            "comment_pos_sentiment": sentiment["pos"],
            "comment_neg_sentiment": sentiment["neg"],
            "comment_neu_sentiment": sentiment["neu"],
            "comment_compound": sentiment["compound"], 
            "source_platform": "youtube"  # Could also be 'reddit', 'youtube'
        })



videos=get_trending_videos(region_code="IN", max_results=50)

for video in videos:
    print(f"\n📹 {video['title']}")
    comments = get_video_comments(video['video_id'], video['title'])
    df = pd.DataFrame(comments)
    print(df.head())

insert_sentiment_data(data)