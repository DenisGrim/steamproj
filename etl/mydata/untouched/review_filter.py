import pandas as pd

csv = input("file: ")
tags_df = pd.read_csv(csv, usecols=["app_id"])
reviews_df = pd.read_csv("reviews.csv", usecols=["app_id", "total"])

reviews_df["total"] = pd.to_numeric(reviews_df["total"], errors="coerce")

# How many reviews
valid_apps = reviews_df[reviews_df["total"] >= 10]["app_id"]

# keep only those in filtered.csv
final_df = tags_df[tags_df["app_id"].isin(valid_apps)]

final_df.to_csv(csv.rstrip(".csv") + "_reviewfiltered.csv", index=False)
