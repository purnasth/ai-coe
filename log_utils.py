import os
import time


def debug_log(msg, debug_envs=("local", "test")):
    env = os.getenv("ENV", "local").lower()
    if env in debug_envs:
        print(f"[DEBUG {time.strftime('%H:%M:%S')}] {msg}")


def output_log(msg):
    print(f"[OUTPUT] {msg}")
