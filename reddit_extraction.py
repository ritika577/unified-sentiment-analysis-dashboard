import praw
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
from db_connection import insert_sentiment_data
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
# Load environment variables from .env
load_dotenv()
def get_sentiment(text):
    return analyzer.polarity_scores(text)

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Choose a subreddit
subreddit = reddit.subreddit("india")

data = []

for post in subreddit.hot(limit=200):
    post.comments.replace_more(limit=0)
    post_sent = get_sentiment(post.title + " " + post.selftext)
    # print(post_sent)

    for comment in post.comments[:50]:
        comment_sent = get_sentiment(comment.body)
        data.append({"post_title":post.title[100:],
        "post_pos_sentiment": post_sent['pos'],
        "post_neg_sentiment": post_sent['neg'],
        "post_neu_sentiment": post_sent['neu'],
        "post_compound": post_sent['compound'],
        "comment":comment.body[100:],
        "comment_pos_sentiment": comment_sent['pos'],
        "comment_neg_sentiment": comment_sent['neg'],
        "comment_neu_sentiment": comment_sent['neu'],
        "comment_compound": comment_sent['compound'],
        "source_platform": "reddit"
          }) # Could also be 'reddit', 'youtube'
        
insert_sentiment_data(data)
