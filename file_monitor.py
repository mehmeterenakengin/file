import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

LOG_FILE = "/home/kali/bsm/logs/changes.json"

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        change = {
            "event_type": event.event_type,
            "file_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.log_change(change)

    def log_change(self, change):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as file:
                json.dump([], file)

        with open(LOG_FILE, "r+") as file:
            data = json.load(file)
            data.append(change)
            file.seek(0)
            json.dump(data, file, indent=4)

if __name__ == "__main__":
    path = "/home/kali/bsm/test"
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print(f"Monitoring changes in {path}")
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
