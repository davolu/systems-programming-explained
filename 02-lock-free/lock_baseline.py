import threading, time

counter = 0
lock = threading.Lock()

def work(n):
    global counter
    for _ in range(n):
        with lock:  # wait for the key, then add one
            counter += 1

for threads in (1, 4):
    counter = 0
    start = time.perf_counter()
    ts = [threading.Thread(target=work, args=(2_000_000 // threads,))
          for _ in range(threads)]
    for t in ts: t.start()
    for t in ts: t.join()
    secs = time.perf_counter() - start
    print(f"{threads} thread(s): counter = {counter}, {secs:.2f} s")
