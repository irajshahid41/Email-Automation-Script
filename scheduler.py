import time
import threading
from email_service import send_email


class EmailScheduler:
    def __init__(self):
        self.running = False
        self.thread = None

    def _run(self, interval, to, subject, body):
        while self.running:
            try:
                send_email(to, subject, body)
                time.sleep(interval)
            except Exception as e:
                print("Scheduler Error:", e)

    def start(self, interval, to, subject, body):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(
                target=self._run,
                args=(interval, to, subject, body),
                daemon=True
            )
            self.thread.start()

    def stop(self):
        self.running = False