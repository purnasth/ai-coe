import os
import time


def debug_log(msg):
    env = os.getenv("ENV", "local").lower()
    if env in ("test", "testing"):
        print(f"[DEBUG {time.strftime('%H:%M:%S')}] {msg}")


def output_log(msg):
    print(f"[OUTPUT] {msg}")
