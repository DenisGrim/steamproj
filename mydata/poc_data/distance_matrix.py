import pandas as pd
import numpy as np
import ast
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity

# load csv
df = pd.read_csv("output.csv")
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
