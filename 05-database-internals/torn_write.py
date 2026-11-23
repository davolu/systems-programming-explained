import json, os, zlib, multiprocessing as mp

LOG = "torn.log"

def entry(key, value):                 # checksum + data, on one line
    body = json.dumps([key, value])
    return f"{zlib.crc32(body.encode())} {body}\n"

def power_cut():
    with open(LOG, "w") as f:
        f.write(entry("ada", 100)); f.write(entry("bob", 50))
        f.write(entry("ada", 70)[:12])  # only part of the last entry...
        f.flush()
        os._exit(1)                     # ...then the power goes out

def naive_replay():
    data = {}
    for line in open(LOG):
        key, value = json.loads(line.split(" ", 1)[1])
        data[key] = value
    return data

def checked_replay():
    data, kept = {}, 0
    for line in open(LOG):
        crc, _, body = line.rstrip("\n").partition(" ")
        if not line.endswith("\n") or str(zlib.crc32(body.encode())) != crc:
            break                       # broken entry: stop here
        key, value = json.loads(body)
        data[key] = value; kept += 1
    return data, kept

p = mp.Process(target=power_cut); p.start(); p.join()
print("log ends with:", repr(open(LOG).read()[-24:]))
try: print("naive replay:", naive_replay())
except ValueError as e: print("naive replay crashed:", type(e).__name__)
data, kept = checked_replay()
print(f"checked replay: kept {kept} good entries -> {data}")
