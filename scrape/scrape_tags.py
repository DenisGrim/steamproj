from requests import get
import psycopg2
from json import dumps
import re
from bs4 import BeautifulSoup

html_url = "https://store.steampowered.com/app/2121980"

headers = headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Priority": "u=0, i"
}

def q_get_tags():
    # get html
    response = get(html_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    tags = [tag.get_text(strip=True) for tag in soup.select(".glance_tags a.app_tag")]
    return tags


def sql_test():
    conn = psycopg2.connect(
        host="db",
        #dbname="user",
        user="user",
        password="pass"
    )

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO games (name, id) VALUES (%s, %s);",
        ("void stranger", 2121980)
    )
    tags = q_get_tags()

    cur.executemany(
        """
        INSERT INTO game_tags (game_id, tag_id)
        SELECT %s, id
        FROM tags
        WHERE name = %s
        ON CONFLICT DO NOTHING;
        """,
        [(2121980,t) for t in tags]
    )
    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":
    sql_test()
