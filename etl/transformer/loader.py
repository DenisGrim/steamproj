import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user="user",
    password="pass",
    options="-c client_encoding=UTF8"
)

# TODO: maybe extra safeguard here? But tbf, I have that in my scraper I think
# I don't know how many weeks ago I wrote this todo, but i need another safeguard because of
# artifacts


def db_copy_reviews(file):

    cur = conn.cursor()
    cur.execute("SAVEPOINT before_copy")
    try:
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
    except psycopg2.error as e:
        cur.execute("ROLLBACK TO SAVEPOINT before_copy")
        conn.commit()
        with open("/errorfiles.txt", "a") as f:
            f.write(file)
    finally:
        cur.close()

def conn_rollback():
    conn.rollback()

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
