from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import pandas as pd
import loader as l
from encoder import embed_text, embed_batch
import tracemalloc



class Handler(FileSystemEventHandler):

    """
    def on_any_event(self, event):
        print(f"ANY EVENT: {event.event_type} - {event.src_path}", flush=True)

    def on_moved(self, event):
    """
    def __init__(self):
        tracemalloc.start()
        # remember all files it handles
        self.processed = set([])
        self.batch = {}
        self._snapshot = tracemalloc.take_snapshot()

    def on_closed(self, event):
        if event.src_path.endswith("reviews.csv"):
            if event.src_path in self.processed:
                return
            file = event.src_path
            print("ready: ", file)
            df = pd.read_csv(file)
            self.append_review_length(df, file)
            self.convert_recommend(df, file)

            l.db_copy_reviews(file)
            self.add_embed_to_game(df)
            # TODO: os.remove(file)
            # move instead of delete for now
            os.rename(file, "/mydata/del/" + file.lstrip("/mydata/"))
            self.processed.add(file)

            # TODO: this just writes into root directory rn, prob shouldnt always
            with open("/transformerlogs.txt", "a") as f:
                 snap2 = tracemalloc.take_snapshot()
                 top_stats = snap2.compare_to(self._snapshot, 'lineno')
                 f.write("[ top 10 diffs ]\n")
                 for stat in top_stats[:10]:
                     f.write(str(stat) + "\n")
                 self._snapshot = snap2


    def append_review_length(self, df, file):
        df["review_length"] = df["review"].fillna("").str.len().astype(int)
        df.to_csv(file, index=False)


    def convert_recommend(self, df, file):
        df["does_recommend"] = df["does_recommend"].astype(int)
        df.to_csv(file, index=False)


    # all_reviews might be too long at times. TODO
    def add_embed_to_game(self, df):
        all_reviews = "\n".join(df["review"].fillna("").astype(str))
        cur_app_id = df.at[0, "app_id"]
        if cur_app_id == "stop":
            self.flush_batch()
            return

        self.batch[cur_app_id] = all_reviews

        # TODO bath size should 100% be env variable
        if len(self.batch) >= 2:
            self.flush_batch()


    def flush_batch(self):
        all_ebs = embed_batch(self.batch)
        for app_id, eb in all_ebs.items():
            l.insert_embedding_to_games(app_id, eb)
        self.batch = {}


def main():
    observer = Observer()
    observer.schedule(Handler(), path="/mydata", recursive=False)

    observer.start()
    print("Observer started!", flush=True)

    # marks service as healthy (see dockercompose)
    with open("/mydata/setup-complete", "w") as f:
        f.close()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
