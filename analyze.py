import pandas as pd
import numpy as np
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from transformer.encoder import embed_text


def make_matrix():

    # load csv
    df = pd.read_csv("mydata/poc_data/output.csv")
    # throw away rows without embedding
    df = df.dropna(subset="embedding")
    # convert embedding strings to lists
    embeddings = np.array(
        df["embedding"].apply(ast.literal_eval).tolist()
    )

    # compute cosine similarity matrix
    sim_matrix = cosine_similarity(embeddings)

    # dataframe with labels
    sim_df = pd.DataFrame(
        sim_matrix,
        index=df["app_id"],
        columns=df["app_id"]
    )

    # plot
    sns.heatmap(sim_df)

    plt.show()

def make_ranker(text = ""):
    
    df = pd.read_csv("mydata/poc_data/output.csv")
    df = df.dropna(subset="embedding")
    embeddings = np.array(
        df["embedding"].apply(ast.literal_eval).tolist()
    )
    if text == "":
        file = input("file: ")
        with open(file, "r") as f:
            text = f.read()

        query_embedding = np.array(
        embed_text(text)
    ).reshape(1, -1)

    # compare query against all embeddings
    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    # sort descending
    order = np.argsort(similarities)[::-1]

    similarities = similarities[order]
    app_ids = df["app_id"].iloc[order].values

    # dataframe for plotting
    sim_df = pd.DataFrame(
        [similarities],
        columns=app_ids,
        index=["query"]
    )

    # heatmap
    plt.figure(figsize=(12, 2))

    sns.heatmap(
        sim_df,
        annot=True,
        fmt=".2f"
    )

    plt.show()

