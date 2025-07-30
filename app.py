import streamlit as st
import pandas as pd 
import seaborn as sns  
from datetime import datetime,timedelta 
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from db_connection import fetch_filtered_data
# load_dotenv()


# 🧠 Aggregate data for graph
def prepare_graph_data(df):
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date
    avg_sent = df.groupby(['date', 'source_platform'])['post_compound'].mean().reset_index()
    return avg_sent

# 🚀 Streamlit UI
st.set_page_config(page_title="Unified Sentiment Dashboard", layout="wide")
    
def get_date_range():
    # Default values: last 30 days
    default_end = datetime.now().date()
    default_start = default_end - timedelta(days=30)

    st.subheader("📅 Select Custom Date Range")

    # Select start and end dates individually
    start_date = st.date_input("Start Date", value=default_start, max_value=default_end)
    end_date = st.date_input("End Date", value=default_end, min_value=start_date, max_value=default_end)

    # Validation
    if start_date > end_date:
        st.error("❌ Start date cannot be after end date.")
    else:
        st.success(f"✅ Showing data from **{start_date}** to **{end_date}**")
    return start_date, end_date


def overview():
    st.title("📊 Unified Sentiment Dashboard Overview")
    st.caption("Last 30 Days | Reddit, YouTube & News")
    # 🔄 Load data
    start_date,end_date=get_date_range()
    df_all = fetch_filtered_data(start_date=start_date,end_date=end_date)
    # 🧮 Show table
    st.subheader("📊 Latest Sentiment Records")
    st.dataframe(df_all.head(100))  # limit preview

    # 📈 Plotting
    
    st.subheader("📈 Sentiment Trend by Platform")
    if not df_all.empty:
        
        chart_data = prepare_graph_data(df_all)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=chart_data, x='date', y='post_compound', hue='source_platform', ax=ax)
        ax.set_title("Average Daily Sentiment (Last 30 Days)")
        ax.set_ylabel("Sentiment Score")
        ax.set_xlabel("Date")
        st.pyplot(fig)


        # Make sure the created_at field is date-only
        df_all["created_date"] = pd.to_datetime(df_all["created_at"]).dt.date

        # Group by day and platform
        daily_trend = df_all.groupby(["created_date", "source_platform"]).size().reset_index(name="count")

        # 📈 Day with highest activity
        total_daily = daily_trend.groupby("created_date")["count"].sum()
        peak_day = total_daily.idxmax()
        peak_count = total_daily.max()
        st.write(f"🔺 The highest activity was on **{peak_day}** with **{peak_count} records** across all platforms.")

        # 🔝 Most active platform
        top_platform = df_all["source_platform"].value_counts().idxmax()
        platform_count = df_all["source_platform"].value_counts().max()
        st.write(f"💡 **{top_platform.capitalize()}** was the most active platform with **{platform_count} entries**.")

        # 🔼 Growth vs Decline Trend
        first_3_day = daily_trend["created_date"].min()
        last_3_day = daily_trend["created_date"].max()

        first_3 = daily_trend[daily_trend["created_date"] <= first_3_day + pd.Timedelta(days=2)]["count"].sum()
        last_3 = daily_trend[daily_trend["created_date"] >= last_3_day - pd.Timedelta(days=2)]["count"].sum()

        if last_3 > first_3:
            st.write("📈 There's an **upward trend** in sentiment activity over the past few days.")
        else:
            st.write("📉 There's been a **decline in sentiment activity** recently.")

        # 💥 Spike detection
        pivot = daily_trend.pivot(index="created_date", columns="source_platform", values="count").dropna()
        spike = pivot.diff().abs().max()
        spike_platform = spike.idxmax()
        if pd.notna(spike_platform) and isinstance(spike_platform, str):
            st.write(f"💡 **{spike_platform.capitalize()}** was the most active platform with **{platform_count} entries**.")
        else:
            st.warning("⚠️ No active platform data available.")

    else:
        st.warning("No data available to plot.")




def youtube():
    start_date,end_date=get_date_range()
    df_youtube = fetch_filtered_data(source_platform="youtube",start_date=start_date,end_date=end_date)
    st.title("📺 YouTube Sentiment Dashboard")

    if df_youtube.empty:
        st.warning("No YouTube data found for the past 30 days.")
        return

    # ✅ 2. Overview of Dataset
    st.subheader("📄 Latest YouTube Sentiment Dataset")
    st.dataframe(df_youtube.sort_values("created_at", ascending=False).reset_index(drop=True))

    # ✅ 3. Preprocessing Dates
    df_youtube["created_date"] = pd.to_datetime(df_youtube["created_at"]).dt.date

    # ✅ 4. Time Series Line Chart
    youtube_daily = df_youtube.groupby("created_date").size().reset_index(name="count")
    st.subheader("📈 Daily Sentiment Activity on YouTube")
    st.line_chart(youtube_daily.set_index("created_date")["count"])

    # ✅ 5. Insights Section
    st.subheader("💡 Insights from YouTube Sentiment Data")

    total_entries = len(df_youtube)
    top_day = youtube_daily.loc[youtube_daily["count"].idxmax()]
    avg_sentiment = df_youtube["comment_compound"].mean()
    sentiment_nature = "😊 Positive" if avg_sentiment > 0 else "😟 Negative" if avg_sentiment < 0 else "😐 Neutral"

    st.markdown(f"""
    - 📌 **Total comments analyzed**: `{total_entries}`
    - 🔺 **Most active day**: `{top_day['created_date']}` with `{top_day['count']}` entries
    - 📊 **Average sentiment score**: `{avg_sentiment:.2f}` → **{sentiment_nature}**
    """)

    # ✅ 6. Sentiment Category Assignment
    df_youtube["sentiment_category"] = df_youtube["comment_compound"].apply(
        lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral"
    )

    # ✅ 7. Sentiment Distribution
    sentiment_counts = df_youtube["sentiment_category"].value_counts()
    st.subheader("📊 Sentiment Category Distribution")
    st.bar_chart(sentiment_counts)

    st.info("This dashboard visualizes user sentiment from recent YouTube comments using VADER analysis.")


