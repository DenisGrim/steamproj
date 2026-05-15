import pandas as pd

def tag_filter(file="tags.csv")
    reminder = input("Remember you have to adjust tags and output file in script? ")
    df = pd.read_csv("tags.csv")

    required_tags = {"Story Rich", "Mystery"}
    forbidden_tags = {}

    # group tags per app_id
    grouped = df.groupby("app_id")["tag"].apply(set)

   # filter app_ids
    valid_ids = grouped[
        grouped.apply(lambda tags:
            required_tags.issubset(tags) and tags.isdisjoint(forbidden_tags)
        )
    ].index

    # filter original dataframe
    filtered = df[df["app_id"].isin(valid_ids)]

    filtered.to_csv("filtered_easy.csv", index=False)

