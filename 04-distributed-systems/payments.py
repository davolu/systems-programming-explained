import uuid

charges = []   # the bank's record of real charges
seen = {}      # idempotency key -> the first answer we gave

def charge(amount, key=None):
    if key in seen:              # this exact request again?
        return seen[key]         # send back the first answer
    charges.append(amount)       # really take the money
    result = f"charged ${amount}"
    if key: seen[key] = result
    return result

def call_over_network(amount, key, attempt):
    result = charge(amount, key)       # the server does the work...
    if attempt == 1:                   # ...but (simulated) the reply
        raise TimeoutError("lost")     # is lost on the first try
    return result

def pay(amount, key=None):
    for attempt in (1, 2, 3):
        try:
            return call_over_network(amount, key, attempt)
        except TimeoutError:
            print(f"  attempt {attempt}: no reply, retrying")

for use_key in (False, True):
    charges.clear(); seen.clear()
    key = str(uuid.uuid4()) if use_key else None
    pay(20, key)
    print(f"key={use_key}: charged {len(charges)} time(s),",
          f"total ${sum(charges)}")
