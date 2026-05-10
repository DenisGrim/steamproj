from requests import get
import time, random
from pathlib import Path
import psycopg2
import csv
import json
import pandas as pd

# TODO idk if I need this. Doesnt just /mydata... work?
base_path = Path(__file__).resolve().parent

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

def get_reviews(app_id, cursor = "*"):
    html_url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    params = {"filter": "recent", "language": "all", "cursor": cursor, "num_per_page": "100"}

    # get raw json
    response = get(html_url, params=params, headers=headers).json()
    return response


def write_review_file(app_id, data):
    filename = f"{app_id}_reviews"

    # check if no reviews
    if len(data["reviews"]) == 0:
        print(f"reviews for {app_id} don't exist!")

    with open(base_path / f"../mydata/{filename}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["app_id", "user_id", "review", "does_recommend", "funny", "helpful", "weight", "playtime_at_review"])  # header
 
        for r in data["reviews"]:
            steamid = r["author"]["steamid"]
            review = r["review"]
            recommend = r["voted_up"]
            funny = r["votes_funny"]
            helpful = r["votes_up"]
            weight = r["weighted_vote_score"]
            playtime = r["author"]["playtime_at_review"]
            writer.writerow([app_id, steamid, review, recommend, funny, helpful, weight, playtime])
        f.close()
        print(f"done writing {app_id}")


def main():
    # TODO random csv name
    data = pd.read_csv(base_path / "../mydata/poc_data/poc_input.csv")
    for app_id in data["app_id"].unique():
        response = get_reviews(app_id)

        # handle rate limitation
        if response["success"] == 0:
            for i in range(2,6):
                delay = i * i * 5
                print(f"rate limit. Retrying {app_id} in {delay}")
                time.sleep(delay)
                response = get_reviews(app_id)
                if response["success"] == 1:
                    break

        if response["success"] == 0:
            return

        write_review_file(app_id, response)
        print(f"{app_id} reviews written\n")
        time.sleep(random.uniform(0.8, 2.0))

if __name__ == "__main__":
    main()
