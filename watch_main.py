import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import threading

WATCHED_EXTENSIONS = [".py"]
EXCLUDE_DIRS = {"__pycache__", ".venv", "chroma_db"}


class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, command, debounce_seconds=1.0):
        self.command = command
        self.process = None
        self.debounce_seconds = debounce_seconds
        self._debounce_timer = None
        self._lock = threading.Lock()
        self.start_process()

    def start_process(self):
        with self._lock:
            if self.process:
                self.process.terminate()
                self.process.wait()
            self.process = subprocess.Popen(self.command)

    def _debounced_restart(self):
        with self._lock:
            if self._debounce_timer:
                self._debounce_timer.cancel()
            self._debounce_timer = threading.Timer(
                self.debounce_seconds, self.start_process
            )
            self._debounce_timer.start()

    def on_modified(self, event):
        if event.is_directory:
            return
        if not any(event.src_path.endswith(ext) for ext in WATCHED_EXTENSIONS):
            return
        if any(excl in event.src_path for excl in EXCLUDE_DIRS):
            return
        if os.path.abspath(event.src_path) == os.path.abspath(__file__):
            return
        print(f"Detected change in {event.src_path}, scheduling restart of main.py...")
        self._debounced_restart()

    def stop(self):
        with self._lock:
            if self._debounce_timer:
                self._debounce_timer.cancel()
            if self.process:
                self.process.terminate()
                self.process.wait()


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    command = [sys.executable, "main.py"]
    event_handler = RestartOnChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print(f"Watching for changes in {path}. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping watcher...")
        observer.stop()
        event_handler.stop()
    observer.join()
