import psycopg2
import os

conn = psycopg2.connect(
    host="db",
    user="user",
    password="pass"
)

def db_copy_reviews(file):

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


def insert_embedding_to_games(game_id, tensor):
    cur = conn.cursor()

    tensor_list = tensor.tolist()
    # cast from numpy.int64 to normal int for sql
    game_id = int(game_id)

    cur.execute(
            "UPDATE games SET embedding = %s::vector WHERE app_id = %s",
        (tensor_list, game_id)
    )

    conn.commit()
    cur.close()
