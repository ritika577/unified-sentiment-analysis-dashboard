# 🌐 Unified Sentiment Analysis Dashboard

A real-time, interactive Streamlit dashboard to analyze sentiment from **Reddit**, **YouTube**, and **News (NewsOrg API)**. This end-to-end pipeline uses **Python**, **VADER Sentiment Analysis**, and **Supabase PostgreSQL** to extract, analyze, store, and visualize public opinion from multiple platforms.

<img width="1824" height="682" alt="image" src="https://github.com/user-attachments/assets/c15ee7b0-b8b8-46a4-8bd2-3ff8d44baa1f" />


---

## 🚀 Live Demo

👉 [Click here to launch the app](https://unified-sentiment-analysis-dashboard.streamlit.app/)  
*(Hosted on Streamlit Cloud)*

---

## 📌 Key Features

- 🔄 **Real-Time Data Extraction** from:
  - Reddit (via PRAW)
  - YouTube (via YouTube Data API)
  - News Headlines (via NewsOrg API)

- 🧠 **Sentiment Classification** using VADER:
  - Positive / Neutral / Negative

- 📊 **Visual Dashboard** built with Streamlit:
  - Time-series sentiment trends
  - Platform-wise activity
  - Sentiment distribution charts
  - Top trending Reddit post titles

- 🗃️ **Database Storage**:
  - Stores all records in Supabase (PostgreSQL)
  - Prevents duplicate entries using composite unique constraints

- 📅 **Date Range Filtering**:
  - Analyze any custom time window
  - Default view: Last 30 days

---

## 🛠️ Tech Stack

| Layer            | Tools Used                                           |
|------------------|------------------------------------------------------|
| Backend          | Python, PRAW, YouTube API, NewsOrg API               |
| Sentiment Engine | VADER SentimentIntensityAnalyzer                     |
| Database         | Supabase (PostgreSQL)                                |
| Dashboard        | Streamlit, Pandas, Matplotlib, Seaborn               |
| Deployment       | Streamlit Cloud                                      |

---

## 📷 Dashboard Preview

| Overview Page | Platform Pages |
|---------------|----------------|
| ![overview](https://res.cloudinary.com/dsbxlxlmo/image/upload/v1753788031/Screenshot_2025-07-29_164814_o1uzhh.png) | ![youtube](https://res.cloudinary.com/dsbxlxlmo/image/upload/v1753788031/Screenshot_2025-07-29_164835_blxjbt.png) | 
![news](https://res.cloudinary.com/dsbxlxlmo/image/upload/v1753788033/Screenshot_2025-07-29_164853_iblm3g.png) | ![reddit](https://res.cloudinary.com/dsbxlxlmo/image/upload/v1753788032/Screenshot_2025-07-29_164905_auqiwb.png)

---

## 🔧 How to Run Locally

```bash
# 1. Clone this repo
git clone https://github.com/yourusername/unified-sentiment-analysis-dashboard.git
cd unified-sentiment-analysis-dashboard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up .env variables
cp .env.example .env  # Add your API keys and Supabase credentials

# 5. Run the app
streamlit run app.py
# unified-sentiment-analysis-dashboard
