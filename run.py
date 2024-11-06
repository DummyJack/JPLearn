import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import psutil

class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = time.time()
        self.process = None
        self.start_app()

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_modified > 1:
                self.last_modified = current_time
                print(f"\n檔案已更新: {event.src_path}")
                self.restart_app()

    def start_app(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        
        print("\n啟動應用程式...")
        self.process = subprocess.Popen([sys.executable, "src/main.py"])

    def restart_app(self):
        print("重新啟動應用程式...")
        self.start_app()

    def stop_app(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

    def is_app_running(self):
        if self.process:
            try:
                return psutil.Process(self.process.pid).is_running()
            except psutil.NoSuchProcess:
                return False
        return False

if __name__ == "__main__":
    path = "src"
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    print("\n應用程式已啟動，按 Ctrl+C 可以完全退出程式")

    try:
        while True:
            time.sleep(1)
            if not event_handler.is_app_running():
                print("\n視窗已關閉，請按 Ctrl+C 完全退出程式")
                while True:
                    time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止監視...")
        event_handler.stop_app()
        observer.stop()
        observer.join()
