import psycopg2
import pandas as pd

"""
 dumper gives functions to be used in etl-container python console to create files out of db
 while still in proof of concept phase (meaning I'll still remove volume a bunch)
"""

def dump_games():
    conn = psycopg2.connect(
            host = "db",
            user="user",
            password="pass"
    )
    
    cur = conn.cursor()
    df = pd.read_sql("""
         SELECT *
         FROM games
         """, conn)
    
    # writing to txt because csvs are in gitignore
    print(f"wriitng output.txt with shape: {df.shape}")
    df.to_csv("/mydata/poc_data/output.csv", index=False)
