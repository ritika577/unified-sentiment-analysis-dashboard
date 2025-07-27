from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Initialize YouTube API
api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=api_key)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def get_trending_videos(region_code="IN", max_results=5):
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



# Fetch top-level comments for a video
def get_video_comments(video_id, max_results=50):
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
        comments.append({
            "comment": comment,
            "compound": sentiment["compound"],
            "pos": sentiment["pos"],
            "neu": sentiment["neu"],
            "neg": sentiment["neg"]
        })
    return comments
videos=get_trending_videos(region_code="IN", max_results=5)

for video in videos:
    print(f"\n📹 {video['title']}")
    comments = get_video_comments(video['video_id'])
    df = pd.DataFrame(comments)
    print(df.head())