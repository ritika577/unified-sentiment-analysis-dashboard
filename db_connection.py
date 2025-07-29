import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import execute_batch
from datetime import datetime, timedelta
import pandas as pd
import os
import atexit
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

conn=None
def get_connection():
    global conn
    if not conn or conn.closed:
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )
    return conn

def get_streamlit_conn():
    global conn
    if 'db_conn' not in st.session_state:    
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )
        st.session_state['db_conn'] = conn
        # Register close on exit
        atexit.register(lambda: conn.close())
    return st.session_state['db_conn']


def insert_sentiment_data(data):
    conn = get_connection()
    with conn.cursor() as cursor:
        query = """
        INSERT INTO platform_sentiments (
            post_title, comment, post_compound, comment_compound,
            post_pos_sentiment, post_neg_sentiment, post_neu_sentiment,
            comment_pos_sentiment, comment_neg_sentiment, comment_neu_sentiment,
            source_platform,
            created_at, updated_at
        ) VALUES (
            %(post_title)s, %(comment)s, %(post_compound)s, %(comment_compound)s,
            %(post_pos_sentiment)s, %(post_neg_sentiment)s, %(post_neu_sentiment)s,
            %(comment_pos_sentiment)s, %(comment_neg_sentiment)s, %(comment_neu_sentiment)s,
            %(source_platform)s,
            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
        )
        ON CONFLICT (post_title, comment,source_platform) DO NOTHING;

        """

        execute_batch(cursor, query, data, page_size=100)  # batch insert in chunks of 100
        conn.commit()
        print("✅ Insert successful or conflict skipped.")
        cursor.close()
        conn.close()

def fetch_filtered_data(source_platform=None, start_date=None, end_date=None):
    conn = get_streamlit_conn()
    
     # SQL query with parameter placeholders
    if source_platform:
        query = """
            SELECT *
            FROM platform_sentiments
            WHERE source_platform = %s AND created_at between %s and %s
            ORDER BY created_at DESC;
        """
        params = (source_platform, start_date,end_date)
    else:
        query = """
            SELECT *
            FROM platform_sentiments
            WHERE created_at between %s and %s
            ORDER BY created_at DESC;
        """
        params = (start_date,end_date)



    df = pd.read_sql(query, conn, params=params)
    return df

   


