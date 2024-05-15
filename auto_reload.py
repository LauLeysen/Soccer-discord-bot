import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import signal

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        self.script = script
        self.process = self.start_script()

    def start_script(self):
        return subprocess.Popen(["python", self.script])

    def restart_script(self):
        self.process.send_signal(signal.SIGTERM)
        self.process = self.start_script()

    def on_modified(self, event):
        if event.src_path.endswith(self.script):
            print(f"{self.script} has been modified. Restarting script...")
            self.restart_script()

if __name__ == "__main__":
    script_name = "bot.py"
    event_handler = ChangeHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    print(f"Watching for changes in {script_name}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
