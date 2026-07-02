from requests import get
from requests.exceptions import HTTPError
import time, random
from pathlib import Path
import psycopg2
import csv
import os
import json
import pandas as pd

"""
   scrapes reviews off of steam via api, puts information into csvs into shared 'mydata' folder
"""

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

SCRIPT_DIR = Path(__file__).resolve().parent
in_docker = os.getenv("RUNNING_IN_DOCKER") == "1"

def get_reviews(app_id, cursor = "*"):
    html_url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    params = {"filter": "recent", "language": "all", "cursor": cursor, "num_per_page": "100"}

    # get raw json
    response = get(html_url, params=params, headers=headers)
    #text = response.text.encode('utf-8').decode('utf-8-sig')
    #response = text.json()
    return response


def parser(response):
    response = response.content.decode('utf-8-sig')
    return json.loads(response)

# handle if json is broken. Return True if unsalvagable
# TODO still breaks if review wasn't read as string
def broken_reviews(data):
    # make sure reviews exist and in right format. cast is needed & possible
    if not isinstance(data, dict):
        return True
    if "reviews" not in data:
        return True
    if not isinstance(data["reviews"], list):
        return True
    if len(data["reviews"]) == 0:
        return True

    req_keys = {"author", "review", "voted_up", "votes_funny", "votes_up", "weighted_vote_score"}
    req_author_keys = {"steamid", "playtime_at_review"}
    for review in data["reviews"]:
        if not isinstance(review, dict):
            return True
        if not req_keys.issubset(review.keys()):
            return True
        if not isinstance(review["author"], dict):
            return True
        if not req_author_keys.issubset(review["author"].keys()):
            return True

        try:
            review["author"]["steamid"] = int(review["author"]["steamid"])
            review["author"]["playtime_at_review"] = int(review["author"]["playtime_at_review"])
            review["voted_up"] = int(review["voted_up"])
            review["votes_funny"] = int(review["votes_funny"])
            review["votes_up"] = int(review["votes_up"])
            review["weighted_vote_score"] = float(review["weighted_vote_score"])
        except (ValueError, TypeError, KeyError) as e:
            return True

    return False


def write_review_file(app_id, data, tmp_path = None):
    filename = f"{app_id}_reviews"

    # handle broken files
    broken_review_log = SCRIPT_DIR / ".." / "broken_reviews.csv"
    if in_docker:
        broken_review_log = "/broken_reviews.csv"
    if broken_reviews(data):
        with open(broken_review_log, "a") as f:
            f.write(str(app_id) + "\n")
        print("broken review json: " + str(app_id))
        return

    # remove all reviews with no review-text (review text is in ["review"])
    data["reviews"] = [review for review in data["reviews"] if len(review["review"]) > 0]

    # check if no valid reviews. Don't write empty files
    if len(data["reviews"]) == 0:
        print(f"reviews for {app_id} don't exist!")
        return
    
    base = SCRIPT_DIR / ".." / "mydata"
    path = base / f"{filename}.csv"

    if in_docker:
        path = f"/mydata/{filename}.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["app_id", "user_id", "review", "does_recommend", "funny",
                "helpful", "weight", "playtime_at_review"])  # header
 
        for r in data["reviews"]:
            steamid = r["author"]["steamid"]
            review = r["review"]
            recommend = r["voted_up"]
            funny = r["votes_funny"]
            helpful = r["votes_up"]
            weight = r["weighted_vote_score"]
            playtime = r["author"]["playtime_at_review"]
            writer.writerow([app_id, steamid, review, recommend, funny,
                helpful, weight, playtime])
        f.close()
        print(f"done writing {app_id}")


def main():

    path = SCRIPT_DIR / ".." / "mydata" / "appid_queue.csv"
    if in_docker:
        # remove file signalling observer is ready
        os.remove("/mydata/setup-complete")
        path = "/mydata/appid_queue.csv"

    data = pd.read_csv(path)
    for app_id in data["app_id"].unique():
        response = get_reviews(app_id)

        # handle rate limitation
        if not response:
            for i in range(2,6):
                delay = i * i * 5
                print(f"rate limit. Retrying {app_id} in {delay}")
                time.sleep(delay)
                response = get_reviews(app_id)
                if response:
                    break

        response = parser(response)
        write_review_file(app_id, response)
        time.sleep(random.uniform(0.8, 2.0))


if __name__ == "__main__":
    main()
