from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import pandas as pd
from loader import db_copy


class Handler(FileSystemEventHandler):

    """
    def on_any_event(self, event):
        print(f"ANY EVENT: {event.event_type} - {event.src_path}", flush=True)

    def on_moved(self, event):
    """
    processed = set([])

    def on_closed(self, event):
        if event.src_path.endswith(".csv"):
            if event.src_path in self.processed:
                return
            print("ready: ", event.src_path)
            #print("transformer will sleep first")
            #time.sleep(0.5)
            append_review_length(event.src_path)
            convert_recommend(event.src_path)

            db_copy(event.src_path)
            # TODO: os.remove(file)
            # move instead of delete for now
            os.rename(event.src_path, "/mydata/del/" + event.src_path.lstrip("/mydata/"))
            self.processed.add(event.src_path)


def append_review_length(filepath):
    df = pd.read_csv(filepath)
    df["review_length"] = df["review"].fillna("").str.len().astype(int)
    df.to_csv(filepath, index=False)

def convert_recommend(filepath):
    df = pd.read_csv(filepath)
    df["does_recommend"] = df["does_recommend"].astype(int)

    """
    df["does_recommend"] = (
        df["does_recommend"]
        .map({"True": 1, "False": 0})
    )
    """

    df.to_csv(filepath, index=False)

def main():
    """
    print("transformer is ready")
    print(f"Watching directory: /mydata", flush=True)
    print(f"Directory exists: {os.path.exists('/mydata')}", flush=True)
    print(f"Directory contents: {os.listdir('/mydata')}", flush=True)
    """
    
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