def news():
    start_date,end_date=get_date_range()
    df_news = fetch_filtered_data(source_platform="news",start_date=start_date,end_date=end_date)
    st.title("🗞️ News Sentiment Dashboard")


    st.subheader("📄 News Sentiment Dataset (Last 30 Days)")
    st.dataframe(df_news.sort_values("created_at", ascending=False).reset_index(drop=True))

    # Convert to date for grouping
    df_news["created_date"] = pd.to_datetime(df_news["created_at"]).dt.date

    # Group by date to get daily count
    news_daily = df_news.groupby("created_date").size().reset_index(name="count")

    st.subheader("📈 Daily News Sentiment Activity")
    st.line_chart(news_daily.set_index("created_date")["count"])

    # ➕ Assign sentiment category
    df_news["sentiment_category"] = df_news["comment_compound"].apply(
        lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral"
    )

    # 📊 Sentiment distribution
    sentiment_counts = df_news["sentiment_category"].value_counts()

    st.subheader("📊 Sentiment Distribution in News Headlines")
    st.bar_chart(sentiment_counts)

    # 📌 Total entries
    total_entries = len(df_news)
    top_day = news_daily.loc[news_daily["count"].idxmax()]
    avg_sentiment = df_news["comment_compound"].mean()
    sentiment_nature = "Positive 😊" if avg_sentiment > 0 else "Negative 😟" if avg_sentiment < 0 else "Neutral 😐"

    # 💡 Insights
    st.subheader("💡 Key Insights")
    st.markdown(f"- 🗂️ **Total News Headlines Analyzed**: `{total_entries}`")
    st.markdown(f"- 🔺 **Most Active Day**: `{top_day['created_date']}` with `{top_day['count']}` entries")
    st.markdown(f"- 📊 **Average Sentiment**: `{avg_sentiment:.2f}` → **{sentiment_nature}**")


def reddit():
    start_date,end_date=get_date_range()
    df_reddit = fetch_filtered_data(source_platform="reddit",start_date=start_date,end_date=end_date)
    st.title("👾 Reddit Sentiment Dashboard")

    # 📌 Filter only Reddit data
    df_reddit = df_reddit[df_reddit["source_platform"] == "reddit"].copy()

    # 🧾 Dataset preview
    st.subheader("🗃️ Recent Reddit Sentiment Data (Last 30 Days)")
    st.dataframe(df_reddit.sort_values("created_at", ascending=False).reset_index(drop=True), use_container_width=True)

    # 📅 Convert to date-only
    df_reddit["created_date"] = pd.to_datetime(df_reddit["created_at"]).dt.date

    # 📊 Line chart: Daily comment activity
    reddit_daily = df_reddit.groupby("created_date").size().reset_index(name="count")
    st.subheader("📈 Daily Sentiment Activity on Reddit")
    st.line_chart(reddit_daily.set_index("created_date")["count"])

    # 💬 Categorize sentiment
    df_reddit["sentiment_category"] = df_reddit["comment_compound"].apply(
        lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral"
    )
    sentiment_counts = df_reddit["sentiment_category"].value_counts()

    # 📊 Bar chart: Sentiment distribution
    st.subheader("📊 Sentiment Distribution")
    st.bar_chart(sentiment_counts)

    # 💡 Insights
    st.subheader("💡 Insights from Reddit Data")
    
    total_entries = len(df_reddit)
    top_day = reddit_daily.loc[reddit_daily["count"].idxmax()]
    avg_sentiment = df_reddit["comment_compound"].mean()
    sentiment_nature = (
        "😊 Positive" if avg_sentiment > 0 else 
        "😟 Negative" if avg_sentiment < 0 else 
        "😐 Neutral"
    )

    st.write(f"📌 Total entries: **{total_entries}**")
    st.write(f"🔺 Most active day: **{top_day['created_date']}** with **{top_day['count']} comments**")
    st.write(f"📊 Average sentiment: **{avg_sentiment:.2f}** → {sentiment_nature}")

    # 🚀 Top 3 trending post titles
    st.subheader("🔥 Top Trending Reddit Posts")
    trending_posts = df_reddit["post_title"].value_counts().head(3)
    for title, count in trending_posts.items():
        st.markdown(f"- **{title}** ({count} comments)")


# st.set_page_config(page_title="Unified Sentiment Dashboard", layout="wide")

# Sidebar navbar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Overview", "YouTube", "News", "Reddit"])

# Render content based on selection
if page == "Overview":
    # st.title("📌 Overview – Last 30 Days Sentiment Data")
    overview()  # Call the overview function
    # call your overview function here

elif page == "YouTube":
    # st.title("🎥 YouTube Sentiment Insights")
    youtube()  # call youtube-specific analysis


    # call youtube-specific analysis/graphs

elif page == "News":
    # st.title("📰 News Sentiment Insights")
    news()
    # call news-specific analysis

elif page == "Reddit":
    # st.title("👾 Reddit Sentiment Insights")
    reddit()
    # call reddit-specific analysis


