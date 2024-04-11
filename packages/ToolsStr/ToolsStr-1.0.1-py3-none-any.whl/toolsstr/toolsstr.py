import time
import sys

class ToolsStr:
    def __init__(self, delay=0.05):
        self.delay = delay

    def TypeMaster(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(self.delay)
