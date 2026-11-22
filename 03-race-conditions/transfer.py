import threading, time

class Account:
    def __init__(self, name, money):
        self.name, self.money = name, money
        self.lock = threading.Lock()

def transfer(src, dst, amount, same_order):
    first, second = src, dst
    if same_order:  # always lock in alphabetical order
        first, second = sorted([src, dst], key=lambda a: a.name)
    with first.lock:
        time.sleep(0.1)  # time for the other thread to grab a lock
        if not second.lock.acquire(timeout=2):
            return "stuck"
        src.money -= amount
        dst.money += amount
        second.lock.release()
        return "done"

for same_order in (False, True):
    ada, bob = Account("Ada", 100), Account("Bob", 100)
    results = []
    def go(src, dst, amount):
        results.append(transfer(src, dst, amount, same_order))
    start = time.perf_counter()
    a = threading.Thread(target=go, args=(ada, bob, 30))
    b = threading.Thread(target=go, args=(bob, ada, 10))
    a.start(); b.start(); a.join(); b.join()
    print(f"same_order={same_order}: {results},",
          f"Ada {ada.money}, Bob {bob.money},",
          f"{time.perf_counter() - start:.1f} s")
