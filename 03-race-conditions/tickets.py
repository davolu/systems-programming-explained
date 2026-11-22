import threading, time

class Dispenser:
    def __init__(self, safe):
        self.next = 1
        self.safe = safe
        self.lock = threading.Lock()

    def take(self):
        if self.safe:
            with self.lock:
                return self._take()
        return self._take()

    def _take(self):
        n = self.next       # read the number
        time.sleep(0)       # a tiny pause: let others run
        self.next = n + 1   # move the counter on
        return n

def check(history):
    tickets = [t for _, _, t in history]
    dupes = len(tickets) - len(set(tickets))
    sequence_ok = sorted(tickets) == list(range(1, len(tickets) + 1))
    # replay in ticket order: nobody may finish before
    # someone with a smaller ticket has even started
    late, latest_start = 0, 0
    for start, end, t in sorted(history, key=lambda h: h[2]):
        if end < latest_start: late += 1
        latest_start = max(latest_start, start)
    return dupes, late, sequence_ok

for safe in (False, True):
    d, history = Dispenser(safe), []
    def customer():
        for _ in range(200):
            start = time.perf_counter_ns()
            t = d.take()
            history.append((start, time.perf_counter_ns(), t))
    crowd = [threading.Thread(target=customer) for _ in range(8)]
    for c in crowd: c.start()
    for c in crowd: c.join()
    dupes, late, sequence_ok = check(history)
    ok = sequence_ok and late == 0
    print(f"safe={safe}: {len(history)} tickets,",
          f"{dupes} duplicates, {late} out of order")
    print(f"   sequence 1..1600: {sequence_ok} ->",
          "linearizable" if ok else "NOT linearizable")
