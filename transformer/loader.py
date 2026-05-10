import psycopg2
import os

#takes file that is used for scraping. Run via transformer for now. TODO make main.py
# this maybe in db cause it makes no sense here? TODO
def db_copy_gameids(file):
    conn = psycopg2.connect(
        host="db",
        user="user",
        password="pass"
    )
    cur = conn.cursor()
    with open(file, "r") as f:
        cur.copy_expert("""
            COPY games(
                id
            )
            FROM STDIN WITH CSV HEADER
        """, f)

    conn.commit()

    cur.close()
    conn.close()


# TODO make connection just one time
def db_copy_reviews(file):
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


def insert_embedding_to_games(game_id, tensor):
    conn = psycopg2.connect(
        host="db",
        user="user",
        password="pass"
    )
    cur = conn.cursor()

    tensor_list = tensor.tolist()
    # cast from numpy.int64 to normal int for sql
    game_id = int(game_id)

    cur.execute(
            "UPDATE games SET embedding = %s::vector WHERE id = %s",
        (tensor_list, game_id)
    )

    conn.commit()
    cur.close()
