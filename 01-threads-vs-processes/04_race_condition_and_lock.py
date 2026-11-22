"""A race condition on a shared 'tip jar', then the fix with threading.Lock.
time.sleep(0) is a tiny, deliberate distraction that makes the gap between read and write easy to see."""
import threading
import time

balance = 0
lock = threading.Lock()


def deposit():
    global balance
    for _ in range(1000):
        current = balance      # 1. read the jar
        time.sleep(0)          # 2. get distracted for a moment
        balance = current + 1  # 3. write the new total


def safe_deposit():
    global balance
    for _ in range(1000):
        with lock:  # only one thread inside at a time
            current = balance
            time.sleep(0)
            balance = current + 1


def run(job):
    global balance
    balance = 0
    threads = [threading.Thread(target=job) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    return balance


if __name__ == "__main__":
    print("No lock:   expected 5000, got", run(deposit))
    print("With lock: expected 5000, got", run(safe_deposit))
