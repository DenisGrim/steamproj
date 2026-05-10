from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import pandas as pd
import loader as l
from encoder import embed_text


class Handler(FileSystemEventHandler):

    """
    def on_any_event(self, event):
        print(f"ANY EVENT: {event.event_type} - {event.src_path}", flush=True)

    def on_moved(self, event):
    """
    # remember all files it handles
    processed = set([])

    def on_closed(self, event):
        if event.src_path.endswith(".csv"):
            if event.src_path in self.processed:
                return
            file = event.src_path
            print("ready: ", file)
            df = pd.read_csv(file)
            append_review_length(df, file)
            convert_recommend(df, file)

            l.db_copy_reviews(file)
            add_embed_to_game(df)
            # TODO: os.remove(file)
            # move instead of delete for now
            os.rename(file, "/mydata/del/" + file.lstrip("/mydata/"))
            self.processed.add(file)


def append_review_length(df, file):
    df["review_length"] = df["review"].fillna("").str.len().astype(int)
    df.to_csv(file, index=False)


def convert_recommend(df, file):
    df["does_recommend"] = df["does_recommend"].astype(int)
    df.to_csv(file, index=False)


def add_embed_to_game(df):
    all_reviews = "\n".join(df["review"].dropna())
    # all_reviews might be too long at times. TODO
    eb = embed_text(all_reviews)
    l.insert_embedding_to_games(df.at[0, "app_id"], eb)


def main():
    l.db_copy_gameids("/mydata/poc_data/poc_input.csv")
    observer = Observer()
    observer.schedule(Handler(), path="/mydata", recursive=False)

    observer.start()
    print("Observer started!", flush=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
