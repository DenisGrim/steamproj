import zipfile
import pandas as pd


def ex_ids(zip_path: str):
    with zipfile.ZipFile(zip_path, "r") as z:
        csv_names = [name.split("_")[0] for name in z.namelist() if name.lower().endswith(".csv")]

    df = pd.DataFrame({"app_id": csv_names})

