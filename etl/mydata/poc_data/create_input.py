import pandas as pd

# takes a csv file with app_id and makes proof of concept input csv
file = input("file: ")
data = pd.read_csv(file)

# rids of duplicates, puts app_id as column name
new_data = pd.Series(data["app_id"].unique(), name = "app_id")
new_data.to_csv("poc_input.csv", index=False)
