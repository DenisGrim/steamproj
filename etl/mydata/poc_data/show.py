import pandas as pd
import matplotlib.pyplot as plt

csv = input("file: ")
df = pd.read_csv(csv)

top_tags = df["tag"].value_counts().head(10)

top_tags.plot(kind="bar")
plt.ylabel("count")
plt.xlabel("tag")
plt.title("Top 10 tags")
plt.show()
