from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from db_connection import insert_sentiment_data
import requests
import os
from dotenv import load_dotenv
# load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")  # replace with your key

def get_top_news(country='India'):
    url = f"https://newsapi.org/v2/everything?q={country}&language=en&sortBy=popularity&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    print("data:  ", data)
    return data['articles']
data = []

# Example use
articles = get_top_news()
for article in articles[:5]:  # Print top 5
    print(f"📰 {article['title']}")
    print(f"📝 {article['description']}")
    print(f"🔗 {article['url']}\n")


analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    return analyzer.polarity_scores(text)

# Apply sentiment
for article in articles[:50]:
    headline = article['title']
    sentiment = analyze_sentiment(headline)
    print(f"📰 {headline}")
    print(f"📊 Sentiment: {sentiment}")
    print("-" * 50)
    data.append({
            "post_title":article['title'],
            "post_pos_sentiment": sentiment['pos'],
            "post_neg_sentiment": sentiment['neg'],
            "post_neu_sentiment": sentiment['neu'],            
            "post_compound": sentiment['compound'],
            "comment":"unknown",
            "comment_pos_sentiment": 0.0,
            "comment_neg_sentiment": 0.0,            
            "comment_neu_sentiment": 0.0,
            "comment_compound": 0.0,
            "source_platform": "news"
        })
insert_sentiment_data(data)