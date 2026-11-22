import json, os, time

LOG, SNAP = "big.log", "checkpoint.json"

def replay(start=0, data=None):
    data = dict(data or {})
    with open(LOG) as f:
        f.seek(start)                    # jump to where we left off
        for line in f:
            key, value = json.loads(line)
            data[key] = value
    return data

with open(LOG, "w") as f:                # a long diary: 500,000 changes
    for i in range(500_000):
        f.write(json.dumps([f"user{i % 1000}", i]) + "\n")

t0 = time.perf_counter(); full = replay()
print(f"full replay: 500,000 entries in {time.perf_counter() - t0:.2f} s")

with open(SNAP, "w") as f:               # checkpoint: the whole shelf
    json.dump({"data": full, "log_pos": os.path.getsize(LOG)}, f)
with open(LOG, "a") as f:                # 1,000 more changes after it
    for i in range(1000):
        f.write(json.dumps([f"user{i}", -i]) + "\n")

t0 = time.perf_counter()
snap = json.load(open(SNAP))
fast = replay(snap["log_pos"], snap["data"])
print(f"from checkpoint: {time.perf_counter() - t0:.3f} s,",
      f"same result as a full replay: {fast == replay()}")
