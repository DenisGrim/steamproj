import psycopg2
import os

def db_copy(file):
    conn = psycopg2.connect(
        host="db",
        user="user",
        password="pass"
    )

    cur = conn.cursor()
    with open(file, "r") as f:
        cur.copy_expert("""
            COPY reviews(
                game_id,
                user_id,
                review,
                does_recommend,
                funny,
                helpful,
                weight,
                playtime_at_review,
                review_length
            )
            FROM STDIN WITH CSV HEADER
        """, f)

    conn.commit()

    cur.close()
    conn.close()
