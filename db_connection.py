import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import execute_batch
from datetime import datetime
import os
from dotenv import load_dotenv
# load_dotenv()
# ✅ Set up connection globally or pass it in
conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )

def insert_sentiment_data(data):
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
