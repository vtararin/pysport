import sireader
import threading
import time


class SIRead(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.daemon = True
        self.parent = parent
        self.is_running = False

    def run(self):
        i = 0
        while True:
            if self.is_running:
                self.parent.status.set('%d', i)
                i += 1
                time.sleep(1)
