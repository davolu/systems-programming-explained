import threading, time

lock = threading.Lock()

def withdraw(amount):
    global balance
    if balance >= amount:   # 1. check: is there enough?
        time.sleep(0.001)   # 2. a slow bank lookup
        balance -= amount   # 3. take the money

def safe_withdraw(amount):
    with lock:              # one person at the counter
        withdraw(amount)

def one_day(fn):
    global balance
    balance = 100
    people = [threading.Thread(target=fn, args=(80,))
              for _ in range(2)]
    for p in people: p.start()
    for p in people: p.join()
    return balance

for fn in (withdraw, safe_withdraw):
    days = [one_day(fn) for _ in range(1000)]
    bad = sum(b < 0 for b in days)
    print(f"{fn.__name__}: {bad} of 1000 days went negative,",
          "balances seen:", sorted(set(days)))
