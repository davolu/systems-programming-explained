import threading, time

for safe in (False, True):
    counter, lock = 0, threading.Lock()
    def add():
        global counter
        for _ in range(1000):
            if safe: lock.acquire()
            seen = counter      # read
            time.sleep(0)       # deliberately let another thread run
            counter = seen + 1  # write
            if safe: lock.release()
    people = [threading.Thread(target=add) for _ in range(2)]
    for p in people: p.start()
    for p in people: p.join()
    print(f"safe={safe}: expected 2000, got {counter}")
